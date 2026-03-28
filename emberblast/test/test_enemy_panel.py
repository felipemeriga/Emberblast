"""Tests for the EnemyPanelWidget."""

from unittest.mock import MagicMock

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.enemy_panel import EnemyPanelWidget


def _make_enemy(name="Goblin", job_name="Thief", level=3, life=50, health_points=50, alive=True, position=None):
    e = MagicMock()
    e.name = name
    e.job.name = job_name
    e.level = level
    e.life = life
    e.health_points = health_points
    e.is_alive.return_value = alive
    e.position = position or [1, 1]
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

    def test_dead_enemy_shows_dead_label(self):
        self.widget.update_enemies([_make_enemy(name="Skeleton", alive=False)])
        text = self.widget._build_panel_text()
        self.assertIn("DEAD", text.plain)

    def test_empty_list_shows_placeholder(self):
        self.widget.update_enemies([])
        text = self.widget._build_panel_text()
        self.assertIn("No enemies", text.plain)

    def test_single_enemy_renders(self):
        self.widget.update_enemies([_make_enemy(name="Dragon", job_name="Boss")])
        text = self.widget._build_panel_text()
        self.assertIn("Dragon", text.plain)
        self.assertIn("Boss", text.plain)
