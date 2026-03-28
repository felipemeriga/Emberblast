"""Setup screen for game creation and character creation questions."""

from __future__ import annotations

from typing import Any, Optional

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Static


class SetupScreen(Screen):
    """Multi-purpose screen handling game creation and character creation flows.

    Supports list navigation for selections and text input via Textual Input widget.
    Resolves answers through the questioner when the user completes their selection.
    """

    def __init__(self, question_type: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self._questioner: Any = None
        self._question_type: str = question_type

        # Interaction state
        self._mode: str = "idle"  # idle | list | input
        self._choices: list = []
        self._choice_labels: list = []
        self._choice_index: int = 0
        self._prompt_text: str = ""
        self._on_resolve: Any = None  # callback after resolve

    def compose(self) -> ComposeResult:
        yield Static("", id="setup-title")
        yield Static("", id="setup-prompt")
        yield Static("", id="setup-choices")
        yield Input(placeholder="Type here...", id="setup-input")

    def on_mount(self) -> None:
        """Hide the input widget initially."""
        try:
            inp = self.query_one("#setup-input", Input)
            inp.display = False
        except Exception:
            pass

    def set_questioner(self, questioner: Any) -> None:
        """Wire the questioner."""
        self._questioner = questioner

    def show_list(
        self,
        prompt: str,
        choices: list,
        labels: Optional[list] = None,
    ) -> None:
        """Display a navigable list of choices."""
        self._mode = "list"
        self._prompt_text = prompt
        self._choices = list(choices)
        self._choice_labels = list(labels) if labels else [str(c) for c in choices]
        self._choice_index = 0

        try:
            title = self.query_one("#setup-title", Static)
            title.update(prompt)
        except Exception:
            pass

        try:
            inp = self.query_one("#setup-input", Input)
            inp.display = False
        except Exception:
            pass

        self._refresh_choices_display()

    def show_input(self, prompt: str, placeholder: str = "Type here...") -> None:
        """Display a text input for the user."""
        self._mode = "input"
        self._prompt_text = prompt

        try:
            title = self.query_one("#setup-title", Static)
            title.update(prompt)
        except Exception:
            pass

        try:
            choices_widget = self.query_one("#setup-choices", Static)
            choices_widget.update("")
        except Exception:
            pass

        try:
            inp = self.query_one("#setup-input", Input)
            inp.display = True
            inp.value = ""
            inp.placeholder = placeholder
            inp.focus()
        except Exception:
            pass

    def _refresh_choices_display(self) -> None:
        """Update the choices display."""
        try:
            choices_widget = self.query_one("#setup-choices", Static)
            lines = []
            for i, label in enumerate(self._choice_labels):
                prefix = "\u25b6 " if i == self._choice_index else "  "
                lines.append(f"{prefix}{label}")
            choices_widget.update("\n".join(lines))
        except Exception:
            pass

    def on_key(self, event) -> None:
        """Handle keyboard input for list navigation."""
        key = event.key.lower() if hasattr(event, "key") else ""

        if self._mode == "list":
            self._handle_list_key(key)

    def _handle_list_key(self, key: str) -> None:
        """Navigate and select from the list."""
        if key in ("up", "k"):
            if self._choice_index > 0:
                self._choice_index -= 1
                self._refresh_choices_display()
        elif key in ("down", "j"):
            if self._choice_index < len(self._choices) - 1:
                self._choice_index += 1
                self._refresh_choices_display()
        elif key == "enter":
            if self._choices:
                selected = self._choices[self._choice_index]
                self._mode = "idle"
                if self._questioner:
                    self._questioner.resolve(selected)
        elif key == "escape":
            self._mode = "idle"
            if self._questioner:
                self._questioner.resolve(False)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle text input submission."""
        if self._mode == "input":
            value = event.value.strip()
            if value:
                self._mode = "idle"
                try:
                    inp = self.query_one("#setup-input", Input)
                    inp.display = False
                except Exception:
                    pass
                if self._questioner:
                    self._questioner.resolve(value)
