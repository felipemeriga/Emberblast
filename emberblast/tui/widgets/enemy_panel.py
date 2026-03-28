"""Enemy panel widget — dedicated panel showing all enemy info."""

from __future__ import annotations

from typing import List

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

MINI_BAR_W = 12
FILLED = "\u2588"  # █
EMPTY = "\u2591"  # ░


def _bar_color(ratio: float) -> str:
    """Return a hex color based on the health ratio."""
    if ratio > 0.50:
        return "#3fb950"
    if ratio > 0.25:
        return "#e3b341"
    return "#f85149"


class EnemyPanelWidget(Widget):
    """Dedicated scrollable panel showing all enemy information."""

    DEFAULT_CSS = """
    EnemyPanelWidget {
        background: #161b22;
        padding: 1;
        border: solid #f85149;
        height: auto;
        max-height: 50%;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._enemies: List[object] = []

    def update_enemies(self, enemies: List[object]) -> None:
        """Update the enemy list and refresh."""
        self._enemies = list(enemies)
        self.refresh()

    def _build_panel_text(self) -> Text:
        """Build a Rich Text object for the enemy panel."""
        result = Text()

        # Header
        result.append(" \u2620 ", style=Style(color="#f85149"))
        result.append("ENEMIES", style=Style(bold=True, color="#f85149"))
        result.append("\n")
        result.append(" " + "\u2500" * 24 + "\n", style=Style(color="#30363d"))

        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        dead = [e for e in self._enemies if hasattr(e, "is_alive") and not e.is_alive()]

        if not alive and not dead:
            result.append(" No enemies", style=Style(dim=True))
            return result

        for e in alive:
            ej = e.job.name if hasattr(e.job, "name") else str(e.job)

            # Name + job + level
            result.append(f" {e.name}", style=Style(bold=True, color="#f85149"))
            result.append(f" {ej}", style=Style(color="#8b949e"))
            result.append(f" Lv.{e.level}\n", style=Style(color="#f0883e"))

            # HP bar
            hp_ratio = e.life / e.health_points if e.health_points > 0 else 0
            hp_color = _bar_color(hp_ratio)
            filled = round(hp_ratio * MINI_BAR_W)
            empty = MINI_BAR_W - filled

            result.append("  HP ", style=Style(color="#8b949e"))
            result.append(FILLED * filled, style=Style(color=hp_color))
            result.append(EMPTY * empty, style=Style(color="#30363d"))
            result.append(f" {e.life}/{e.health_points}\n", style=Style(dim=True))

            # Position
            if hasattr(e, "position") and e.position:
                pos = e.position
                if isinstance(pos, list) and len(pos) == 2:
                    from emberblast.utils import convert_number_to_letter

                    pos_str = f"{convert_number_to_letter(pos[0])}{pos[1]}"
                else:
                    pos_str = str(pos)
                result.append(f"  Pos: {pos_str}\n", style=Style(dim=True))

        # Dead enemies
        for e in dead:
            ej = e.job.name if hasattr(e.job, "name") else str(e.job)
            result.append(f" \u2620 {e.name}", style=Style(color="#484f58", strike=True))
            result.append(f" {ej} DEAD\n", style=Style(color="#484f58"))

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_panel_text()
