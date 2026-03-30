"""Enemy panel widget — dedicated panel showing all enemy info."""

from __future__ import annotations

from typing import List

from rich.style import Style
from rich.text import Text
from textual.widgets import RichLog

MINI_BAR_W = 10
FILLED = "\u2588"  # █
EMPTY = "\u2591"  # ░


def _bar_color(ratio: float) -> str:
    if ratio > 0.50:
        return "#3fb950"
    if ratio > 0.25:
        return "#e3b341"
    return "#f85149"


class EnemyPanelWidget(RichLog):
    """Panel showing all enemies with Tab to cycle expanded details."""

    DEFAULT_CSS = """
    EnemyPanelWidget {
        background: #0d1117;
        padding: 0 1;
        border: tall #f85149;
        scrollbar-size: 1 1;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(highlight=False, markup=False, wrap=True, auto_scroll=False, **kwargs)
        self._enemies: List[object] = []
        self._selected_idx: int = 0
        self._rebuilding: bool = False

    def update_enemies(self, enemies: List[object]) -> None:
        self._enemies = list(enemies)
        # Clamp selection
        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        if self._selected_idx >= len(alive):
            self._selected_idx = 0
        self._rebuild()

    def cycle_enemy(self, direction: int = 1) -> None:
        """Cycle selected enemy by direction (+1 next, -1 prev)."""
        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        if not alive:
            return
        self._selected_idx = (self._selected_idx + direction) % len(alive)
        self._rebuild()

    def refresh(self, *args, **kwargs) -> None:
        """Override refresh to rebuild content from stored enemy data."""
        if self._enemies and not self._rebuilding:
            self._rebuild()
        return super().refresh(*args, **kwargs)

    def _rebuild(self) -> None:
        """Clear and rewrite all content."""
        self._rebuilding = True
        try:
            self.clear()
            for line in self._build_lines():
                self.write(line)
        finally:
            self._rebuilding = False

    def _build_panel_text(self) -> Text:
        """Build full panel as single Text (for tests)."""
        result = Text()
        for line in self._build_lines():
            result.append_text(line)
            result.append("\n")
        return result

    def _build_lines(self) -> List[Text]:
        """Build list of Text lines for the panel."""
        lines: List[Text] = []

        # Header
        header = Text()
        header.append("  \u2620 ", style=Style(color="#f85149", bold=True))
        header.append("ENEMIES", style=Style(bold=True, color="#f85149"))

        alive = [e for e in self._enemies if hasattr(e, "is_alive") and e.is_alive()]
        dead = [e for e in self._enemies if hasattr(e, "is_alive") and not e.is_alive()]

        header.append(f"  ({len(alive)} alive", style=Style(color="#6e7681"))
        if dead:
            header.append(f", {len(dead)} dead", style=Style(color="#484f58"))
        header.append(")", style=Style(color="#6e7681"))

        if alive:
            header.append("  [Tab] cycle", style=Style(color="#484f58"))
        lines.append(header)

        if not alive and not dead:
            lines.append(Text("  No enemies nearby", style=Style(dim=True)))
            return lines

        lines.append(Text(" \u2500" * 15, style=Style(color="#21262d")))

        for idx, e in enumerate(alive):
            is_selected = idx == self._selected_idx
            ej = e.job.name if hasattr(e.job, "name") else str(e.job)

            # Name line
            name_line = Text()
            prefix = " \u25b8 " if is_selected else "   "
            name_color = "#ff7b72" if is_selected else "#f85149"
            name_line.append(prefix)
            name_line.append(f"{e.name}", style=Style(bold=is_selected, color=name_color))
            name_line.append(f" {ej}", style=Style(color="#8b949e"))
            name_line.append(f" Lv.{e.level}", style=Style(color="#f0883e"))

            if hasattr(e, "position") and e.position:
                pos = e.position
                if isinstance(pos, list) and len(pos) == 2:
                    from emberblast.utils import convert_number_to_letter

                    pos_str = f"{convert_number_to_letter(pos[0])}{pos[1]}"
                else:
                    pos_str = str(pos)
                name_line.append(f" \u25c8{pos_str}", style=Style(color="#58a6ff"))
            lines.append(name_line)

            # HP bar
            hp_line = Text()
            hp_ratio = e.life / e.health_points if e.health_points > 0 else 0
            hp_color = _bar_color(hp_ratio)
            filled = round(hp_ratio * MINI_BAR_W)
            empty = MINI_BAR_W - filled

            hp_line.append("   HP ", style=Style(color="#6e7681"))
            hp_line.append(FILLED * filled, style=Style(color=hp_color))
            hp_line.append(EMPTY * empty, style=Style(color="#21262d"))
            hp_line.append(f" {e.life}/{e.health_points}", style=Style(color="#6e7681"))

            if hasattr(e, "mana") and hasattr(e, "magic_points") and e.magic_points > 0:
                hp_line.append(f"  MP {e.mana}/{e.magic_points}", style=Style(color="#d2a8ff"))
            lines.append(hp_line)

            # Expanded details for selected enemy
            if is_selected:
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
                    lines.append(Text("   " + "  ".join(stats_parts), style=Style(color="#484f58")))

                # Side effects
                if hasattr(e, "side_effects") and e.side_effects:
                    se_line = Text()
                    for se in e.side_effects:
                        se_name = se.name if hasattr(se, "name") else str(se)
                        se_type = getattr(se, "effect_type", "buff")
                        icon = "\u25b2" if se_type == "buff" else "\u25bc"
                        color = "#3fb950" if se_type == "buff" else "#f85149"
                        se_line.append(f"   {icon}{se_name}", style=Style(color=color))
                        if hasattr(se, "duration"):
                            se_line.append(f"({se.duration}t)", style=Style(color="#6e7681"))
                        se_line.append(" ")
                    lines.append(se_line)

        # Dead enemies
        if dead:
            lines.append(Text(" \u2500" * 15, style=Style(color="#21262d")))
            for e in dead:
                ej = e.job.name if hasattr(e.job, "name") else str(e.job)
                dead_line = Text()
                dead_line.append(
                    f"   \u2620 {e.name} {ej}",
                    style=Style(color="#484f58", strike=True),
                )
                dead_line.append(" DEAD", style=Style(color="#484f58"))
                lines.append(dead_line)

        return lines

    def render(self) -> Text:
        # Fallback for initial empty state
        if not self._enemies:
            result = Text()
            result.append("  \u2620 ", style=Style(color="#f85149", bold=True))
            result.append("ENEMIES", style=Style(bold=True, color="#f85149"))
            result.append("  (0 alive)", style=Style(color="#6e7681"))
            return result
        return Text("")
