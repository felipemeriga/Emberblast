import asyncio
from pathlib import Path
from typing import Dict, List, Union

from emberblast.interface.interface import IEquipmentItem, IItem, IPlayer, IQuestioningSystem, ISkill


class TextualQuestioner(IQuestioningSystem):
    """Async questioning system that bridges the game loop with a Textual UI.

    The game loop awaits answers via asyncio.Event. UI widgets call resolve()
    to provide the user's response and unblock the game loop.
    """

    def __init__(self, app) -> None:
        self._app = app
        self._response = None
        self._response_event = asyncio.Event()

    def resolve(self, value) -> None:
        """Called by UI widgets to provide the user's answer."""
        self._response = value
        self._response_event.set()

    async def _wait_for_response(self):
        """Block until resolve() is called, then return and reset."""
        await self._response_event.wait()
        self._response_event.clear()
        result = self._response
        self._response = None
        return result

    async def _ask(self, method_name: str, **kwargs):
        """Post question request to UI, then await the response."""
        self._app.handle_question(method_name, **kwargs)
        return await self._wait_for_response()

    async def ask_check_action(self, show_items: bool = False) -> Union[str, bool, list, str]:
        return await self._ask("ask_check_action", show_items=show_items)

    async def ask_actions_questions(self, actions_available: List[str]) -> Union[str, bool, list, str]:
        return await self._ask("ask_actions_questions", actions_available=actions_available)

    async def ask_enemy_to_check(self, enemies: List[IPlayer]) -> Union[str, bool, list, IPlayer]:
        return await self._ask("ask_enemy_to_check", enemies=enemies)

    async def ask_enemy_to_attack(
        self, enemies: List[IPlayer], skill_type: str = ""
    ) -> Union[str, bool, list, IPlayer]:
        return await self._ask("ask_enemy_to_attack", enemies=enemies, skill_type=skill_type)

    async def select_item(self, items: List[IItem]) -> Union[str, bool, list, IItem]:
        return await self._ask("select_item", items=items)

    async def confirm_item_selection(self) -> Union[str, bool, list, bool]:
        return await self._ask("confirm_item_selection")

    async def confirm_use_item_on_you(self) -> Union[str, bool, list, bool]:
        return await self._ask("confirm_use_item_on_you")

    async def display_equipment_choices(self, player: IPlayer) -> Union[str, bool, list, IEquipmentItem]:
        return await self._ask("display_equipment_choices", player=player)

    async def ask_attributes_to_improve(self) -> Union[str, bool, list, List]:
        return await self._ask("ask_attributes_to_improve")

    async def ask_where_to_move(self, possibilities: List[str]) -> Union[str, bool, list, str]:
        return await self._ask("ask_where_to_move", possibilities=possibilities)

    async def perform_first_question(self) -> Union[str, bool, list, str]:
        return await self._ask("perform_first_question")

    async def perform_game_create_questions(self) -> Union[str, bool, list, dict]:
        return await self._ask("perform_game_create_questions")

    async def select_skill(self, available_skills: List[ISkill]) -> Union[str, bool, list, ISkill]:
        return await self._ask("select_skill", available_skills=available_skills)

    async def get_saved_game(self, normalized_files: List[Dict]) -> Union[str, bool, list, Path]:
        return await self._ask("get_saved_game", normalized_files=normalized_files)

    async def perform_character_creation_questions(
        self, existing_names: List[str]
    ) -> Union[str, bool, list, dict]:
        return await self._ask("perform_character_creation_questions", existing_names=existing_names)
