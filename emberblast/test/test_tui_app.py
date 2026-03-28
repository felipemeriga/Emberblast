"""Tests for EmberblastApp."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.app import EmberblastApp


class TestEmberblastAppStructure(BaseTestCase):
    """Verify EmberblastApp has all required methods."""

    def test_has_set_questioner(self):
        self.assertHasAttr(EmberblastApp, "set_questioner")

    def test_has_set_game_task(self):
        self.assertHasAttr(EmberblastApp, "set_game_task")

    def test_has_on_mount(self):
        self.assertHasAttr(EmberblastApp, "on_mount")

    def test_has_post_combat_log(self):
        self.assertHasAttr(EmberblastApp, "post_combat_log")

    def test_has_refresh_map(self):
        self.assertHasAttr(EmberblastApp, "refresh_map")

    def test_has_refresh_huds(self):
        self.assertHasAttr(EmberblastApp, "refresh_huds")

    def test_has_set_turn(self):
        self.assertHasAttr(EmberblastApp, "set_turn")

    def test_has_set_active_player(self):
        self.assertHasAttr(EmberblastApp, "set_active_player")

    def test_has_update_map_from_event(self):
        self.assertHasAttr(EmberblastApp, "update_map_from_event")

    def test_has_show_move_highlights(self):
        self.assertHasAttr(EmberblastApp, "show_move_highlights")

    def test_has_show_game_over(self):
        self.assertHasAttr(EmberblastApp, "show_game_over")

    def test_has_handle_question(self):
        self.assertHasAttr(EmberblastApp, "handle_question")

    def test_has_switch_to_battle(self):
        self.assertHasAttr(EmberblastApp, "switch_to_battle")

    def test_has_update_hud(self):
        self.assertHasAttr(EmberblastApp, "update_hud")

    def test_has_update_enemies(self):
        self.assertHasAttr(EmberblastApp, "update_enemies")

    def test_default_state(self):
        app = EmberblastApp()
        self.assertEqual(app._active_player_name, "")
        self.assertEqual(app._current_turn, 0)
        self.assertIsNone(app._questioner)
        self.assertIsNone(app._game_task_fn)
        self.assertEqual(app._friendly_names, [])
