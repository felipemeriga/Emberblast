"""Main Textual application for Emberblast."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Coroutine, List, Optional

from textual.app import App

from emberblast.tui.screens.battle import BattleScreen, TurnHeader
from emberblast.tui.screens.game_over import GameOverScreen
from emberblast.tui.screens.title import TitleScreen
from emberblast.tui.widgets.combat_log import CombatLogWidget
from emberblast.tui.widgets.map_grid import MapWidget
from emberblast.tui.widgets.player_hud import PlayerHUDWidget

logger = logging.getLogger(__name__)

# Question method names that route to battle screen
_BATTLE_QUESTIONS = {
    "ask_actions_questions",
    "ask_where_to_move",
    "ask_enemy_to_attack",
    "ask_enemy_to_check",
    "select_skill",
    "select_item",
    "confirm_item_selection",
    "confirm_use_item_on_you",
    "display_equipment_choices",
    "ask_check_action",
    "ask_attributes_to_improve",
}


class EmberblastApp(App):
    """Main Textual app managing screens and bridging the game loop."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._questioner: Any = None
        self._game_task_fn: Optional[Callable[[], Coroutine]] = None
        self._game_task: Optional[asyncio.Task] = None
        self._active_player_name: str = ""
        self._current_turn: int = 0
        self._friendly_names: List[str] = []

    def set_questioner(self, questioner: Any) -> None:
        """Wire the questioner instance."""
        self._questioner = questioner

    def set_game_task(self, coro_fn: Callable[[], Coroutine]) -> None:
        """Store the game coroutine factory to schedule after mount."""
        self._game_task_fn = coro_fn

    async def on_mount(self) -> None:
        """Push the title screen and schedule the game task."""
        title = TitleScreen()
        if self._questioner:
            title.set_questioner(self._questioner)
        await self.push_screen(title)

        if self._game_task_fn:
            self._game_task = asyncio.create_task(self._game_task_fn())

    # ── Bridge methods called by TextualRenderer ──

    def post_combat_log(self, message: str, category: str = "system") -> None:
        """Forward a message to the CombatLogWidget."""
        try:
            log = self.screen.query_one("#combat-log", CombatLogWidget)
            log.add_entry(message, category)
        except Exception:
            logger.debug("CombatLogWidget not available", exc_info=True)

    def refresh_map(self) -> None:
        """Refresh the map widget."""
        try:
            map_w = self.screen.query_one("#map-widget", MapWidget)
            map_w.refresh()
        except Exception:
            logger.debug("MapWidget not available", exc_info=True)

    def refresh_huds(self) -> None:
        """Refresh the player HUD widget."""
        try:
            hud = self.screen.query_one("#player-hud", PlayerHUDWidget)
            hud.refresh()
        except Exception:
            logger.debug("PlayerHUDWidget not available", exc_info=True)

    def update_hud(self, player) -> None:
        """Update the player HUD with actual player data."""
        try:
            hud = self.screen.query_one("#player-hud", PlayerHUDWidget)
            hud.update_player(player)
        except Exception:
            logger.debug("PlayerHUDWidget not available for update", exc_info=True)

    def update_enemies(self, enemies: list) -> None:
        """Update the enemy list in the HUD."""
        try:
            hud = self.screen.query_one("#player-hud", PlayerHUDWidget)
            hud.update_enemies(enemies)
        except Exception:
            logger.debug("PlayerHUDWidget not available for enemy update", exc_info=True)

    def set_turn(self, turn: int) -> None:
        """Update the turn header."""
        self._current_turn = turn
        try:
            header = self.screen.query_one("#turn-header", TurnHeader)
            header.set_turn(turn)
        except Exception:
            logger.debug("TurnHeader not available", exc_info=True)

    def set_map_name(self, name: str) -> None:
        """Set the map name in the turn header."""
        try:
            header = self.screen.query_one("#turn-header", TurnHeader)
            header.set_map_name(name)
        except Exception:
            logger.debug("TurnHeader not available for map name", exc_info=True)

    def set_active_player(self, player_name: str) -> None:
        """Store the currently active player name."""
        self._active_player_name = player_name

    def update_map_from_event(
        self,
        player: Any,
        enemies: list,
        matrix: list,
        size: int,
    ) -> None:
        """Update the MapWidget with event data."""
        try:
            screen = self.screen
            map_w = screen.query_one("#map-widget", MapWidget)
            all_players = [player] + list(enemies)
            map_w.update_map(
                matrix=matrix,
                size=size,
                players=all_players,
                active_player_name=self._active_player_name,
                friendly_names=set(self._friendly_names),
            )
        except Exception:
            logger.debug("MapWidget not available for event update", exc_info=True)

    def show_move_highlights(
        self,
        position: str,
        possibilities: list,
        matrix: list,
        size: int,
    ) -> None:
        """Highlight possible movement cells on the map."""
        try:
            map_w = self.screen.query_one("#map-widget", MapWidget)
            map_w._highlight_cells = set(possibilities)
            map_w.refresh()
        except Exception:
            logger.debug("MapWidget not available for highlights", exc_info=True)

    def show_game_over(self, winner_name: str) -> None:
        """Push the game over screen."""
        screen = GameOverScreen(winner_name=winner_name)
        self.push_screen(screen)

    # ── Screen transition ──

    def switch_to_battle(self, friendly_names: List[str]) -> None:
        """Transition from setup to the battle screen."""
        self._friendly_names = list(friendly_names)
        # Pop the TitleScreen (and any setup screens) so BattleScreen becomes
        # the active screen and widget queries resolve correctly.
        while len(self.screen_stack) > 1:
            self.pop_screen()
        battle = BattleScreen(friendly_names=friendly_names)
        if self._questioner:
            battle.set_questioner(self._questioner)
        self.push_screen(battle)

    # ── Highlight helpers ──

    def _show_movement_highlights(self, possibilities: list) -> None:
        """Highlight possible movement cells on the map."""
        try:
            map_w = self.screen.query_one("#map-widget", MapWidget)
            map_w._highlight_cells = set(possibilities)
            map_w.refresh()
        except Exception:
            logger.debug("MapWidget not available for movement highlights", exc_info=True)

    def clear_highlights(self) -> None:
        """Clear all highlight and flash cells on the map."""
        try:
            map_w = self.screen.query_one("#map-widget", MapWidget)
            map_w._highlight_cells = set()
            map_w._flash_cells = set()
            map_w.refresh()
        except Exception:
            logger.debug("MapWidget not available for clearing highlights", exc_info=True)

    # ── Question routing ──

    def handle_question(self, method_name: str, **kwargs) -> None:
        """Route a question from the questioner to the appropriate screen.

        Note: perform_game_create_questions, perform_character_creation_questions,
        and get_saved_game are handled directly by TextualQuestioner using
        _ask_setup_list/_ask_setup_input, so they don't route through here.
        """
        if method_name == "perform_first_question":
            self._handle_title_question(method_name, **kwargs)
        elif method_name in _BATTLE_QUESTIONS:
            self._handle_battle_question(method_name, **kwargs)

    def _handle_title_question(self, method_name: str, **kwargs) -> None:
        """Forward question to the TitleScreen."""
        try:
            screen = self.screen
            if isinstance(screen, TitleScreen) and self._questioner:
                screen.set_questioner(self._questioner)
        except Exception:
            logger.debug("TitleScreen not available", exc_info=True)

    def _handle_battle_question(self, method_name: str, **kwargs) -> None:
        """Forward question to the current BattleScreen."""
        try:
            screen = self.screen
            if not isinstance(screen, BattleScreen):
                return

            if method_name == "ask_actions_questions":
                actions = kwargs.get("actions_available", [])
                screen.show_actions(actions)
            elif method_name == "ask_where_to_move":
                possibilities = kwargs.get("possibilities", [])
                # Highlight movement cells on the map
                self._show_movement_highlights(possibilities)
                screen.show_choices(method_name, possibilities, possibilities)
            elif method_name in ("ask_enemy_to_attack", "ask_enemy_to_check"):
                enemies = kwargs.get("enemies", [])
                labels = [f"{e.name} (HP:{e.life})" if hasattr(e, "life") else str(e) for e in enemies]
                screen.show_choices(method_name, enemies, labels)
            elif method_name == "select_skill":
                skills = kwargs.get("available_skills", [])
                labels = [f"{s.name} (MP:{s.mana_cost})" if hasattr(s, "mana_cost") else str(s) for s in skills]
                screen.show_choices(method_name, skills, labels)
            elif method_name == "select_item":
                items = kwargs.get("items", [])
                labels = [f"{i.name}" if hasattr(i, "name") else str(i) for i in items]
                screen.show_choices(method_name, items, labels)
            elif method_name in ("confirm_item_selection", "confirm_use_item_on_you"):
                screen.show_confirm(method_name, "Are you sure?")
            elif method_name == "display_equipment_choices":
                player = kwargs.get("player")
                if player and hasattr(player, "bag"):
                    equips = player.bag.get_equipments()
                    labels = [f"{e.name}" if hasattr(e, "name") else str(e) for e in equips]
                    equips_with_cancel = list(equips) + [None]
                    labels_with_cancel = labels + ["Cancel"]
                    screen.show_choices(method_name, equips_with_cancel, labels_with_cancel)
            elif method_name == "ask_check_action":
                show_items = kwargs.get("show_items", False)
                choices = ["map", "status", "enemy"]
                labels = ["Map and Enemies", "My Status", "Single Enemy"]
                if show_items:
                    choices.append("item")
                    labels.append("My Items")
                choices.append("cancel")
                labels.append("Cancel")
                screen.show_choices(method_name, choices, labels)
            elif method_name == "ask_attributes_to_improve":
                attrs = ["strength", "intelligence", "accuracy", "armour", "magic_resist", "will"]
                screen.show_choices(method_name, attrs, attrs)
        except Exception:
            logger.debug("Battle question handling failed", exc_info=True)
