"""Character badge widget — always-visible controlled player info."""

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


def _build_bar(current: int, maximum: int, label: str, bar_width: int = BAR_WIDTH) -> Text:
    """Build a colored bar with label and numeric values."""
    ratio = current / maximum if maximum > 0 else 0
    filled_count = round(ratio * bar_width)
    empty_count = bar_width - filled_count
    color = _bar_color(ratio)

    bar = Text()
    bar.append(f" {label}: ", style=Style(bold=True, color="#8b949e"))
    bar.append(FILLED * filled_count, style=Style(color=color))
    bar.append(EMPTY * empty_count, style=Style(color="#30363d"))
    bar.append(f" {current}/{maximum}", style=Style(dim=True))
    return bar


class CharacterBadgeWidget(Widget):
    """Always-visible panel showing the controlled player's full stats."""

    DEFAULT_CSS = """
    CharacterBadgeWidget {
        background: #161b22;
        padding: 1;
        border: solid #3fb950;
        height: auto;
        max-height: 18;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._player: Optional[object] = None

    def update_player(self, player: object) -> None:
        """Update the displayed player and refresh."""
        self._player = player
        self.refresh()

    def _build_badge_text(self) -> Text:
        """Build a Rich Text object for the character badge."""
        result = Text()

        if self._player is None:
            result.append(" No player data", style=Style(dim=True))
            return result

        p = self._player

        job_name = p.job.name if hasattr(p.job, "name") else str(p.job)
        race_name = p.race.name if hasattr(p.race, "name") else str(p.race)

        # Header: name + race
        result.append(" \u2694 ", style=Style(color="#f0883e"))
        result.append(f"{p.name}", style=Style(bold=True, color="#58a6ff"))
        result.append(f"  {race_name}", style=Style(color="#8b949e"))
        result.append("\n")

        # Job + Level
        result.append(f"   {job_name}", style=Style(color="#d2a8ff"))
        result.append(f"  Lv.{p.level}", style=Style(color="#f0883e", bold=True))
        result.append("\n")

        # Separator
        result.append(" " + "\u2500" * 24 + "\n", style=Style(color="#30363d"))

        # HP bar
        hp_bar = _build_bar(p.life, p.health_points, "HP")
        result.append_text(hp_bar)
        result.append("\n")

        # MP bar
        mp_bar = _build_bar(p.mana, p.magic_points, "MP")
        result.append_text(mp_bar)
        result.append("\n")

        # Separator
        result.append(" " + "\u2500" * 24 + "\n", style=Style(color="#30363d"))

        # Stats in 2 columns
        result.append("  STR ", style=Style(color="#8b949e"))
        result.append(f"{p.strength:<4}", style=Style(bold=True, color="#f85149"))
        result.append("INT ", style=Style(color="#8b949e"))
        result.append(f"{p.intelligence:<4}", style=Style(bold=True, color="#d2a8ff"))
        result.append("ACC ", style=Style(color="#8b949e"))
        result.append(f"{p.accuracy}", style=Style(bold=True, color="#e3b341"))
        result.append("\n")

        result.append("  ARM ", style=Style(color="#8b949e"))
        result.append(f"{p.armour:<4}", style=Style(bold=True, color="#58a6ff"))
        result.append("RES ", style=Style(color="#8b949e"))
        result.append(f"{p.magic_resist:<4}", style=Style(bold=True, color="#d2a8ff"))
        result.append("SPD ", style=Style(color="#8b949e"))
        result.append(f"{p.move_speed}", style=Style(bold=True, color="#3fb950"))
        result.append("\n")

        result.append("  WILL ", style=Style(color="#8b949e"))
        result.append(f"{p.will}", style=Style(bold=True, color="#e3b341"))

        # Position
        if hasattr(p, "position") and p.position:
            pos = p.position
            if isinstance(pos, list) and len(pos) == 2:
                from emberblast.utils import convert_number_to_letter

                pos_str = f"{convert_number_to_letter(pos[0])}{pos[1]}"
            else:
                pos_str = str(pos)
            result.append("   Pos: ", style=Style(color="#8b949e"))
            result.append(pos_str, style=Style(bold=True, color="#58a6ff"))

        result.append("\n")

        # Active side effects
        if hasattr(p, "side_effects") and p.side_effects:
            result.append(" " + "\u2500" * 24 + "\n", style=Style(color="#30363d"))
            result.append(" Effects:\n", style=Style(color="#8b949e"))
            for se in p.side_effects:
                se_name = se.name if hasattr(se, "name") else str(se)
                se_type = getattr(se, "effect_type", "buff")
                icon = "\u25b2" if se_type == "buff" else "\u25bc"
                color = "#3fb950" if se_type == "buff" else "#f85149"
                result.append(f"  {icon} {se_name}", style=Style(color=color))
                if hasattr(se, "duration"):
                    result.append(f" ({se.duration}t)", style=Style(dim=True))
                result.append("\n")

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_badge_text()
