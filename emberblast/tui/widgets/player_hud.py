"""Player HUD widget for the Textual TUI."""

from __future__ import annotations

from typing import Optional

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

BAR_WIDTH = 20
FILLED = "\u2588"  # █
EMPTY = "\u2591"  # ░


def _bar_color(ratio: float) -> str:
    """Return a hex color based on the health/mana ratio."""
    if ratio > 0.50:
        return "#3fb950"  # green
    if ratio > 0.25:
        return "#e3b341"  # yellow
    return "#f85149"  # red


def _build_bar(current: int, maximum: int, label: str) -> Text:
    """Build a colored bar with label and numeric values."""
    ratio = current / maximum if maximum > 0 else 0
    filled_count = round(ratio * BAR_WIDTH)
    empty_count = BAR_WIDTH - filled_count
    color = _bar_color(ratio)

    bar = Text()
    bar.append(f"{label}: ", style=Style(bold=True))
    bar.append(FILLED * filled_count, style=Style(color=color))
    bar.append(EMPTY * empty_count, style=Style(color="#30363d"))
    bar.append(f" {current}/{maximum}", style=Style(dim=True))
    return bar


class PlayerHUDWidget(Widget):
    """Displays player name, job, race, HP bar, MP bar, and stats."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._player: Optional[object] = None

    def update_player(self, player: object) -> None:
        """Update the displayed player and refresh."""
        self._player = player
        self.refresh()

    def _build_hud_text(self) -> Text:
        """Build a Rich Text object for the HUD display."""
        if self._player is None:
            return Text("No player data")

        p = self._player
        result = Text()

        # Name / Job / Race / Level
        job_name = p.job.name if hasattr(p.job, "name") else str(p.job)
        race_name = p.race.name if hasattr(p.race, "name") else str(p.race)
        result.append(f"{p.name}", style=Style(bold=True, color="#58a6ff"))
        result.append(f"  Lv.{p.level} {job_name} ({race_name})\n", style=Style(dim=True))

        # HP bar
        hp_bar = _build_bar(p.life, p.health_points, "HP")
        result.append_text(hp_bar)
        result.append("\n")

        # MP bar
        mp_bar = _build_bar(p.mana, p.magic_points, "MP")
        result.append_text(mp_bar)
        result.append("\n")

        # Stats line
        stats = (
            f"STR:{p.strength}  INT:{p.intelligence}  ACC:{p.accuracy}  "
            f"ARM:{p.armour}  RES:{p.magic_resist}  SPD:{p.move_speed}  WILL:{p.will}"
        )
        result.append(stats, style=Style(dim=True))

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_hud_text()
