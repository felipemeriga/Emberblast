"""Combat log widget for the Textual TUI."""

from __future__ import annotations

from rich.style import Style
from rich.text import Text
from textual.widgets import RichLog

from emberblast.tui.styles import LOG_COLORS

# Categories that get special formatting
_BOLD_CATEGORIES = {"turn", "victory", "death", "level_up", "critical"}


class CombatLogWidget(RichLog):
    """Scrollable, color-coded combat log using Textual's RichLog for real scrolling."""

    DEFAULT_CSS = """
    CombatLogWidget {
        background: #161b22;
        border: solid #30363d;
        scrollbar-size: 1 1;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(highlight=False, markup=False, wrap=True, auto_scroll=True, **kwargs)
        self._current_turn: int = 0
        self._initialized: bool = False

    def on_mount(self) -> None:
        """Write the header when mounted."""
        if not self._initialized:
            self._initialized = True
            header = Text()
            header.append("COMBAT LOG", style=Style(bold=True, color="#f0883e"))
            self.write(header)
            sep = Text("─" * 40, style=Style(color="#30363d"))
            self.write(sep)

    def set_turn(self, turn: int) -> None:
        """Track the current turn number for log prefixes."""
        self._current_turn = turn

    def add_entry(self, message: str, category: str = "system") -> None:
        """Append a styled log entry."""
        color = LOG_COLORS.get(category, LOG_COLORS["system"])

        # Separator lines
        if message == "---":
            sep = Text("─" * 40, style=Style(color="#30363d"))
            self.write(sep)
            return

        line = Text()

        # Turn prefix for combat events
        if self._current_turn > 0 and category not in ("system", "turn"):
            line.append(f"[T{self._current_turn}] ", style=Style(color="#6e7681"))

        bold = category in _BOLD_CATEGORIES
        italic = category == "narration"
        line.append(message, style=Style(color=color, bold=bold, italic=italic))

        self.write(line)

    def clear_log(self) -> None:
        """Remove all log entries."""
        self.clear()
