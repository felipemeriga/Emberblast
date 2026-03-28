"""Map grid widget for the Textual TUI."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from rich.style import Style
from rich.text import Text
from textual.widget import Widget

from emberblast.tui.styles import (
    TEAM_COLORS,
    TERRAIN_COLORS,
    get_player_token,
    get_terrain_cell,
)
from emberblast.utils import convert_number_to_letter

# Map matrix integer values to terrain type names.
# 0 is always void; 1 defaults to plains.
_VALUE_TO_TERRAIN: Dict[int, str] = {
    1: "plains",
    2: "wall",
    3: "water",
    4: "mountain",
    5: "forest",
}


class MapWidget(Widget):
    """Renders a grid map with terrain, players, and highlights."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._matrix: List[List[int]] = []
        self._size: int = 0
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
        self._size = size
        self._players = players
        self._active_player_name = active_player_name
        self._friendly_names = friendly_names
        self._flash_cells = flash_cells or set()
        self._highlight_cells = highlight_cells or set()
        self.refresh()

    def _build_grid_text(self) -> Text:
        """Build a Rich Text object representing the full grid."""
        if not self._matrix or self._size == 0:
            return Text("No map data")

        # Index players by (row, col) for fast lookup
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
        result.append("   ")
        for col in range(self._size):
            header = f"{col:>2} "
            result.append(header, style=Style(bold=True, dim=True))
        result.append("\n")

        # Rows
        for row in range(self._size):
            row_label = convert_number_to_letter(row)
            result.append(f"{row_label}  ", style=Style(bold=True, dim=True))

            for col in range(self._size):
                cell_value = self._matrix[row][col]
                position_key = (row, col)
                position_str = f"{row_label}{col}"

                # Check for players at this position
                players_here = player_positions.get(position_key, [])

                if players_here:
                    player = players_here[0]
                    job_name = player.job.name if hasattr(player.job, "name") else str(player.job)
                    token = get_player_token(player.name, job_name)
                    is_friendly = player.name in self._friendly_names
                    team = "friendly" if is_friendly else "enemy"
                    colors = TEAM_COLORS[team]
                    style = Style(
                        color=colors["fg"],
                        bgcolor=colors["bg"],
                        bold=True,
                        blink=player.name == self._active_player_name,
                    )
                    result.append(f"{token} ", style=style)
                elif cell_value == 0:
                    # Void cell
                    result.append("   ")
                else:
                    terrain_name = _VALUE_TO_TERRAIN.get(cell_value, "plains")
                    symbol = get_terrain_cell(terrain_name)
                    color = TERRAIN_COLORS.get(terrain_name, TERRAIN_COLORS["plains"])

                    style_kwargs: dict = {"color": color}
                    if position_str in self._highlight_cells:
                        style_kwargs["underline"] = True
                    if position_str in self._flash_cells:
                        style_kwargs["bold"] = True
                        style_kwargs["reverse"] = True

                    result.append(f"{symbol} ", style=Style(**style_kwargs))

            result.append("\n")

        return result

    def render(self) -> Text:
        """Render the widget content."""
        return self._build_grid_text()
