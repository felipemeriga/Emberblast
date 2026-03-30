"""Game over screen with victory banner and menu."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

MENU_ITEMS = ["Play Again", "Quit"]


class GameOverScreen(Screen):
    """Displays a victory banner and play again / quit menu."""

    def __init__(self, winner_name: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self._winner_name = winner_name
        self._menu_index: int = 0

    def compose(self) -> ComposeResult:
        banner = f"\u2728 VICTORY! \u2728\n\n{self._winner_name} has won the battle!"
        yield Static(banner, id="victory-banner")
        yield Static(self._build_menu_text(), id="game-over-menu")

    def _build_menu_text(self) -> str:
        lines = []
        for i, item in enumerate(MENU_ITEMS):
            prefix = "\u25b6 " if i == self._menu_index else "  "
            lines.append(f"{prefix}{item}")
        return "\n".join(lines)

    def _refresh_menu(self) -> None:
        try:
            menu = self.query_one("#game-over-menu", Static)
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
            if selected == "Quit":
                self.app.exit()
            elif selected == "Play Again":
                self.app.exit(result="play_again")
