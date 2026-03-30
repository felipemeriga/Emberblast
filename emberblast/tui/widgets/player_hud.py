"""Player HUD widget for the Textual TUI."""

from __future__ import annotations

from typing import List, Optional

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


def _build_bar(current: int, maximum: int, label: str, bar_width: int = BAR_WIDTH) -> Text:
    """Build a colored bar with label and numeric values."""
    ratio = current / maximum if maximum > 0 else 0
    filled_count = round(ratio * bar_width)
    empty_count = bar_width - filled_count
    color = _bar_color(ratio)

    bar = Text()
    bar.append(f"{label}: ", style=Style(bold=True))
    bar.append(FILLED * filled_count, style=Style(color=color))
    bar.append(EMPTY * empty_count, style=Style(color="#30363d"))
    bar.append(f" {current}/{maximum}", style=Style(dim=True))
    return bar


class PlayerHUDWidget(Widget):
    """Displays controlled player stats and a compact enemy list."""

    DEFAULT_CSS = """
    PlayerHUDWidget {
        background: #161b22;
        padding: 1;
        border: solid #30363d;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._player: Optional[object] = None
        self._enemies: List[object] = []

    def update_player(self, player: object) -> None:
        """Update the displayed player and refresh."""
        self._player = player
        self.refresh()

    def update_enemies(self, enemies: List[object]) -> None:
        """Update the enemy list and refresh."""
        self._enemies = list(enemies)
        self.refresh()

    def _build_hud_text(self) -> Text:
        """Build a Rich Text object for the HUD display."""
        result = Text()

        if self._player is None:
            result.append("No player data", style=Style(dim=True))
            return result

        p = self._player

        # ── Your character ──
        job_name = p.job.name if hasattr(p.job, "name") else str(p.job)
        race_name = p.race.name if hasattr(p.race, "name") else str(p.race)
        result.append(f"⚔ {p.name}", style=Style(bold=True, color="#58a6ff"))
        result.append(f"  {race_name}\n", style=Style(color="#8b949e"))
        result.append(f"  {job_name}", style=Style(color="#8b949e"))
        result.append(f"  Lv.{p.level}\n", style=Style(color="#f0883e", bold=True))

        # HP bar
        hp_bar = _build_bar(p.life, p.health_points, "HP")
        result.append_text(hp_bar)
        result.append("\n")

        # MP bar
        mp_bar = _build_bar(p.mana, p.magic_points, "MP")
        result.append_text(mp_bar)
        result.append("\n")

        # Stats
        result.append(
            f"STR:{p.strength} INT:{p.intelligence} ACC:{p.accuracy} "
            f"ARM:{p.armour} RES:{p.magic_resist} SPD:{p.move_speed} WILL:{p.will}\n",
            style=Style(dim=True),
        )

        # ── Enemy list ──
        alive_enemies = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        if alive_enemies:
            result.append("─" * 30 + "\n", style=Style(color="#30363d"))
            result.append("ENEMIES\n", style=Style(bold=True, color="#f85149"))
            for e in alive_enemies:
                ej = e.job.name if hasattr(e.job, "name") else str(e.job)
                hp_ratio = e.life / e.health_points if e.health_points > 0 else 0
                hp_color = _bar_color(hp_ratio)
                mini_bar_w = 10
                filled = round(hp_ratio * mini_bar_w)
                empty = mini_bar_w - filled

                result.append(f"  {e.name}", style=Style(color="#f85149"))
                result.append(f" {ej}", style=Style(dim=True))
                result.append(f" Lv.{e.level} ", style=Style(dim=True))
                result.append(FILLED * filled, style=Style(color=hp_color))
                result.append(EMPTY * empty, style=Style(color="#30363d"))
                result.append(f" {e.life}/{e.health_points}\n", style=Style(dim=True))

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_hud_text()
