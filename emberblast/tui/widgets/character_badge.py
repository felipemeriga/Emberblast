"""Character badge widget — always-visible controlled player info."""

from __future__ import annotations

from typing import Optional

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

BAR_WIDTH = 16
FILLED = "\u2588"  # █
EMPTY = "\u2591"  # ░


def _bar_color(ratio: float) -> str:
    if ratio > 0.50:
        return "#3fb950"
    if ratio > 0.25:
        return "#e3b341"
    return "#f85149"


def _build_bar(current: int, maximum: int, label: str, color_override: str = "") -> Text:
    ratio = current / maximum if maximum > 0 else 0
    filled_count = round(ratio * BAR_WIDTH)
    empty_count = BAR_WIDTH - filled_count
    color = color_override or _bar_color(ratio)

    bar = Text()
    bar.append(f" {label} ", style=Style(bold=True, color="#8b949e"))
    bar.append(FILLED * filled_count, style=Style(color=color))
    bar.append(EMPTY * empty_count, style=Style(color="#21262d"))
    bar.append(f" {current}/{maximum}", style=Style(color="#6e7681"))
    return bar


class CharacterBadgeWidget(Widget):
    """Always-visible panel showing the controlled player's full stats."""

    DEFAULT_CSS = """
    CharacterBadgeWidget {
        background: #0d1117;
        padding: 0 1;
        border: tall #3fb950;
        height: auto;
        min-height: 14;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._player: Optional[object] = None

    def update_player(self, player: object) -> None:
        self._player = player
        self.refresh()

    def _build_badge_text(self) -> Text:
        result = Text()

        if self._player is None:
            result.append(" Awaiting hero...", style=Style(dim=True))
            return result

        p = self._player
        job_name = p.job.name if hasattr(p.job, "name") else str(p.job)
        race_name = p.race.name if hasattr(p.race, "name") else str(p.race)

        # ── Header ──
        result.append("\n")
        result.append("  \u2694 ", style=Style(color="#f0883e", bold=True))
        result.append(f"{p.name}", style=Style(bold=True, color="#58a6ff"))
        result.append(f"  the {race_name} {job_name}\n", style=Style(color="#8b949e"))

        # Level + XP
        result.append("  Lv.", style=Style(color="#8b949e"))
        result.append(f"{p.level}", style=Style(bold=True, color="#f0883e"))
        xp = getattr(p, "experience", 0)
        result.append(f"  XP: {xp}/100", style=Style(color="#e3b341"))

        # Position
        if hasattr(p, "position") and p.position:
            pos = p.position
            if isinstance(pos, list) and len(pos) == 2:
                from emberblast.utils import convert_number_to_letter

                pos_str = f"{convert_number_to_letter(pos[0])}{pos[1]}"
            else:
                pos_str = str(pos)
            result.append(f"  \u25c8 {pos_str}", style=Style(color="#58a6ff"))
        result.append("\n")

        # ── Bars ──
        result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))

        hp_bar = _build_bar(p.life, p.health_points, "HP")
        result.append_text(hp_bar)
        result.append("\n")

        mp_bar = _build_bar(p.mana, p.magic_points, "MP")
        result.append_text(mp_bar)
        result.append("\n")

        # XP bar
        xp_bar = _build_bar(xp, 100, "XP", color_override="#e3b341")
        result.append_text(xp_bar)
        result.append("\n")

        # ── Stats ──
        result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))

        stats = [
            ("STR", p.strength, "#f85149"),
            ("INT", p.intelligence, "#d2a8ff"),
            ("ACC", p.accuracy, "#e3b341"),
            ("ARM", p.armour, "#58a6ff"),
            ("RES", p.magic_resist, "#d2a8ff"),
            ("SPD", p.move_speed, "#3fb950"),
            ("WIL", p.will, "#f0883e"),
        ]
        for i, (name, val, color) in enumerate(stats):
            if i % 4 == 0:
                result.append("  ")
            result.append(f"{name}", style=Style(color="#6e7681"))
            result.append(f"{val:<3} ", style=Style(bold=True, color=color))
            if i % 4 == 3:
                result.append("\n")
        if len(stats) % 4 != 0:
            result.append("\n")

        # ── Equipment summary ──
        if hasattr(p, "equipment") and p.equipment:
            eq = p.equipment
            slots = []
            for slot in ("weapon", "armor", "helmet", "shield", "accessory"):
                item = getattr(eq, slot, None)
                if item and hasattr(item, "name"):
                    slots.append((slot[:3].upper(), item.name))
            if slots:
                result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))
                for abbr, item_name in slots:
                    result.append(f"  {abbr} ", style=Style(color="#6e7681"))
                    result.append(f"{item_name}\n", style=Style(color="#3fb950"))

        # ── Side effects ──
        if hasattr(p, "side_effects") and p.side_effects:
            result.append(" \u2500" * 15 + "\n", style=Style(color="#21262d"))
            for se in p.side_effects:
                se_name = se.name if hasattr(se, "name") else str(se)
                se_type = getattr(se, "effect_type", "buff")
                icon = "\u25b2" if se_type == "buff" else "\u25bc"
                color = "#3fb950" if se_type == "buff" else "#f85149"
                result.append(f"  {icon} {se_name}", style=Style(color=color))
                if hasattr(se, "duration"):
                    result.append(f" ({se.duration}t)", style=Style(color="#6e7681"))
                result.append("\n")

        return result

    def render(self) -> Text:
        return self._build_badge_text()
