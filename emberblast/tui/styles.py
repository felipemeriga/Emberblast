"""Shared visual constants for the Textual TUI."""

TERRAIN_SYMBOLS: dict[str, str] = {
    "plains": "░░",
    "wall": "██",
    "water": "~~",
    "mountain": "^^",
    "forest": "**",
}

TERRAIN_COLORS: dict[str, str] = {
    "plains": "#484f58",
    "wall": "#6e7681",
    "water": "#58a6ff",
    "mountain": "#f0883e",
    "forest": "#3fb950",
}

TEAM_COLORS: dict[str, dict[str, str]] = {
    "friendly": {"fg": "#3fb950", "bg": "#1a6334"},
    "enemy": {"fg": "#f85149", "bg": "#6e2d1a"},
}

LOG_COLORS: dict[str, str] = {
    "damage": "#f85149",
    "heal": "#3fb950",
    "narration": "#f0883e",
    "move": "#58a6ff",
    "system": "#8b949e",
    "mana": "#d2a8ff",
    "death": "#f85149",
    "xp": "#e3b341",
    "item": "#3fb950",
    "turn": "#f0883e",
    "skill": "#d2a8ff",
    "dice": "#e3b341",
    "critical": "#ff7b72",
    "victory": "#3fb950",
    "side_effect": "#d2a8ff",
    "trap": "#f85149",
    "info": "#8b949e",
    "miss": "#6e7681",
    "warning": "#e3b341",
    "level_up": "#3fb950",
    "action": "#58a6ff",
    "stats": "#8b949e",
}

ACTION_COLORS: dict[str, str] = {
    "move": "#58a6ff",
    "attack": "#f85149",
    "skill": "#d2a8ff",
    "defend": "#3fb950",
    "item": "#f0883e",
    "hide": "#8b949e",
    "search": "#e3b341",
    "equip": "#58a6ff",
    "drop": "#f85149",
    "check": "#8b949e",
    "pass": "#6e7681",
}

BG_COLOR = "#0d1117"
PANEL_BG = "#161b22"
BORDER_COLOR = "#30363d"
BOT_TURN_DELAY = 0.5


def get_player_token(name: str, job_name: str) -> str:
    """Return a 2-character uppercase token from the player name and job."""
    return (name[0] + job_name[0]).upper()


def get_terrain_cell(terrain_type: str) -> str:
    """Return the 2-char symbol for a terrain type, defaulting to plains."""
    return TERRAIN_SYMBOLS.get(terrain_type, TERRAIN_SYMBOLS["plains"])
