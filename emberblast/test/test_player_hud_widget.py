"""Tests for the PlayerHUDWidget (now CharacterBadgeWidget + EnemyPanelWidget).

This file is kept for backward compatibility — the actual widget tests
are in test_character_badge.py and test_enemy_panel.py.
"""

from emberblast.test.test import BaseTestCase
from emberblast.tui.widgets.character_badge import CharacterBadgeWidget
from emberblast.tui.widgets.enemy_panel import EnemyPanelWidget


class TestPlayerHUDWidgetMigration(BaseTestCase):
    """Verify the old PlayerHUDWidget was replaced by new widgets."""

    def test_character_badge_exists(self):
        widget = CharacterBadgeWidget()
        self.assertTrue(callable(getattr(widget, "update_player", None)))

    def test_enemy_panel_exists(self):
        widget = EnemyPanelWidget()
        self.assertTrue(callable(getattr(widget, "update_enemies", None)))
