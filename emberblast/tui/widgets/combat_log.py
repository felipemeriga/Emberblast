"""Combat log widget for the Textual TUI."""

from __future__ import annotations

from collections import deque
from typing import Tuple

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

from emberblast.tui.styles import LOG_COLORS

DEFAULT_MAX_ENTRIES = 100

# Categories that get special formatting
_SEPARATOR_CATEGORIES = {"system"}
_BOLD_CATEGORIES = {"turn", "victory", "death", "level_up", "critical"}


class CombatLogWidget(Widget):
    """Scrollable, color-coded combat log."""

    DEFAULT_CSS = """
    CombatLogWidget {
        background: #161b22;
        padding: 1;
        overflow-y: auto;
    }
    """

    def __init__(self, max_entries: int = DEFAULT_MAX_ENTRIES, **kwargs) -> None:
        super().__init__(**kwargs)
        self._entries: deque[Tuple[str, str]] = deque(maxlen=max_entries)
        self._current_turn: int = 0

    def set_turn(self, turn: int) -> None:
        """Track the current turn number for log prefixes."""
        self._current_turn = turn

    def add_entry(self, message: str, category: str = "system") -> None:
        """Append a log entry and refresh."""
        self._entries.append((message, category, self._current_turn))
        self.refresh()

    def clear_log(self) -> None:
        """Remove all log entries."""
        self._entries.clear()
        self.refresh()

    def _build_log_text(self) -> Text:
        """Build a Rich Text object for the log display."""
        result = Text()
        # Header
        result.append("COMBAT LOG\n", style=Style(bold=True, color="#f0883e"))
        result.append("─" * 30 + "\n", style=Style(color="#30363d"))

        if not self._entries:
            result.append("Awaiting battle...", style=Style(dim=True))
            return result

        for entry in self._entries:
            message, category = entry[0], entry[1]
            turn = entry[2] if len(entry) > 2 else 0
            color = LOG_COLORS.get(category, LOG_COLORS["system"])

            # Separator lines stay plain
            if message == "---":
                result.append("─" * 30 + "\n", style=Style(color="#30363d"))
                continue

            bold = category in _BOLD_CATEGORIES
            italic = category == "narration"
            style = Style(color=color, bold=bold, italic=italic)

            # Add turn prefix for combat events (not system/separator)
            if turn > 0 and category not in _SEPARATOR_CATEGORIES and category != "turn":
                result.append(f"[T{turn}] ", style=Style(color="#6e7681", dim=True))

            result.append(f"{message}\n", style=style)

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_log_text()
