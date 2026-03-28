"""Map grid widget for the Textual TUI."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

from emberblast.tui.styles import (
    TEAM_COLORS,
    get_player_token,
)
from emberblast.utils import convert_number_to_letter

# Map matrix integer values to terrain type names.
_VALUE_TO_TERRAIN: Dict[int, str] = {
    1: "plains",
    2: "wall",
    3: "water",
    4: "mountain",
    5: "forest",
}

# Terrain rendering: (symbol, foreground, background) — 6-char wide cells
_TERRAIN_STYLE: Dict[str, tuple] = {
    "plains": ("  \u00b7\u00b7  ", "#484f58", "#131820"),
    "wall": ("  \u2588\u2588  ", "#6e7681", "#2d333b"),
    "water": ("  \u2248\u2248  ", "#58a6ff", "#0a2240"),
    "mountain": ("  /\\  ", "#f0883e", "#2a1a0a"),
    "forest": ("  \u2663\u2663  ", "#3fb950", "#0a2a0f"),
}

# Highlight terrain symbols (replace symbol with directional markers)
_HIGHLIGHT_SYMBOL = "  \u25aa\u25aa  "
_FLASH_SYMBOL = "  \u25c6\u25c6  "

CELL_WIDTH = 6


class MapWidget(Widget):
    """Renders a grid map with terrain, players, and highlights."""

    DEFAULT_CSS = """
    MapWidget {
        background: #0d1117;
        padding: 0 1;
        border: tall #f0883e;
        height: 1fr;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._matrix: List[List[int]] = []
        self._grid_size: int = 0
        self._players: list = []
        self._active_player_name: str = ""
        self._friendly_names: Set[str] = set()
        self._flash_cells: Set[str] = set()
        self._highlight_cells: Set[str] = set()

    def update_map(
        self,
        matrix: List[List[int]],
        size: int,
        players: list,
        active_player_name: str,
        friendly_names: Set[str],
        flash_cells: Optional[Set[str]] = None,
        highlight_cells: Optional[Set[str]] = None,
    ) -> None:
        self._matrix = matrix
        self._grid_size = size
        self._players = players
        self._active_player_name = active_player_name
        self._friendly_names = friendly_names
        self._flash_cells = flash_cells or set()
        self._highlight_cells = highlight_cells or set()
        self.refresh()

    def _build_grid_text(self) -> Text:
        if not self._matrix or self._grid_size == 0:
            return Text("  No map data")

        # Index players by (row, col)
        player_positions: Dict[tuple, list] = {}
        for p in self._players:
            if hasattr(p, "is_alive") and not p.is_alive():
                continue
            pos = p.position
            if isinstance(pos, list) and len(pos) == 2:
                key = (pos[0], pos[1])
            elif isinstance(pos, str) and len(pos) >= 2:
                row_letter = pos[0].upper()
                col = int(pos[1:])
                key = (ord(row_letter) - ord("A"), col)
            else:
                continue
            player_positions.setdefault(key, []).append(p)

        result = Text()
        border_color = "#f0883e"
        border_style = Style(color=border_color)
        header_style = Style(bold=True, color="#6e7681")

        # Column headers
        result.append("\n")
        result.append("       ")
        for col in range(self._grid_size):
            result.append(f"  {col:<4}", style=header_style)
        result.append("\n")

        # Top border — heavy double-line
        result.append("     \u2554", style=border_style)
        result.append("\u2550" * (CELL_WIDTH * self._grid_size + 1), style=border_style)
        result.append("\u2557\n", style=border_style)

        for row in range(self._grid_size):
            row_label = convert_number_to_letter(row)

            # Main cell row
            result.append(f"   {row_label} \u2551", style=Style(bold=True, color="#8b949e"))

            for col in range(self._grid_size):
                cell_value = self._matrix[row][col]
                position_key = (row, col)
                position_str = f"{row_label}{col}"
                players_here = player_positions.get(position_key, [])

                if players_here:
                    player = players_here[0]
                    job_name = player.job.name if hasattr(player.job, "name") else str(player.job)
                    token = get_player_token(player.name, job_name)
                    is_friendly = player.name in self._friendly_names
                    team = "friendly" if is_friendly else "enemy"
                    colors = TEAM_COLORS[team]
                    is_active = player.name == self._active_player_name
                    style = Style(
                        color=colors["fg"],
                        bgcolor=colors["bg"],
                        bold=True,
                        blink=is_active,
                    )
                    result.append(f" [{token}] ", style=style)
                elif cell_value == 0:
                    result.append(" " * CELL_WIDTH)
                else:
                    terrain_name = _VALUE_TO_TERRAIN.get(cell_value, "plains")
                    symbol, fg, bg = _TERRAIN_STYLE.get(terrain_name, _TERRAIN_STYLE["plains"])

                    if position_str in self._flash_cells:
                        style = Style(color="#000000", bgcolor="#00ffff", bold=True)
                        result.append(_FLASH_SYMBOL, style=style)
                    elif position_str in self._highlight_cells:
                        style = Style(color="#00ffff", bgcolor="#1a3a3a", bold=True)
                        result.append(_HIGHLIGHT_SYMBOL, style=style)
                    else:
                        style = Style(color=fg, bgcolor=bg)
                        result.append(symbol, style=style)

            result.append("\u2551\n", style=border_style)

            # Spacing row between grid rows (half-height visual separator)
            if row < self._grid_size - 1:
                result.append("     \u2551", style=border_style)
                for col in range(self._grid_size):
                    cell_value = self._matrix[row][col]
                    terrain_name = _VALUE_TO_TERRAIN.get(cell_value, "plains")
                    _, _, bg = _TERRAIN_STYLE.get(terrain_name, _TERRAIN_STYLE["plains"])
                    # Subtle row separator
                    result.append("\u2500" * CELL_WIDTH, style=Style(color="#21262d"))
                result.append("\u2551\n", style=border_style)

        # Bottom border
        result.append("     \u255a", style=border_style)
        result.append("\u2550" * (CELL_WIDTH * self._grid_size + 1), style=border_style)
        result.append("\u255d\n", style=border_style)

        # Legend — player tokens
        result.append("     ")
        for p in self._players:
            if hasattr(p, "is_alive") and not p.is_alive():
                continue
            job_name = p.job.name if hasattr(p.job, "name") else str(p.job)
            token = get_player_token(p.name, job_name)
            is_friendly = p.name in self._friendly_names
            team = "friendly" if is_friendly else "enemy"
            colors = TEAM_COLORS[team]
            result.append(f"[{token}]", style=Style(color=colors["fg"], bgcolor=colors["bg"], bold=True))
            result.append(f" {p.name}", style=Style(color="#8b949e"))
            result.append("  ")
        result.append("\n")

        return result

    def render(self) -> Text:
        return self._build_grid_text()
