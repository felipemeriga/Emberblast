"""Tests for the CombatLogWidget."""

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.combat_log import CombatLogWidget


class TestCombatLogWidget(BaseTestCase):
    """Tests for the CombatLogWidget."""

    def setUp(self):
        self.widget = CombatLogWidget(max_entries=5)

    def test_add_entry_stores_message(self):
        self.widget.add_entry("Player attacked!", "damage")
        self.assertEqual(len(self.widget._entries), 1)
        msg, cat, turn = self.widget._entries[0]
        self.assertEqual(msg, "Player attacked!")
        self.assertEqual(cat, "damage")

    def test_max_entries_respected(self):
        for i in range(10):
            self.widget.add_entry(f"Message {i}", "system")
        self.assertEqual(len(self.widget._entries), 5)
        # Oldest entries should be gone, newest should remain
        msg, cat, turn = self.widget._entries[0]
        self.assertEqual(msg, "Message 5")
        self.assertEqual(cat, "system")

    def test_clear_removes_all(self):
        self.widget.add_entry("test", "damage")
        self.widget.add_entry("test2", "heal")
        self.widget.clear_log()
        self.assertEqual(len(self.widget._entries), 0)

    def test_build_text_contains_entries(self):
        self.widget.add_entry("Fireball hits!", "damage")
        self.widget.add_entry("Healed 20 HP", "heal")
        text = self.widget._build_log_text()
        plain = text.plain
        self.assertIn("Fireball hits!", plain)
        self.assertIn("Healed 20 HP", plain)

    def test_empty_log_shows_placeholder(self):
        text = self.widget._build_log_text()
        self.assertIn("Awaiting battle", text.plain)

    def test_narration_entries_present(self):
        self.widget.add_entry("A dark wind blows...", "narration")
        text = self.widget._build_log_text()
        self.assertIn("A dark wind blows...", text.plain)
