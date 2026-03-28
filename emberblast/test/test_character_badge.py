"""Tests for the CharacterBadgeWidget."""

from unittest.mock import MagicMock

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.character_badge import CharacterBadgeWidget


def _make_player(
    name="Hero",
    job_name="Warrior",
    race_name="Human",
    level=5,
    life=80,
    health_points=100,
    mana=30,
    magic_points=50,
    strength=15,
    intelligence=10,
    accuracy=12,
    armour=8,
    magic_resist=6,
    move_speed=3,
    will=7,
    position=None,
):
    p = MagicMock()
    p.name = name
    p.job.name = job_name
    p.race.name = race_name
    p.level = level
    p.life = life
    p.health_points = health_points
    p.mana = mana
    p.magic_points = magic_points
    p.strength = strength
    p.intelligence = intelligence
    p.accuracy = accuracy
    p.armour = armour
    p.magic_resist = magic_resist
    p.move_speed = move_speed
    p.will = will
    p.position = position or [0, 0]
    p.side_effects = []
    return p


class TestCharacterBadgeWidget(BaseTestCase):
    """Tests for the CharacterBadgeWidget."""

    def setUp(self):
        self.widget = CharacterBadgeWidget()

    def test_name_appears(self):
        player = _make_player(name="Gandalf")
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        self.assertIn("Gandalf", text.plain)

    def test_job_and_race_appear(self):
        player = _make_player(job_name="Wizard", race_name="Elf")
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        self.assertIn("Wizard", text.plain)
        self.assertIn("Elf", text.plain)

    def test_level_appears(self):
        player = _make_player(level=7)
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        self.assertIn("Lv.7", text.plain)

    def test_hp_values_appear(self):
        player = _make_player(life=80, health_points=100)
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        self.assertIn("80", text.plain)
        self.assertIn("100", text.plain)

    def test_mp_values_appear(self):
        player = _make_player(mana=30, magic_points=50)
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        self.assertIn("30", text.plain)
        self.assertIn("50", text.plain)

    def test_all_stats_appear(self):
        player = _make_player()
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        plain = text.plain
        for stat in ("STR", "INT", "ACC", "ARM", "RES", "SPD", "WILL"):
            self.assertIn(stat, plain)

    def test_no_player_shows_placeholder(self):
        text = self.widget._build_badge_text()
        self.assertIn("No player", text.plain)

    def test_zero_hp_renders(self):
        player = _make_player(life=0, health_points=100)
        self.widget.update_player(player)
        text = self.widget._build_badge_text()
        self.assertIn("0/100", text.plain)
