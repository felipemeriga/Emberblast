"""Tests for TitleScreen and GameOverScreen."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.screens.game_over import GameOverScreen
from emberblast.tui.screens.title import LOGO, MENU_ITEMS, TitleScreen


class TestTitleScreenStructure(BaseTestCase):
    """Verify TitleScreen has expected structure."""

    def test_has_compose(self):
        self.assertHasAttr(TitleScreen, "compose")

    def test_has_set_questioner(self):
        self.assertHasAttr(TitleScreen, "set_questioner")

    def test_has_on_key(self):
        self.assertHasAttr(TitleScreen, "on_key")

    def test_logo_is_nonempty_string(self):
        self.assertIsInstance(LOGO, str)
        self.assertGreater(len(LOGO), 0)

    def test_menu_items(self):
        self.assertIn("New Game", MENU_ITEMS)
        self.assertIn("Continue", MENU_ITEMS)
        self.assertIn("Quit", MENU_ITEMS)

    def test_initial_menu_index(self):
        screen = TitleScreen()
        self.assertEqual(screen._menu_index, 0)


class TestGameOverScreenStructure(BaseTestCase):
    """Verify GameOverScreen has expected structure."""

    def test_has_compose(self):
        self.assertHasAttr(GameOverScreen, "compose")

    def test_has_on_key(self):
        self.assertHasAttr(GameOverScreen, "on_key")

    def test_stores_winner_name(self):
        screen = GameOverScreen(winner_name="Alice")
        self.assertEqual(screen._winner_name, "Alice")

    def test_initial_menu_index(self):
        screen = GameOverScreen()
        self.assertEqual(screen._menu_index, 0)
