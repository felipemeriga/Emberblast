"""Tests for the TUI styles module."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.styles import (
    ACTION_COLORS,
    LOG_COLORS,
    TEAM_COLORS,
    TERRAIN_COLORS,
    TERRAIN_SYMBOLS,
    get_player_token,
    get_terrain_cell,
)


class TestTerrainSymbols(BaseTestCase):
    """Tests for terrain symbol constants."""

    def test_all_terrain_types_exist(self):
        expected = {"plains", "wall", "water", "mountain", "forest"}
        self.assertEqual(set(TERRAIN_SYMBOLS.keys()), expected)

    def test_all_symbols_are_two_chars(self):
        for terrain, symbol in TERRAIN_SYMBOLS.items():
            self.assertEqual(len(symbol), 2, f"Symbol for {terrain} should be 2 chars")

    def test_terrain_colors_match_terrain_symbols(self):
        self.assertEqual(set(TERRAIN_COLORS.keys()), set(TERRAIN_SYMBOLS.keys()))


class TestTeamColors(BaseTestCase):
    """Tests for team color constants."""

    def test_friendly_has_fg_and_bg(self):
        self.assertIn("fg", TEAM_COLORS["friendly"])
        self.assertIn("bg", TEAM_COLORS["friendly"])

    def test_enemy_has_fg_and_bg(self):
        self.assertIn("fg", TEAM_COLORS["enemy"])
        self.assertIn("bg", TEAM_COLORS["enemy"])


class TestLogColors(BaseTestCase):
    """Tests for log color constants."""

    def test_all_log_categories_exist(self):
        expected = {
            "damage",
            "heal",
            "narration",
            "move",
            "system",
            "mana",
            "death",
            "xp",
            "item",
        }
        self.assertEqual(set(LOG_COLORS.keys()), expected)


class TestActionColors(BaseTestCase):
    """Tests for action color constants."""

    def test_all_action_types_exist(self):
        expected = {
            "move",
            "attack",
            "skill",
            "defend",
            "item",
            "hide",
            "search",
            "equip",
            "drop",
            "check",
            "pass",
        }
        self.assertEqual(set(ACTION_COLORS.keys()), expected)


class TestGetPlayerToken(BaseTestCase):
    """Tests for get_player_token function."""

    def test_returns_two_char_string(self):
        token = get_player_token("Gandalf", "wizard")
        self.assertEqual(len(token), 2)

    def test_returns_uppercase(self):
        token = get_player_token("gandalf", "wizard")
        self.assertEqual(token, "GW")

    def test_uses_first_chars(self):
        token = get_player_token("Aragorn", "ranger")
        self.assertEqual(token, "AR")


class TestGetTerrainCell(BaseTestCase):
    """Tests for get_terrain_cell function."""

    def test_known_terrain(self):
        self.assertEqual(get_terrain_cell("wall"), "██")

    def test_unknown_terrain_defaults_to_plains(self):
        self.assertEqual(get_terrain_cell("lava"), TERRAIN_SYMBOLS["plains"])

    def test_plains_terrain(self):
        self.assertEqual(get_terrain_cell("plains"), "░░")
