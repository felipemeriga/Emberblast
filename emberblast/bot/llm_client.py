import json
import logging
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

JOB_TRAITS = {
    "Knight": (
        "Honorable and brave. You charge headfirst into battle and respect"
        " strength above all. You protect the weak and fight with discipline."
    ),
    "Wizard": (
        "Calculating and intellectual. You position carefully, preferring to"
        " strike from a distance with devastating magic."
        " You look down on brute force."
    ),
    "Rogue": (
        "Opportunistic and sneaky. You avoid fair fights, preferring to"
        " strike from the shadows. You look for cheap shots and escape routes."
    ),
    "Archer": (
        "Patient and methodical. You keep your distance and pick off enemies"
        " one by one. You value precision over power."
    ),
    "Priest": (
        "Cautious and wise. You are a reluctant combatant who prefers healing"
        " and support. You fight only when cornered."
    ),
}

RACE_MODIFIERS = {
    "Orc": "You are aggressive, blunt, and love to trash-talk your enemies.",
    "Elf": "You are eloquent, condescending, and surgically precise in everything you do.",
    "Dwarf": "You are grumpy, stubborn, and have a dry sense of humor.",
    "Halflings": "You are nervous, scrappy, and fight with underdog energy.",
    "Human": "You are balanced, adaptable, and practical in your approach.",
}

SYSTEM_TEMPLATE = """You are {name}, a {race} {job} in a tactical RPG deathmatch.

Personality: {job_trait} {race_modifier}

You must choose one action per turn based on the game state provided. Respond ONLY with a JSON object:
{{
  "action": "<one of the available actions>",
  "target": "<target player name, if applicable>",
  "skill_name": "<skill to use, if action is skill>",
  "item_name": "<item to use, if action is item>",
  "move_to": "<destination tile, if action is move>",
  "narration": "<a short in-character line, 1 sentence, spoken aloud>"
}}

Rules:
- You can only move to tiles listed in bot_walkable_tiles_in_range
- You can only attack/skill enemies within your range
- Skills cost mana — check you have enough
- Think tactically: consider positioning, health, mana, and enemy threats
- Stay in character with your narration"""


def build_personality_prompt(name: str, job_name: str, race_name: str) -> str:
    """Build a system prompt with personality traits based on job and race."""
    job_trait = JOB_TRAITS.get(job_name, f"A skilled {job_name}.")
    race_modifier = RACE_MODIFIERS.get(race_name, f"You have the traits of a {race_name}.")
    return SYSTEM_TEMPLATE.format(
        name=name,
        race=race_name,
        job=job_name,
        job_trait=job_trait,
        race_modifier=race_modifier,
    )


def serialize_game_state(
    bot: Any,
    enemies: List[Any],
    game: Any,
    memory_entries: List[str],
    available_actions: List[str],
) -> Dict:
    """Serialize the current game state into a dict suitable for LLM consumption."""
    skills_data = []
    for skill in bot.skills:
        if skill.cost <= bot.mana:
            skills_data.append(
                {
                    "name": skill.name,
                    "damage": skill.base,
                    "mana_cost": skill.cost,
                    "range": skill.ranged,
                    "kind": skill.kind,
                }
            )

    bag_items = []
    for item in bot.bag.items:
        item_data = {"name": item.name, "tier": item.tier}
        if hasattr(item, "attribute"):
            item_data["attribute"] = item.attribute
        if hasattr(item, "base"):
            item_data["value"] = item.base
        bag_items.append(item_data)

    equipment = {}
    for slot in ["weapon", "armour", "boots", "accessory"]:
        eq = getattr(bot.equipment, slot, None)
        equipment[slot] = eq.name if eq else None

    effects = []
    for se in bot.side_effects:
        effects.append(
            {
                "name": se.name,
                "turns_remaining": se.duration,
                "effect_type": se.effect_type,
            }
        )

    enemies_data = []
    for enemy in enemies:
        if not enemy.is_hidden():
            distance = game.game_map.graph.get_shortest_distance_between_positions(bot.position, enemy.position)
            enemies_data.append(
                {
                    "name": enemy.name,
                    "job": enemy.job.get_name(),
                    "position": enemy.position,
                    "life": enemy.life,
                    "max_life": enemy.health_points,
                    "distance": round(distance, 1),
                }
            )

    walkable = game.game_map.graph.get_available_nodes_in_range(bot.position, bot.move_speed)

    return {
        "current_bot": {
            "name": bot.name,
            "job": bot.job.get_name(),
            "race": bot.race.get_name(),
            "level": bot.level,
            "position": bot.position,
            "life": bot.life,
            "max_life": bot.health_points,
            "mana": bot.mana,
            "max_mana": bot.magic_points,
            "attack_type": bot.job.attack_type,
            "attributes": {
                "strength": bot.strength,
                "intelligence": bot.intelligence,
                "accuracy": bot.accuracy,
                "armour": bot.armour,
                "magic_resist": bot.magic_resist,
                "move_speed": bot.move_speed,
            },
            "available_skills": skills_data,
            "bag_items": bag_items,
            "equipment": equipment,
            "active_effects": effects,
        },
        "enemies": enemies_data,
        "map": {
            "bot_walkable_tiles_in_range": walkable,
        },
        "available_actions": available_actions,
        "memory": memory_entries,
    }


def parse_llm_response(raw: str) -> Optional[Dict]:
    """Parse LLM JSON response, returning None if invalid."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    if "action" not in data:
        return None
    return data


_openai_client: Optional[OpenAI] = None


def _get_openai_client() -> OpenAI:
    """Return a singleton OpenAI client instance."""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI()
    return _openai_client


def call_openai(system_prompt: str, user_prompt: str) -> Optional[str]:
    """Call OpenAI API and return the response content, or None on failure."""
    try:
        client = _get_openai_client()
        response = client.chat.completions.create(
            model=os.environ.get("EMBERBLAST_MODEL", "gpt-4o-mini"),
            temperature=0.7,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.warning("OpenAI API call failed: %s", e)
        return None
