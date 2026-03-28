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
    """Panel showing all enemies with Tab to cycle expanded details."""

    DEFAULT_CSS = """
    EnemyPanelWidget {
        background: #0d1117;
        padding: 0 1;
        border: tall #f85149;
        height: auto;
        min-height: 6;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._enemies: List[object] = []
        self._selected_idx: int = 0

    def update_enemies(self, enemies: List[object]) -> None:
        self._enemies = list(enemies)
        # Clamp selection
        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        if self._selected_idx >= len(alive):
            self._selected_idx = 0
        self.refresh()

    def cycle_enemy(self, direction: int = 1) -> None:
        """Cycle selected enemy by direction (+1 next, -1 prev)."""
        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        if not alive:
            return
        self._selected_idx = (self._selected_idx + direction) % len(alive)
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
        result.append(")", style=Style(color="#6e7681"))

        if alive:
            result.append("  [Tab] cycle", style=Style(color="#484f58"))
        result.append("\n")

        if not alive and not dead:
            result.append("  No enemies nearby", style=Style(dim=True))
            return result

        result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))

        for idx, e in enumerate(alive):
            is_selected = idx == self._selected_idx
            ej = e.job.name if hasattr(e.job, "name") else str(e.job)

            # Selection indicator
            prefix = " \u25b8 " if is_selected else "   "

            # Name + job + level + position (compact)
            name_color = "#ff7b72" if is_selected else "#f85149"
            result.append(prefix)
            result.append(f"{e.name}", style=Style(bold=is_selected, color=name_color))
            result.append(f" {ej}", style=Style(color="#8b949e"))
            result.append(f" Lv.{e.level}", style=Style(color="#f0883e"))

            if hasattr(e, "position") and e.position:
                pos = e.position
                if isinstance(pos, list) and len(pos) == 2:
                    from emberblast.utils import convert_number_to_letter

                    pos_str = f"{convert_number_to_letter(pos[0])}{pos[1]}"
                else:
                    pos_str = str(pos)
                result.append(f" \u25c8{pos_str}", style=Style(color="#58a6ff"))
            result.append("\n")

            # HP bar — always shown for all enemies
            hp_ratio = e.life / e.health_points if e.health_points > 0 else 0
            hp_color = _bar_color(hp_ratio)
            filled = round(hp_ratio * MINI_BAR_W)
            empty = MINI_BAR_W - filled

            result.append("   HP ", style=Style(color="#6e7681"))
            result.append(FILLED * filled, style=Style(color=hp_color))
            result.append(EMPTY * empty, style=Style(color="#21262d"))
            result.append(f" {e.life}/{e.health_points}", style=Style(color="#6e7681"))

            if hasattr(e, "mana") and hasattr(e, "magic_points") and e.magic_points > 0:
                result.append(f"  MP {e.mana}/{e.magic_points}", style=Style(color="#d2a8ff"))
            result.append("\n")

            # Expanded details for selected enemy
            if is_selected:
                # Stats
                stats_parts = []
                for attr, label in [
                    ("strength", "STR"),
                    ("intelligence", "INT"),
                    ("accuracy", "ACC"),
                    ("armour", "ARM"),
                    ("magic_resist", "RES"),
                    ("move_speed", "SPD"),
                ]:
                    val = getattr(e, attr, None)
                    if val is not None:
                        stats_parts.append(f"{label} {val}")
                if stats_parts:
                    result.append("   ", style=Style(color="#484f58"))
                    result.append("  ".join(stats_parts) + "\n", style=Style(color="#484f58"))

                # Side effects
                if hasattr(e, "side_effects") and e.side_effects:
                    for se in e.side_effects:
                        se_name = se.name if hasattr(se, "name") else str(se)
                        se_type = getattr(se, "effect_type", "buff")
                        icon = "\u25b2" if se_type == "buff" else "\u25bc"
                        color = "#3fb950" if se_type == "buff" else "#f85149"
                        result.append(f"   {icon}{se_name}", style=Style(color=color))
                        if hasattr(se, "duration"):
                            result.append(f"({se.duration}t)", style=Style(color="#6e7681"))
                        result.append(" ")
                    result.append("\n")

        # Dead enemies — single compact line
        if dead:
            result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))
            for e in dead:
                ej = e.job.name if hasattr(e.job, "name") else str(e.job)
                result.append(f"   \u2620 {e.name} {ej}", style=Style(color="#484f58", strike=True))
                result.append(" DEAD\n", style=Style(color="#484f58"))

        return result

    def render(self) -> Text:
        return self._build_panel_text()
