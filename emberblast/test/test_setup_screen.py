"""Tests for SetupScreen."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.screens.setup import SetupScreen


class TestSetupScreenStructure(BaseTestCase):
    """Verify SetupScreen has expected structure."""

    def test_has_compose(self):
        self.assertHasAttr(SetupScreen, "compose")

    def test_has_set_questioner(self):
        self.assertHasAttr(SetupScreen, "set_questioner")

    def test_has_show_list(self):
        self.assertHasAttr(SetupScreen, "show_list")

    def test_has_show_input(self):
        self.assertHasAttr(SetupScreen, "show_input")

    def test_has_on_key(self):
        self.assertHasAttr(SetupScreen, "on_key")

    def test_has_on_input_submitted(self):
        self.assertHasAttr(SetupScreen, "on_input_submitted")

    def test_stores_question_type(self):
        screen = SetupScreen(question_type="game_create")
        self.assertEqual(screen._question_type, "game_create")

    def test_default_mode_is_idle(self):
        screen = SetupScreen()
        self.assertEqual(screen._mode, "idle")

    def test_default_question_type_is_empty(self):
        screen = SetupScreen()
        self.assertEqual(screen._question_type, "")
