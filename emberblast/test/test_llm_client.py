import json
from unittest.mock import MagicMock, patch

from emberblast.bot.llm_client import (
    JOB_TRAITS,
    RACE_MODIFIERS,
    build_personality_prompt,
    call_openai,
    parse_llm_response,
    serialize_game_state,
)
from emberblast.test.test import BaseTestCase


class TestPersonalityPrompt(BaseTestCase):
    def test_build_personality_known_job_race(self):
        prompt = build_personality_prompt("Grukk", "Knight", "Orc")
        self.assertIn("Grukk", prompt)
        self.assertIn("Orc", prompt)
        self.assertIn("Knight", prompt)
        self.assertIn(JOB_TRAITS["Knight"], prompt)
        self.assertIn(RACE_MODIFIERS["Orc"], prompt)

    def test_build_personality_unknown_job(self):
        prompt = build_personality_prompt("Test", "UnknownJob", "Human")
        self.assertIn("Test", prompt)
        self.assertIn("UnknownJob", prompt)

    def test_all_jobs_have_traits(self):
        for job in ["Knight", "Wizard", "Rogue", "Archer", "Priest"]:
            self.assertIn(job, JOB_TRAITS)

    def test_all_races_have_modifiers(self):
        for race in ["Human", "Dwarf", "Elf", "Orc", "Halflings"]:
            self.assertIn(race, RACE_MODIFIERS)


class TestSerializeGameState(BaseTestCase):
    def _make_mock_player(
        self,
        name="Grukk",
        job_name="Knight",
        race_name="Orc",
        position="C4",
        life=45,
        health_points=80,
        mana=10,
        magic_points=20,
        level=3,
        attack_type="melee",
        damage_vector="strength",
    ):
        player = MagicMock()
        player.name = name
        player.position = position
        player.life = life
        player.health_points = health_points
        player.mana = mana
        player.magic_points = magic_points
        player.level = level
        player.strength = 12
        player.intelligence = 4
        player.accuracy = 6
        player.armour = 10
        player.magic_resist = 3
        player.move_speed = 3
        player.will = 5
        player.job = MagicMock()
        player.job.get_name.return_value = job_name
        player.job.attack_type = attack_type
        player.job.damage_vector = damage_vector
        player.race = MagicMock()
        player.race.get_name.return_value = race_name
        player.skills = []
        player.bag = MagicMock()
        player.bag.items = []
        player.equipment = MagicMock()
        player.equipment.weapon = None
        player.equipment.armour = None
        player.equipment.boots = None
        player.equipment.accessory = None
        player.side_effects = []
        player.is_hidden.return_value = False
        return player

    def test_serialize_basic_state(self):
        bot = self._make_mock_player()
        enemies = [
            self._make_mock_player(
                name="Elara",
                job_name="Wizard",
                position="F7",
                life=30,
                health_points=50,
            )
        ]

        game = MagicMock()
        game.game_map.graph.get_available_nodes_in_range.return_value = ["C3", "C5"]
        game.game_map.graph.get_shortest_distance_between_positions.return_value = 4.0

        memory_entries = ["Turn 1: Moved to C4"]

        state = serialize_game_state(
            bot,
            enemies,
            game,
            memory_entries,
            ["move", "attack", "pass"],
        )
        self.assertEqual(state["current_bot"]["name"], "Grukk")
        self.assertEqual(state["current_bot"]["job"], "Knight")
        self.assertEqual(len(state["enemies"]), 1)
        self.assertEqual(state["enemies"][0]["name"], "Elara")
        self.assertEqual(state["memory"], ["Turn 1: Moved to C4"])
        self.assertIn("move", state["available_actions"])

    def test_serialize_with_skills(self):
        bot = self._make_mock_player()
        skill = MagicMock()
        skill.name = "Shield Bash"
        skill.base = 15
        skill.cost = 8
        skill.ranged = 1
        skill.kind = "inflict"
        bot.skills = [skill]
        bot.mana = 10

        state = serialize_game_state(bot, [], MagicMock(), [], ["attack"])
        self.assertEqual(len(state["current_bot"]["available_skills"]), 1)
        self.assertEqual(
            state["current_bot"]["available_skills"][0]["name"],
            "Shield Bash",
        )


class TestParseLLMResponse(BaseTestCase):
    def test_parse_valid_response(self):
        response = json.dumps(
            {
                "action": "attack",
                "target": "Elara",
                "narration": "Die, wizard!",
            }
        )
        result = parse_llm_response(response)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["target"], "Elara")
        self.assertEqual(result["narration"], "Die, wizard!")

    def test_parse_invalid_json(self):
        result = parse_llm_response("not json")
        self.assertIsNone(result)

    def test_parse_missing_action(self):
        response = json.dumps({"target": "Elara", "narration": "hi"})
        result = parse_llm_response(response)
        self.assertIsNone(result)


class TestCallOpenAI(BaseTestCase):
    @patch("emberblast.bot.llm_client.OpenAI")
    def test_call_openai_success(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"action": "attack", "target": "Elara", "narration": "Die!"}'
        mock_client.chat.completions.create.return_value = mock_response

        result = call_openai("system prompt", "user prompt")
        self.assertIn("attack", result)

    @patch("emberblast.bot.llm_client.OpenAI")
    def test_call_openai_failure(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        result = call_openai("system prompt", "user prompt")
        self.assertIsNone(result)
