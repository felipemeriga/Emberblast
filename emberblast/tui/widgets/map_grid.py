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

# Terrain rendering: (symbol, foreground, background)
_TERRAIN_STYLE: Dict[str, tuple] = {
    "plains": (" ∙∙ ", "#484f58", "#1a1e24"),
    "wall": (" ██ ", "#6e7681", "#2d333b"),
    "water": (" ~~ ", "#58a6ff", "#0c2d4a"),
    "mountain": (" /\\ ", "#f0883e", "#2a1a0a"),
    "forest": (" ♣♣ ", "#3fb950", "#0a2a0f"),
}

# Cell width must match symbol length
CELL_WIDTH = 4


class MapWidget(Widget):
    """Renders a grid map with terrain, players, and highlights."""

    DEFAULT_CSS = """
    MapWidget {
        background: #0d1117;
        padding: 1;
        border: solid #f0883e;
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
        """Update the map data and trigger a refresh."""
        self._matrix = matrix
        self._grid_size = size
        self._players = players
        self._active_player_name = active_player_name
        self._friendly_names = friendly_names
        self._flash_cells = flash_cells or set()
        self._highlight_cells = highlight_cells or set()
        self.refresh()

    def _build_grid_text(self) -> Text:
        """Build a Rich Text object representing the full grid."""
        if not self._matrix or self._grid_size == 0:
            return Text("No map data")

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

        # Column headers
        result.append("     ")
        for col in range(self._grid_size):
            result.append(f" {col:^3}", style=Style(bold=True, color="#6e7681"))
        result.append("\n")

        # Top border
        result.append("   ┌─")
        result.append("────" * self._grid_size)
        result.append("┐\n", style=Style(color="#f0883e"))

        for row in range(self._grid_size):
            row_label = convert_number_to_letter(row)
            result.append(f" {row_label} │ ", style=Style(bold=True, color="#6e7681"))

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
                    result.append(f" {token} ", style=style)
                elif cell_value == 0:
                    result.append("    ")
                else:
                    terrain_name = _VALUE_TO_TERRAIN.get(cell_value, "plains")
                    symbol, fg, bg = _TERRAIN_STYLE.get(terrain_name, _TERRAIN_STYLE["plains"])

                    if position_str in self._flash_cells:
                        style = Style(color="#000000", bgcolor="#00ffff", bold=True)
                    elif position_str in self._highlight_cells:
                        style = Style(color="#00ffff", bgcolor="#1a4040", bold=True)
                    else:
                        style = Style(color=fg, bgcolor=bg)

                    result.append(symbol, style=style)

            result.append("│\n", style=Style(color="#f0883e"))

        # Bottom border
        result.append("   └─")
        result.append("────" * self._grid_size)
        result.append("┘\n", style=Style(color="#f0883e"))

        # Legend
        result.append("\n ")
        for p in self._players:
            if hasattr(p, "is_alive") and not p.is_alive():
                continue
            job_name = p.job.name if hasattr(p.job, "name") else str(p.job)
            token = get_player_token(p.name, job_name)
            is_friendly = p.name in self._friendly_names
            team = "friendly" if is_friendly else "enemy"
            colors = TEAM_COLORS[team]
            result.append(f" {token}", style=Style(color=colors["fg"], bgcolor=colors["bg"], bold=True))
            result.append(f"={p.name}", style=Style(color="#8b949e"))
            result.append("  ")

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_grid_text()
