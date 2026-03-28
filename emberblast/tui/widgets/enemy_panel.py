"""Enemy panel widget — dedicated panel showing all enemy info."""

from __future__ import annotations

from typing import List

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

MINI_BAR_W = 10
FILLED = "\u2588"  # █
EMPTY = "\u2591"  # ░


def _bar_color(ratio: float) -> str:
    if ratio > 0.50:
        return "#3fb950"
    if ratio > 0.25:
        return "#e3b341"
    return "#f85149"


class EnemyPanelWidget(Widget):
    """Dedicated panel showing all enemy information with mini-cards."""

    DEFAULT_CSS = """
    EnemyPanelWidget {
        background: #0d1117;
        padding: 0 1;
        border: tall #f85149;
        height: auto;
        min-height: 8;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._enemies: List[object] = []

    def update_enemies(self, enemies: List[object]) -> None:
        self._enemies = list(enemies)
        self.refresh()

    def _build_panel_text(self) -> Text:
        result = Text()

        # Header
        result.append("\n")
        result.append("  \u2620 ", style=Style(color="#f85149", bold=True))
        result.append("ENEMIES", style=Style(bold=True, color="#f85149"))

        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        dead = [e for e in self._enemies if hasattr(e, "is_alive") and not e.is_alive()]

        result.append(f"  ({len(alive)} alive", style=Style(color="#6e7681"))
        if dead:
            result.append(f", {len(dead)} dead", style=Style(color="#484f58"))
        result.append(")\n", style=Style(color="#6e7681"))

        if not alive and not dead:
            result.append("  No enemies nearby", style=Style(dim=True))
            return result

        result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))

        for idx, e in enumerate(alive):
            ej = e.job.name if hasattr(e.job, "name") else str(e.job)

            # Name line: name + job + level
            result.append(f"  {e.name}", style=Style(bold=True, color="#f85149"))
            result.append(f"  {ej}", style=Style(color="#8b949e"))
            result.append(f"  Lv.{e.level}", style=Style(color="#f0883e"))

            # Position
            if hasattr(e, "position") and e.position:
                pos = e.position
                if isinstance(pos, list) and len(pos) == 2:
                    from emberblast.utils import convert_number_to_letter

                    pos_str = f"{convert_number_to_letter(pos[0])}{pos[1]}"
                else:
                    pos_str = str(pos)
                result.append(f"  \u25c8{pos_str}", style=Style(color="#58a6ff"))
            result.append("\n")

            # HP bar
            hp_ratio = e.life / e.health_points if e.health_points > 0 else 0
            hp_color = _bar_color(hp_ratio)
            filled = round(hp_ratio * MINI_BAR_W)
            empty = MINI_BAR_W - filled

            result.append("  HP ", style=Style(color="#6e7681"))
            result.append(FILLED * filled, style=Style(color=hp_color))
            result.append(EMPTY * empty, style=Style(color="#21262d"))
            result.append(f" {e.life}/{e.health_points}", style=Style(color="#6e7681"))

            # MP inline
            if hasattr(e, "mana") and hasattr(e, "magic_points") and e.magic_points > 0:
                result.append(f"  MP {e.mana}/{e.magic_points}", style=Style(color="#d2a8ff"))
            result.append("\n")

            # Key stats inline
            stats_parts = []
            if hasattr(e, "strength"):
                stats_parts.append(f"STR:{e.strength}")
            if hasattr(e, "intelligence"):
                stats_parts.append(f"INT:{e.intelligence}")
            if hasattr(e, "armour"):
                stats_parts.append(f"ARM:{e.armour}")
            if stats_parts:
                result.append(f"  {' '.join(stats_parts)}\n", style=Style(color="#484f58"))

            # Side effects
            if hasattr(e, "side_effects") and e.side_effects:
                for se in e.side_effects:
                    se_name = se.name if hasattr(se, "name") else str(se)
                    se_type = getattr(se, "effect_type", "buff")
                    icon = "\u25b2" if se_type == "buff" else "\u25bc"
                    color = "#3fb950" if se_type == "buff" else "#f85149"
                    result.append(f"  {icon}{se_name}", style=Style(color=color))
                    if hasattr(se, "duration"):
                        result.append(f"({se.duration}t)", style=Style(color="#6e7681"))
                    result.append(" ")
                result.append("\n")

            # Separator between enemies
            if idx < len(alive) - 1:
                result.append("  \u00b7 \u00b7 \u00b7\n", style=Style(color="#21262d"))

        # Dead enemies compact
        if dead:
            result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))
            for e in dead:
                ej = e.job.name if hasattr(e.job, "name") else str(e.job)
                result.append(f"  \u2620 {e.name} {ej}", style=Style(color="#484f58", strike=True))
                result.append(" DEAD\n", style=Style(color="#484f58"))

        return result

    def render(self) -> Text:
        return self._build_panel_text()
