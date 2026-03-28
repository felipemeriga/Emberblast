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
    """Displays available actions as styled bordered buttons."""

    DEFAULT_CSS = """
    ActionBarWidget {
        dock: bottom;
        height: 5;
        background: #0d1117;
        border-top: tall #30363d;
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
        """Build a Rich Text object for the action bar with bordered buttons."""
        result = Text()

        if self._status and not self._actions:
            result.append("\n ")
            result.append(self._status, style=Style(italic=True, color="#8b949e"))
            return result

        if self._actions:
            # Top border of buttons
            top_line = Text(" ")
            mid_line = Text(" ")
            bot_line = Text(" ")

            for action in self._actions:
                key = ACTION_KEYS.get(action, action[0].upper())
                color = ACTION_COLORS.get(action, "#8b949e")
                label = f"[{key}]{action[1:]}"
                width = len(label) + 2  # padding inside box
                border_style = Style(color=color)

                top_line.append("\u250c" + "\u2500" * width + "\u2510 ", style=border_style)
                mid_line.append("\u2502", style=border_style)
                mid_line.append(f" [{key}]", style=Style(bold=True, color=color))
                mid_line.append(f"{action[1:]} ", style=Style(color=color))
                mid_line.append("\u2502 ", style=border_style)
                bot_line.append("\u2514" + "\u2500" * width + "\u2518 ", style=border_style)

            result.append_text(top_line)
            result.append("\n")
            result.append_text(mid_line)
            result.append("\n")
            result.append_text(bot_line)

        if self._status and self._actions:
            result.append("\n ")
            result.append(self._status, style=Style(dim=True, italic=True))

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_bar_text()
