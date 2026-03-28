"""Combat log widget for the Textual TUI."""

from __future__ import annotations

from rich.style import Style
from rich.text import Text
from textual.widgets import RichLog

from emberblast.tui.styles import LOG_COLORS

# Categories that get special formatting
_BOLD_CATEGORIES = {"turn", "victory", "death", "level_up", "critical"}

# Category-specific icons
_CATEGORY_ICONS = {
    "damage": "\u2694",
    "heal": "\u271a",
    "move": "\u2192",
    "skill": "\u2726",
    "death": "\u2620",
    "victory": "\u265b",
    "narration": "\u275d",
    "item": "\u25c6",
    "level_up": "\u25b2",
    "xp": "\u2605",
    "dice": "\u2684",
    "critical": "\u26a1",
    "side_effect": "\u223c",
    "trap": "\u26a0",
    "miss": "\u00d7",
    "warning": "\u26a0",
    "stats": "\u25a3",
}


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
            header.append(" \u2694 ", style=Style(color="#f0883e"))
            header.append("COMBAT LOG", style=Style(bold=True, color="#f0883e"))
            self.write(header)
            sep = Text("\u2500" * 40, style=Style(color="#30363d"))
            self.write(sep)

    def set_turn(self, turn: int) -> None:
        """Track the current turn number for log prefixes."""
        self._current_turn = turn

    def add_entry(self, message: str, category: str = "system") -> None:
        """Append a styled log entry."""
        color = LOG_COLORS.get(category, LOG_COLORS["system"])

        # Separator lines
        if message == "---":
            sep = Text("\u2500" * 40, style=Style(color="#30363d"))
            self.write(sep)
            return

        # Turn start gets special banner treatment
        if category == "turn" and "Turn" in message:
            banner = Text()
            banner.append(" \u2550" * 12, style=Style(color="#f0883e"))
            banner.append(f" {message} ", style=Style(bold=True, color="#f0883e"))
            banner.append("\u2550" * 12, style=Style(color="#f0883e"))
            self.write(banner)
            return

        line = Text()

        # Turn prefix for combat events
        if self._current_turn > 0 and category not in ("system", "turn"):
            line.append(f"[T{self._current_turn}] ", style=Style(color="#6e7681"))

        # Category icon
        icon = _CATEGORY_ICONS.get(category)
        if icon:
            line.append(f"{icon} ", style=Style(color=color))

        bold = category in _BOLD_CATEGORIES
        italic = category == "narration"
        line.append(message, style=Style(color=color, bold=bold, italic=italic))

        self.write(line)

    def pause_scroll(self) -> None:
        """Temporarily disable auto-scroll (e.g. during movement selection)."""
        self.auto_scroll = False

    def resume_scroll(self) -> None:
        """Re-enable auto-scroll."""
        self.auto_scroll = True

    def clear_log(self) -> None:
        """Remove all log entries."""
        self.clear()
