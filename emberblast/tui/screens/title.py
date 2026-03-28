"""Title screen with ASCII logo and main menu."""

from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

LOGO = r"""
 ______          _               _     _           _
|  ____|        | |             | |   | |         | |
| |__   _ __ ___ | |__   ___ _ __| |__ | | __ _ ___| |_
|  __| | '_ ` _ \| '_ \ / _ \ '__| '_ \| |/ _` / __| __|
| |____| | | | | | |_) |  __/ |  | |_) | | (_| \__ \ |_
|______|_| |_| |_|_.__/ \___|_|  |_.__/|_|\__,_|___/\__|
"""

MENU_ITEMS = ["New Game", "Continue", "Quit"]

_MENU_RESULT = {
    "New Game": "new",
    "Continue": "continue",
    "Quit": "quit",
}


class TitleScreen(Screen):
    """Title screen with ASCII logo and navigable menu."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._questioner: Any = None
        self._menu_index: int = 0

    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="title-logo")
        yield Static(self._build_menu_text(), id="title-menu")

    def set_questioner(self, questioner: Any) -> None:
        """Wire the questioner."""
        self._questioner = questioner

    def _build_menu_text(self) -> str:
        lines = []
        for i, item in enumerate(MENU_ITEMS):
            prefix = "\u25b6 " if i == self._menu_index else "  "
            lines.append(f"{prefix}{item}")
        return "\n".join(lines)

    def _refresh_menu(self) -> None:
        try:
            menu = self.query_one("#title-menu", Static)
            menu.update(self._build_menu_text())
        except Exception:
            pass

    def on_key(self, event) -> None:
        key = event.key.lower() if hasattr(event, "key") else ""

        if key in ("up", "k"):
            if self._menu_index > 0:
                self._menu_index -= 1
                self._refresh_menu()
        elif key in ("down", "j"):
            if self._menu_index < len(MENU_ITEMS) - 1:
                self._menu_index += 1
                self._refresh_menu()
        elif key == "enter":
            selected = MENU_ITEMS[self._menu_index]
            result = _MENU_RESULT[selected]
            if result == "quit":
                self.app.exit()
            elif self._questioner:
                self._questioner.resolve(result)
