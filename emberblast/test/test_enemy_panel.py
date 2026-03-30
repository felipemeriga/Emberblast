"""Tests for the EnemyPanelWidget."""

from unittest.mock import MagicMock

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.enemy_panel import EnemyPanelWidget


def _make_enemy(
    name="Goblin",
    job_name="Thief",
    level=3,
    life=50,
    health_points=50,
    mana=10,
    magic_points=20,
    strength=8,
    intelligence=5,
    armour=3,
    alive=True,
    position=None,
):
    e = MagicMock()
    e.name = name
    e.job.name = job_name
    e.level = level
    e.life = life
    e.health_points = health_points
    e.mana = mana
    e.magic_points = magic_points
    e.strength = strength
    e.intelligence = intelligence
    e.armour = armour
    e.is_alive.return_value = alive
    e.position = position or [1, 1]
    e.side_effects = []
    return e


class TestEnemyPanelWidget(BaseTestCase):
    """Tests for the EnemyPanelWidget."""

    def setUp(self):
        self.widget = EnemyPanelWidget()

    def test_header_appears(self):
        text = self.widget._build_panel_text()
        self.assertIn("ENEMIES", text.plain)

    def test_alive_enemy_shows_name(self):
        self.widget.update_enemies([_make_enemy(name="Orc")])
        text = self.widget._build_panel_text()
        self.assertIn("Orc", text.plain)

    def test_alive_enemy_shows_hp(self):
        self.widget.update_enemies([_make_enemy(life=30, health_points=50)])
        text = self.widget._build_panel_text()
        self.assertIn("30/50", text.plain)

    def test_alive_enemy_shows_mp(self):
        self.widget.update_enemies([_make_enemy(mana=10, magic_points=20)])
        text = self.widget._build_panel_text()
        self.assertIn("10/20", text.plain)

    def test_alive_enemy_shows_stats(self):
        self.widget.update_enemies([_make_enemy(strength=12, intelligence=8, armour=5)])
        text = self.widget._build_panel_text()
        plain = text.plain
        self.assertIn("STR 12", plain)
        self.assertIn("INT 8", plain)
        self.assertIn("ARM 5", plain)

    def test_dead_enemy_shows_dead_label(self):
        self.widget.update_enemies([_make_enemy(name="Skeleton", alive=False)])
        text = self.widget._build_panel_text()
        self.assertIn("DEAD", text.plain)

    def test_empty_list_shows_placeholder(self):
        self.widget.update_enemies([])
        text = self.widget._build_panel_text()
        self.assertIn("No enemies", text.plain)

    def test_alive_count_shown(self):
        enemies = [_make_enemy(name="Orc"), _make_enemy(name="Troll")]
        self.widget.update_enemies(enemies)
        text = self.widget._build_panel_text()
        self.assertIn("2 alive", text.plain)

    def test_single_enemy_renders(self):
        self.widget.update_enemies([_make_enemy(name="Dragon", job_name="Boss")])
        text = self.widget._build_panel_text()
        self.assertIn("Dragon", text.plain)
        self.assertIn("Boss", text.plain)

    def test_cycle_enemy_changes_selection(self):
        enemies = [_make_enemy(name="Orc"), _make_enemy(name="Troll")]
        self.widget.update_enemies(enemies)
        self.assertEqual(self.widget._selected_idx, 0)
        self.widget.cycle_enemy(1)
        self.assertEqual(self.widget._selected_idx, 1)
        self.widget.cycle_enemy(1)
        self.assertEqual(self.widget._selected_idx, 0)  # wraps around
