from emberblast.bot.memory import BotMemory
from emberblast.test.test import BaseTestCase


class TestBotMemory(BaseTestCase):
    def setUp(self):
        self.memory = BotMemory(max_entries=10)

    def test_add_entry(self):
        self.memory.add(1, "Attacked Elara for 15 damage")
        entries = self.memory.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], "Turn 1: Attacked Elara for 15 damage")

    def test_rolling_window(self):
        for i in range(15):
            self.memory.add(i, f"Event {i}")
        entries = self.memory.get_entries()
        self.assertEqual(len(entries), 10)
        self.assertEqual(entries[0], "Turn 5: Event 5")
        self.assertEqual(entries[9], "Turn 14: Event 14")

    def test_empty_memory(self):
        entries = self.memory.get_entries()
        self.assertEqual(entries, [])

    def test_custom_max_entries(self):
        small_memory = BotMemory(max_entries=3)
        for i in range(5):
            small_memory.add(i, f"Event {i}")
        entries = small_memory.get_entries()
        self.assertEqual(len(entries), 3)

    def test_clear(self):
        self.memory.add(1, "test")
        self.memory.clear()
        self.assertEqual(self.memory.get_entries(), [])
