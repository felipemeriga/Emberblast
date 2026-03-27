# LLM-Powered Bot AI & UI Modernization for Emberblast

## Overview

Two major changes to Emberblast:

1. **LLM-Powered Bots** — Replace deterministic bot decision-making with OpenAI LLM-powered decisions. Each bot gets a personality derived from its job/race combo, reasons about game state with memory of recent turns, and outputs both an action and an in-character narration line.

2. **UI Modernization & Event System** — Replace the old terminal output stack (`colorama`/`termcolor`/`emojis`/`timg`) with Rich, and introduce a structured game event system with a renderer pattern. This makes the CLI experience beautiful now and sets up a clean path to a future Discord backend.

## Goals

- Make bot behavior non-deterministic, strategic, and emergent
- Give each bot a distinct personality that influences decisions
- Add narration to make the game feel alive
- Modernize terminal output with Rich (panels, tables, colors, formatting)
- Introduce typed game events + renderer pattern for multi-backend support (CLI now, Discord later)
- Graceful fallback to deterministic logic on API failure
- Migrate project tooling from pip/setuptools to uv

## Decisions Made

- **LLM Provider**: OpenAI (GPT-4o-mini)
- **Approach**: Direct replacement inside `BotDecisioning.decide()`
- **All bots** use LLM (no mixed mode)
- **Personality + narration** per turn
- **Full game state + memory summary** sent each turn
- **API key** via `OPENAI_API_KEY` environment variable
- **Fallback**: retry once, then deterministic logic, log warning
- **UI library**: Rich (replaces colorama, termcolor, emojis, timg)
- **Event architecture**: Typed event objects + renderer pattern (game emits events, active renderer displays them)
- **Package manager**: uv (replaces pip/setuptools)

---

## Part 1: LLM-Powered Bots

### Section 1: Game State Serialization

Each bot turn, build a JSON payload from existing game objects:

```json
{
  "current_bot": {
    "name": "Grukk",
    "job": "Knight",
    "race": "Orc",
    "level": 3,
    "position": "C4",
    "life": 45,
    "max_life": 80,
    "mana": 10,
    "max_mana": 20,
    "attributes": {
      "strength": 12,
      "intelligence": 4,
      "accuracy": 6,
      "armour": 10,
      "magic_resist": 3,
      "move_speed": 3
    },
    "available_skills": [
      { "name": "Shield Bash", "damage": 15, "mana_cost": 8, "range": 1 }
    ],
    "bag_items": [
      { "name": "Healing Potion", "type": "healing", "value": 25 }
    ],
    "equipment": {
      "weapon": "Iron Sword",
      "armor": "Chain Mail"
    },
    "active_effects": [
      { "name": "Poisoned", "turns_remaining": 2, "effect": "-5 HP/turn" }
    ]
  },
  "enemies": [
    {
      "name": "Elara",
      "job": "Wizard",
      "position": "F7",
      "life": 30,
      "max_life": 50,
      "distance": 4,
      "visible": true
    }
  ],
  "map": {
    "size": "8x8",
    "bot_walkable_tiles_in_range": ["C3", "C5", "D4", "D3", "B4", "B3"],
    "obstacles_nearby": ["C6", "D6"]
  },
  "available_actions": [
    "move", "attack", "skill", "item", "defend", "hide",
    "search", "equip", "pass"
  ],
  "memory": [
    "Turn 3: Elara hit you with Fireball for 20 damage",
    "Turn 4: You found a Healing Potion at D5",
    "Turn 5: You attacked Elara for 12 damage"
  ]
}
```

Built inside `BotDecisioning` from existing game objects. No new data structures needed.

### Section 2: Personality System

Each bot gets a system prompt built from job + race:

**Template:**

```
You are {name}, a {race} {job} in a tactical RPG deathmatch.

Personality: {personality_trait}

You must choose one action per turn. Respond in JSON format with:
- "action": the action type
- "target": target player name or position (if applicable)
- "skill_name": skill to use (if action is "skill")
- "item_name": item to use (if action is "item")
- "move_to": destination tile (if action is "move")
- "narration": a short in-character line (1 sentence, spoken aloud)
```

**Job base traits:**

| Job     | Trait                                              |
|---------|----------------------------------------------------|
| Knight  | Honorable, charges into battle, protects the weak  |
| Wizard  | Calculating, intellectual, positions carefully      |
| Rogue   | Opportunistic, sneaky, avoids fair fights           |
| Archer  | Patient, methodical, keeps distance                 |
| Priest  | Cautious, wise, reluctant combatant                 |

**Race modifiers:**

| Race      | Tone modifier                              |
|-----------|--------------------------------------------|
| Orc       | More aggressive, blunt, trash-talks        |
| Elf       | Eloquent, condescending, precise           |
| Dwarf     | Grumpy, stubborn, dry humor                |
| Halfling  | Nervous, scrappy, underdog energy          |
| Human     | Balanced, adaptable, practical             |

Example — Orc Knight: *"Brutal and honorable. You charge headfirst into battle and respect strength above all. You trash-talk your enemies but fight fair."*

Example — Elf Rogue: *"Elegant and deadly. You consider direct combat beneath you. You strike from the shadows with surgical precision and mock those too slow to see you coming."*

### Section 3: LLM Integration & Action Parsing

**Flow inside `BotDecisioning.decide()`:**

1. Build game state JSON (Section 1)
2. Build personality system prompt (Section 2)
3. Call OpenAI API:
   - Model: `gpt-4o-mini`
   - Temperature: `0.7`
   - `response_format: { "type": "json_object" }` for guaranteed valid JSON
4. Parse response JSON into action + target + narration
5. Validate action against game rules (legal move, target in range, enough mana, etc.)
6. If valid: execute via existing game methods, emit narration event
7. If invalid: retry once with error feedback appended ("That action was invalid because: {reason}. Choose again.")
8. If still invalid or API error: fall back to old deterministic logic, log warning

**New dependency:** `openai` Python package.

**API key:** Read from `OPENAI_API_KEY` env var at game start. If missing, print error and exit.

**Token budget:** ~1000 tokens input, ~50-80 tokens output per turn. At GPT-4o-mini pricing, ~$0.0001 per bot turn.

### Section 4: Memory System

Per-bot rolling history stored as a list of strings:

- After each turn, append: `"Turn {n}: {what happened}"`
- Events tracked: attacks given/received, damage dealt/taken, items found/used, skills used, kills, movement
- Rolling window of **last 10 entries** per bot
- Memory lives in-memory for the game duration
- Serializable via existing `cloudpickle` save system

---

## Part 2: UI Modernization & Event System

### Section 5: Typed Game Events

Replace direct method calls on `IInformingSystem` with typed event objects. The game engine produces events; renderers consume them.

**Event dataclasses** (new module `emberblast/events/`):

```python
@dataclass
class GameEvent:
    """Base class for all game events."""
    pass

@dataclass
class TurnStartEvent(GameEvent):
    turn: int

@dataclass
class PlayerTurnEvent(GameEvent):
    player_name: str

@dataclass
class MoveEvent(GameEvent):
    player_name: str
    from_position: str
    to_position: str

@dataclass
class DamageEvent(GameEvent):
    attacker_name: str
    target_name: str
    damage: int
    target_alive: bool
    target_life: int

@dataclass
class HealEvent(GameEvent):
    healer_name: str
    target_name: str
    amount: int
    target_life: int

@dataclass
class SkillEvent(GameEvent):
    caster_name: str
    skill_name: str
    mana_cost: int

@dataclass
class ItemEvent(GameEvent):
    player_name: str
    item_name: str
    target_name: str

@dataclass
class DiceRollEvent(GameEvent):
    player_name: str
    result: int
    kind: str
    is_critical: bool

@dataclass
class NarrationEvent(GameEvent):
    player_name: str
    text: str

@dataclass
class DeathEvent(GameEvent):
    player_name: str

@dataclass
class VictoryEvent(GameEvent):
    player_name: str

@dataclass
class SideEffectEvent(GameEvent):
    player_name: str
    effect_name: str
    effect_type: str  # "buff", "debuff", "inflicted"

@dataclass
class MapInfoEvent(GameEvent):
    current_player: IPlayer
    enemies: List[IPlayer]
    matrix: List[List[int]]
    size: int

@dataclass
class ItemFoundEvent(GameEvent):
    player_name: str
    found: bool
    item_name: str = None
    item_tier: str = None

@dataclass
class LevelUpEvent(GameEvent):
    player_name: str
    new_level: int

@dataclass
class XPEarnedEvent(GameEvent):
    player_name: str
    xp: int
    kill_target: str = None  # if XP was from a kill
```

One event class per distinct thing that happens in the game. Events are pure data — no rendering logic.

### Section 6: Renderer Interface & Rich CLI Renderer

**New `IRenderer` interface** (replaces `IInformingSystem`):

```python
class IRenderer(ABC):
    @abstractmethod
    def render(self, event: GameEvent) -> None:
        """Render a game event to the output backend."""
        pass

    @abstractmethod
    def render_map(self, event: MapInfoEvent) -> None:
        """Render the game map (special case — complex layout)."""
        pass

    @abstractmethod
    def prompt_action(self, actions: List[str]) -> str:
        """Get player input for action selection."""
        pass
```

**`RichCLIRenderer`** implements `IRenderer` using Rich:

- `TurnStartEvent` → Rich Panel with turn number, styled header
- `DamageEvent` → Rich colored text (red for damage, with attacker/target names)
- `NarrationEvent` → Rich Panel with bot name as title, italic narration text
- `MapInfoEvent` → Rich Table for the grid, colored cells for players/enemies/obstacles
- `VictoryEvent` → Rich Panel with celebration styling
- `DiceRollEvent` → Styled text, bold for criticals
- Player prompts → Rich-styled `InquirerPy` prompts (InquirerPy works fine with Rich)

**Migration path:**
- `InformerCMD` methods get replaced by `RichCLIRenderer.render()` dispatch
- `QuestionerCMD` stays mostly as-is but uses Rich for formatting the prompt text
- The `ICommunicator` wrapper still exists but delegates to `IRenderer` + `IQuestioningSystem`

### Section 7: Renderer Dispatch

The renderer uses a dispatch dict mapping event types to render methods:

```python
class RichCLIRenderer(IRenderer):
    def __init__(self):
        self.console = Console()
        self._dispatch = {
            TurnStartEvent: self._render_turn_start,
            DamageEvent: self._render_damage,
            NarrationEvent: self._render_narration,
            # ... etc
        }

    def render(self, event: GameEvent) -> None:
        handler = self._dispatch.get(type(event))
        if handler:
            handler(event)
```

This means adding a Discord renderer later is just: create `DiscordRenderer` with its own `_dispatch` mapping the same events to Discord embeds/messages.

### Section 8: Rich Output Examples

**Turn header:**
```
╭─────────────────────────────────╮
│  Turn 5 — Embrace Yourselves!  │
╰─────────────────────────────────╯
```

**Bot narration:**
```
╭─ Grukk (Orc Knight) ───────────────────╮
│ "You think you can hide from me?"       │
╰─────────────────────────────────────────╯
  ⚔ Grukk attacked Elara for 15 damage
  💚 Elara now has 35 HP
```

**Map display:**
```
╭─ Millstone Plains ─────────────────────╮
│     0   1   2   3   4   5   6   7      │
│ A   ·   ·   ·   ■   ·   ·   ·   ·     │
│ B   ·   ·   ·   ■   ·   ·   ·   ·     │
│ C   ·   ·   ·   ·  [G]  ·   ·   ·     │  <- Green for current player
│ D   ·   ·   ·   ·   ·   ·   ·   ·     │
│ E   ·   ·   ·   ·   ·   ·   ·   ·     │
│ F   ·   ·   ·   ·   ·   ·  [E]  ·     │  <- Red for enemies
│ G   ·   ■   ■   ·   ·   ·   ·   ·     │
│ H   ·   ·   ·   ·   ·   ·   ·   ·     │
╰────────────────────────────────────────╯
```

**Player stats:**
```
╭─ Grukk (Orc Knight) Lv.3 ─────────────╮
│ ❤ Life: 45/80    💧 Mana: 10/20       │
│ 💪 STR: 12  🧠 INT: 4   🎯 ACC: 6    │
│ 🛡 ARM: 10  🌀 RES: 3   👟 SPD: 3    │
╰────────────────────────────────────────╯
```

---

## Part 3: Project Tooling

### Section 9: uv Migration

- Create `pyproject.toml` migrating metadata from `setup.cfg` and `setup.py`
- Add new dependencies: `openai`, `rich`
- Remove old dependencies: `colorama`, `termcolor`, `emojis`, `timg`
- Keep `InquirerPy` (still needed for interactive prompts)
- Remove `setup.cfg` and `setup.py`
- Update `__main__.py` to remove pip install helper
- Add `.python-version` file

---

## Files to Create

- `emberblast/events/__init__.py` — typed event dataclasses
- `emberblast/events/events.py` — all GameEvent subclasses
- `emberblast/renderer/__init__.py` — renderer module
- `emberblast/renderer/interface.py` — `IRenderer` abstract class
- `emberblast/renderer/rich_cli.py` — `RichCLIRenderer` implementation
- `pyproject.toml` — replaces setup.cfg/setup.py
- `.python-version` — Python version pin for uv

## Files to Modify

- `emberblast/bot/bot_decisioning.py` — add LLM call, game state serialization, personality prompts, memory, fallback logic
- `emberblast/orchestrator/game_orchestrator.py` — emit typed events instead of calling informer methods directly, capture turn events for bot memory
- `emberblast/interface/interface.py` — add `IRenderer` interface, keep `IQuestioningSystem`
- `emberblast/communicator/questioner_cmd.py` — update formatting to use Rich for prompt text
- `emberblast/__main__.py` — API key check at startup, remove pip helper

## Files to Remove

- `emberblast/communicator/informer_cmd.py` — replaced by `RichCLIRenderer`
- `setup.cfg` — replaced by `pyproject.toml`
- `setup.py` — replaced by `pyproject.toml`

## Out of Scope

- Discord renderer (future work — the event system enables it)
- Multiple LLM providers / provider abstraction
- Per-bot LLM vs deterministic configuration
- Persistent memory across games
- Fine-tuning or training
- Fog of war / partial information
