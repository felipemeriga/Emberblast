"""Action bar widget for the Textual TUI."""

from __future__ import annotations

from typing import Dict, List

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

from emberblast.tui.styles import ACTION_COLORS

ACTION_KEYS: Dict[str, str] = {
    "move": "M",
    "attack": "A",
    "skill": "S",
    "defend": "D",
    "item": "I",
    "hide": "H",
    "search": "R",
    "equip": "E",
    "drop": "X",
    "check": "C",
    "pass": "P",
}


class ActionBarWidget(Widget):
    """Displays available actions as keybinding buttons."""

    DEFAULT_CSS = """
    ActionBarWidget {
        dock: bottom;
        height: 3;
        background: #161b22;
        border-top: solid #30363d;
        content-align: center middle;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._actions: List[str] = []
        self._status: str = ""

    def set_actions(self, actions: List[str]) -> None:
        """Set the available actions and refresh."""
        self._actions = list(actions)
        self.refresh()

    def set_status(self, text: str) -> None:
        """Set a status message (shown when no actions or alongside them)."""
        self._status = text
        self.refresh()

    def clear(self) -> None:
        """Reset actions and status."""
        self._actions = []
        self._status = ""
        self.refresh()

    def _build_bar_text(self) -> Text:
        """Build a Rich Text object for the action bar."""
        result = Text()

        if self._actions:
            for i, action in enumerate(self._actions):
                key = ACTION_KEYS.get(action, action[0].upper())
                color = ACTION_COLORS.get(action, "#8b949e")

                if i > 0:
                    result.append("  ")

                result.append(f"[{key}]", style=Style(bold=True, color=color))
                result.append(f" {action.capitalize()}", style=Style(color=color))

        if self._status:
            if self._actions:
                result.append("  ")
            result.append(self._status, style=Style(dim=True, italic=True))

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_bar_text()
