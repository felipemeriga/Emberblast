"""Combat log widget for the Textual TUI."""

from __future__ import annotations

from collections import deque
from typing import Tuple

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

from emberblast.tui.styles import LOG_COLORS

DEFAULT_MAX_ENTRIES = 100


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

    def add_entry(self, message: str, category: str = "system") -> None:
        """Append a log entry and refresh."""
        self._entries.append((message, category))
        self.refresh()

    def clear_log(self) -> None:
        """Remove all log entries."""
        self._entries.clear()
        self.refresh()

    def _build_log_text(self) -> Text:
        """Build a Rich Text object for the log display."""
        if not self._entries:
            return Text("No entries yet")

        result = Text()
        for message, category in self._entries:
            color = LOG_COLORS.get(category, LOG_COLORS["system"])
            style = Style(color=color, italic=(category == "narration"))
            result.append(f"{message}\n", style=style)

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_log_text()
