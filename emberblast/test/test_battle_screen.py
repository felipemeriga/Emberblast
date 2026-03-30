"""Tests for BattleScreen."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.screens.battle import _KEY_TO_ACTION, BattleScreen, TurnHeader
from emberblast.tui.widgets.action_bar import ACTION_KEYS


class TestBattleScreenStructure(BaseTestCase):
    """Verify BattleScreen has the expected class structure."""

    def test_battle_screen_has_compose(self):
        self.assertHasAttr(BattleScreen, "compose")

    def test_battle_screen_has_set_questioner(self):
        self.assertHasAttr(BattleScreen, "set_questioner")

    def test_battle_screen_has_show_actions(self):
        self.assertHasAttr(BattleScreen, "show_actions")

    def test_battle_screen_has_show_choices(self):
        self.assertHasAttr(BattleScreen, "show_choices")

    def test_battle_screen_has_show_confirm(self):
        self.assertHasAttr(BattleScreen, "show_confirm")

    def test_battle_screen_has_on_key(self):
        self.assertHasAttr(BattleScreen, "on_key")

    def test_turn_header_has_set_turn(self):
        self.assertHasAttr(TurnHeader, "set_turn")

    def test_turn_header_has_set_map_name(self):
        self.assertHasAttr(TurnHeader, "set_map_name")


class TestActionKeysCompleteness(BaseTestCase):
    """Verify ACTION_KEYS covers all expected actions and reverse map is consistent."""

    def test_all_action_keys_have_reverse_mapping(self):
        """Every action in ACTION_KEYS should be reachable via _KEY_TO_ACTION."""
        for action, key in ACTION_KEYS.items():
            self.assertIn(key.lower(), _KEY_TO_ACTION)
            self.assertEqual(_KEY_TO_ACTION[key.lower()], action)

    def test_reverse_map_size_matches(self):
        """Reverse map should have same number of entries as ACTION_KEYS (assuming unique keys)."""
        self.assertEqual(len(_KEY_TO_ACTION), len(ACTION_KEYS))

    def test_expected_actions_present(self):
        expected = ["move", "attack", "skill", "defend", "item", "hide", "search", "equip", "drop", "check", "pass"]
        for action in expected:
            self.assertIn(action, ACTION_KEYS, f"Missing action: {action}")
