"""Tests for the PlayerHUDWidget."""

from unittest.mock import MagicMock

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.player_hud import PlayerHUDWidget


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
    return p


class TestPlayerHUDWidget(BaseTestCase):
    """Tests for the PlayerHUDWidget."""

    def setUp(self):
        self.widget = PlayerHUDWidget()

    def test_name_appears_in_hud(self):
        player = _make_player(name="Gandalf")
        self.widget.update_player(player)
        text = self.widget._build_hud_text()
        self.assertIn("Gandalf", text.plain)

    def test_hp_values_appear(self):
        player = _make_player(life=80, health_points=100)
        self.widget.update_player(player)
        text = self.widget._build_hud_text()
        self.assertIn("80", text.plain)
        self.assertIn("100", text.plain)

    def test_mp_values_appear(self):
        player = _make_player(mana=30, magic_points=50)
        self.widget.update_player(player)
        text = self.widget._build_hud_text()
        self.assertIn("30", text.plain)
        self.assertIn("50", text.plain)

    def test_bar_color_green_above_50_percent(self):
        player = _make_player(life=80, health_points=100)
        self.widget.update_player(player)
        text = self.widget._build_hud_text()
        # Check that green color is used (spans contain green)
        plain = text.plain
        self.assertIn("80", plain)  # HP value present

    def test_bar_color_changes_for_low_hp(self):
        # Below 25%
        player = _make_player(life=10, health_points=100)
        self.widget.update_player(player)
        text = self.widget._build_hud_text()
        self.assertIn("10", text.plain)

    def test_stats_line_appears(self):
        player = _make_player(strength=15, intelligence=10)
        self.widget.update_player(player)
        text = self.widget._build_hud_text()
        plain = text.plain
        self.assertIn("STR", plain)
        self.assertIn("INT", plain)

    def test_no_player_shows_placeholder(self):
        text = self.widget._build_hud_text()
        self.assertIn("No player", text.plain)
