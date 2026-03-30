"""Tests for the CombatLogWidget."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.combat_log import CombatLogWidget


class TestCombatLogWidget(BaseTestCase):
    """Tests for the CombatLogWidget."""

    def test_widget_is_rich_log(self):
        from textual.widgets import RichLog

        widget = CombatLogWidget()
        self.assertIsInstance(widget, RichLog)

    def test_set_turn_stores_value(self):
        widget = CombatLogWidget()
        widget.set_turn(3)
        self.assertEqual(widget._current_turn, 3)

    def test_has_add_entry(self):
        widget = CombatLogWidget()
        self.assertTrue(callable(getattr(widget, "add_entry", None)))

    def test_has_clear_log(self):
        widget = CombatLogWidget()
        self.assertTrue(callable(getattr(widget, "clear_log", None)))

    def test_auto_scroll_enabled(self):
        widget = CombatLogWidget()
        self.assertTrue(widget.auto_scroll)
