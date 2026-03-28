"""Tests for the ActionBar widget."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.action_bar import ActionBarWidget


class TestActionBarWidget(BaseTestCase):
    """Tests for the ActionBar widget."""

    def setUp(self):
        self.widget = ActionBarWidget()

    def test_set_actions_stores_actions(self):
        self.widget.set_actions(["move", "attack", "defend"])
        self.assertEqual(self.widget._actions, ["move", "attack", "defend"])

    def test_set_status_stores_text(self):
        self.widget.set_status("Waiting for input...")
        self.assertEqual(self.widget._status, "Waiting for input...")

    def test_build_bar_text_contains_keys(self):
        self.widget.set_actions(["move", "attack", "skill"])
        text = self.widget._build_bar_text()
        plain = text.plain
        self.assertIn("[M]", plain)
        self.assertIn("[A]", plain)
        self.assertIn("[S]", plain)

    def test_build_bar_text_contains_action_names(self):
        self.widget.set_actions(["move", "attack"])
        text = self.widget._build_bar_text()
        plain = text.plain
        self.assertIn("ove", plain)  # [M]ove
        self.assertIn("ttack", plain)  # [A]ttack

    def test_clear_resets_state(self):
        self.widget.set_actions(["move", "attack"])
        self.widget.set_status("Some status")
        self.widget.clear()
        self.assertEqual(self.widget._actions, [])
        self.assertEqual(self.widget._status, "")

    def test_status_appears_in_bar(self):
        self.widget.set_status("Enemy turn...")
        text = self.widget._build_bar_text()
        self.assertIn("Enemy turn...", text.plain)

    def test_empty_actions_shows_status_only(self):
        self.widget.set_status("Waiting...")
        text = self.widget._build_bar_text()
        self.assertIn("Waiting...", text.plain)

    def test_bordered_buttons_have_box_chars(self):
        self.widget.set_actions(["move"])
        text = self.widget._build_bar_text()
        plain = text.plain
        self.assertIn("\u250c", plain)  # top-left corner
        self.assertIn("\u2518", plain)  # bottom-right corner
