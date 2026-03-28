"""Battle screen composing map, HUD, combat log, and action bar."""

from __future__ import annotations

from typing import Any, List, Optional

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static

from emberblast.tui.widgets.action_bar import ACTION_KEYS, ActionBarWidget
from emberblast.tui.widgets.character_badge import CharacterBadgeWidget
from emberblast.tui.widgets.combat_log import CombatLogWidget
from emberblast.tui.widgets.enemy_panel import EnemyPanelWidget
from emberblast.tui.widgets.map_grid import MapWidget

# Reverse lookup: key letter -> action name
_KEY_TO_ACTION = {v.lower(): k for k, v in ACTION_KEYS.items()}


class TurnHeader(Static):
    """Displays current turn number and map name."""

    DEFAULT_CSS = """
    TurnHeader {
        dock: top;
        height: 3;
        background: #0d1117;
        color: #f0883e;
        text-style: bold;
        content-align: center middle;
        border: tall #f0883e;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("", **kwargs)
        self._turn: int = 0
        self._map_name: str = ""

    def set_turn(self, turn: int) -> None:
        self._turn = turn
        self._refresh_text()

    def set_map_name(self, name: str) -> None:
        self._map_name = name
        self._refresh_text()

    def _refresh_text(self) -> None:
        label = f"\u2694 TURN {self._turn}"
        if self._map_name:
            label += f"  {self._map_name}"
        self.update(label)


class BattleScreen(Screen):
    """Main battle screen with classic RPG layout."""

    DEFAULT_CSS = """
    BattleScreen {
        background: #0d1117;
    }
    BattleScreen > Horizontal {
        height: 1fr;
    }
    #map-column {
        width: 3fr;
        min-width: 50;
    }
    #info-column {
        width: 2fr;
        min-width: 32;
    }
    #info-column > CharacterBadgeWidget {
        height: auto;
    }
    #info-column > EnemyPanelWidget {
        height: auto;
    }
    #info-column > CombatLogWidget {
        height: 1fr;
        min-height: 6;
    }
    """

    def __init__(self, friendly_names: Optional[list] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._questioner: Any = None
        self._friendly_names: list = friendly_names or []

        # Interaction state
        self._mode: str = "idle"  # idle | actions | choices | confirm
        self._available_actions: List[str] = []
        self._choices: list = []
        self._choice_labels: list = []
        self._choice_index: int = 0
        self._question_type: str = ""
        self._confirm_message: str = ""

    def compose(self) -> ComposeResult:
        yield TurnHeader(id="turn-header")
        with Horizontal():
            with Vertical(id="map-column"):
                yield MapWidget(id="map-widget")
            with Vertical(id="info-column"):
                yield CharacterBadgeWidget(id="character-badge")
                yield EnemyPanelWidget(id="enemy-panel")
                yield CombatLogWidget(id="combat-log")
        yield ActionBarWidget(id="action-bar")

    def set_questioner(self, questioner: Any) -> None:
        """Wire the questioner for resolving user input."""
        self._questioner = questioner

    def show_actions(self, actions: List[str]) -> None:
        """Display action buttons and enable key selection."""
        self._mode = "actions"
        self._available_actions = list(actions)
        try:
            bar = self.query_one("#action-bar", ActionBarWidget)
            bar.set_actions(actions)
        except Exception:
            pass

    def show_choices(self, question_type: str, choices: list, labels: Optional[list] = None) -> None:
        """Show a navigable list of choices."""
        self._mode = "choices"
        self._question_type = question_type
        self._choices = list(choices)
        self._choice_labels = list(labels) if labels else [str(c) for c in choices]
        self._choice_index = 0
        # Pause combat log scrolling while navigating choices
        try:
            log = self.query_one("#combat-log", CombatLogWidget)
            log.pause_scroll()
        except Exception:
            pass
        self._update_choice_display()

    def show_confirm(self, question_type: str, message: str) -> None:
        """Show a Y/N confirmation prompt."""
        self._mode = "confirm"
        self._question_type = question_type
        self._confirm_message = message
        try:
            bar = self.query_one("#action-bar", ActionBarWidget)
            bar.set_status(f"{message} [Y/N]")
        except Exception:
            pass

    def _update_choice_display(self) -> None:
        """Update the action bar to show current choice selection."""
        try:
            bar = self.query_one("#action-bar", ActionBarWidget)
            if self._choice_labels:
                idx = self._choice_index
                total = len(self._choice_labels)
                label = self._choice_labels[idx]
                bar.set_status(f"\u25b6 {label}  ({idx + 1}/{total})  [Up/Down] Navigate  [Enter] Select  [Esc] Cancel")
            else:
                bar.set_status("")
        except Exception:
            pass

        # Flash the currently selected cell when navigating movement choices
        if self._question_type == "ask_where_to_move" and self._choices:
            try:
                map_w = self.query_one("#map-widget", MapWidget)
                selected_pos = self._choices[self._choice_index]
                map_w._flash_cells = {str(selected_pos)}
                map_w.refresh()
            except Exception:
                pass

    def on_key(self, event) -> None:
        """Handle all keyboard input based on current mode."""
        key = event.key.lower() if hasattr(event, "key") else ""

        # Tab cycles enemy panel selection regardless of mode
        if key == "tab":
            try:
                panel = self.query_one("#enemy-panel", EnemyPanelWidget)
                panel.cycle_enemy(1)
            except Exception:
                pass
            return

        if self._mode == "actions":
            self._handle_action_key(key)
        elif self._mode == "choices":
            self._handle_choice_key(key)
        elif self._mode == "confirm":
            self._handle_confirm_key(key)

    def _handle_action_key(self, key: str) -> None:
        """Handle key press in action selection mode."""
        action = _KEY_TO_ACTION.get(key)
        if action and action in self._available_actions:
            self._mode = "idle"
            try:
                bar = self.query_one("#action-bar", ActionBarWidget)
                bar.clear()
            except Exception:
                pass
            if self._questioner:
                self._questioner.resolve(action)

    def _handle_choice_key(self, key: str) -> None:
        """Handle key press in choice navigation mode."""
        if key in ("up", "k"):
            if self._choice_index > 0:
                self._choice_index -= 1
                self._update_choice_display()
        elif key in ("down", "j"):
            if self._choice_index < len(self._choices) - 1:
                self._choice_index += 1
                self._update_choice_display()
        elif key == "enter":
            if self._choices:
                selected = self._choices[self._choice_index]
                self._mode = "idle"
                try:
                    bar = self.query_one("#action-bar", ActionBarWidget)
                    bar.clear()
                except Exception:
                    pass
                try:
                    log = self.query_one("#combat-log", CombatLogWidget)
                    log.resume_scroll()
                except Exception:
                    pass
                # Clear movement highlights from the map
                if hasattr(self.app, "clear_highlights"):
                    self.app.clear_highlights()
                if self._questioner:
                    self._questioner.resolve(selected)
        elif key == "escape":
            self._mode = "idle"
            try:
                bar = self.query_one("#action-bar", ActionBarWidget)
                bar.clear()
            except Exception:
                pass
            try:
                log = self.query_one("#combat-log", CombatLogWidget)
                log.resume_scroll()
            except Exception:
                pass
            # Clear movement highlights from the map
            if hasattr(self.app, "clear_highlights"):
                self.app.clear_highlights()
            if self._questioner:
                self._questioner.resolve(False)

    def _handle_confirm_key(self, key: str) -> None:
        """Handle key press in Y/N confirmation mode."""
        if key == "y":
            self._mode = "idle"
            try:
                bar = self.query_one("#action-bar", ActionBarWidget)
                bar.clear()
            except Exception:
                pass
            if self._questioner:
                self._questioner.resolve(True)
        elif key == "n":
            self._mode = "idle"
            try:
                bar = self.query_one("#action-bar", ActionBarWidget)
                bar.clear()
            except Exception:
                pass
            if self._questioner:
                self._questioner.resolve(False)
