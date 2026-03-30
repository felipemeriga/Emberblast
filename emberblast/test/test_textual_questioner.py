import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


class TestTextualQuestioner(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = MagicMock()
        # Make push_screen and pop_screen async-compatible for multi-step methods
        self.app.push_screen = AsyncMock()
        self.app.pop_screen = MagicMock()
        from emberblast.tui.questioner import TextualQuestioner

        self.questioner = TextualQuestioner(self.app)

    async def test_resolve_unblocks_wait_for_response(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve("some_value")

        asyncio.create_task(resolver())
        result = await self.questioner._wait_for_response()
        self.assertEqual(result, "some_value")

    async def test_response_cleared_after_wait(self):
        self.questioner.resolve("first")
        result = await self.questioner._wait_for_response()
        self.assertEqual(result, "first")
        self.assertIsNone(self.questioner._response)
        self.assertFalse(self.questioner._response_event.is_set())

    async def test_ask_check_action(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve("stats")

        asyncio.create_task(resolver())
        result = await self.questioner.ask_check_action(show_items=True)
        self.assertEqual(result, "stats")
        self.app.handle_question.assert_called_once_with("ask_check_action", show_items=True)

    async def test_ask_actions_questions(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve("attack")

        asyncio.create_task(resolver())
        result = await self.questioner.ask_actions_questions(actions_available=["attack", "move"])
        self.assertEqual(result, "attack")
        self.app.handle_question.assert_called_once_with("ask_actions_questions", actions_available=["attack", "move"])

    async def test_ask_enemy_to_check(self):
        enemies = [MagicMock(), MagicMock()]

        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(enemies[0])

        asyncio.create_task(resolver())
        result = await self.questioner.ask_enemy_to_check(enemies=enemies)
        self.assertEqual(result, enemies[0])
        self.app.handle_question.assert_called_once_with("ask_enemy_to_check", enemies=enemies)

    async def test_ask_enemy_to_attack(self):
        enemies = [MagicMock()]

        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(enemies[0])

        asyncio.create_task(resolver())
        result = await self.questioner.ask_enemy_to_attack(enemies=enemies, skill_type="melee")
        self.assertEqual(result, enemies[0])
        self.app.handle_question.assert_called_once_with("ask_enemy_to_attack", enemies=enemies, skill_type="melee")

    async def test_select_item(self):
        items = [MagicMock()]

        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(items[0])

        asyncio.create_task(resolver())
        result = await self.questioner.select_item(items=items)
        self.assertEqual(result, items[0])
        self.app.handle_question.assert_called_once_with("select_item", items=items)

    async def test_confirm_item_selection(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(True)

        asyncio.create_task(resolver())
        result = await self.questioner.confirm_item_selection()
        self.assertTrue(result)
        self.app.handle_question.assert_called_once_with("confirm_item_selection")

    async def test_confirm_use_item_on_you(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(False)

        asyncio.create_task(resolver())
        result = await self.questioner.confirm_use_item_on_you()
        self.assertFalse(result)
        self.app.handle_question.assert_called_once_with("confirm_use_item_on_you")

    async def test_display_equipment_choices(self):
        player = MagicMock()
        equipment = MagicMock()

        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(equipment)

        asyncio.create_task(resolver())
        result = await self.questioner.display_equipment_choices(player=player)
        self.assertEqual(result, equipment)
        self.app.handle_question.assert_called_once_with("display_equipment_choices", player=player)

    async def test_ask_attributes_to_improve(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(["strength", "accuracy"])

        asyncio.create_task(resolver())
        result = await self.questioner.ask_attributes_to_improve()
        self.assertEqual(result, ["strength", "accuracy"])
        self.app.handle_question.assert_called_once_with("ask_attributes_to_improve")

    async def test_ask_where_to_move(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve("B1")

        asyncio.create_task(resolver())
        result = await self.questioner.ask_where_to_move(possibilities=["A1", "B1"])
        self.assertEqual(result, "B1")
        self.app.handle_question.assert_called_once_with("ask_where_to_move", possibilities=["A1", "B1"])

    async def test_perform_first_question(self):
        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve("new_game")

        asyncio.create_task(resolver())
        result = await self.questioner.perform_first_question()
        self.assertEqual(result, "new_game")
        self.app.handle_question.assert_called_once_with("perform_first_question")

    async def test_perform_game_create_questions(self):
        """Multi-step: resolves 4 sub-questions into a dict."""
        answers = ["Deathmatch", "Millstone Plains", "1", "4"]
        call_count = 0

        async def resolver():
            nonlocal call_count
            for answer in answers:
                await asyncio.sleep(0.1)
                self.questioner.resolve(answer)
                call_count += 1

        asyncio.create_task(resolver())
        result = await self.questioner.perform_game_create_questions()
        self.assertEqual(result["game"], "Deathmatch")
        self.assertEqual(result["map"], "Millstone Plains")
        self.assertEqual(result["controlled_players_number"], "1")
        self.assertEqual(result["bots_number"], "4")
        self.assertEqual(call_count, 4)

    async def test_select_skill(self):
        skills = [MagicMock()]

        async def resolver():
            await asyncio.sleep(0.01)
            self.questioner.resolve(skills[0])

        asyncio.create_task(resolver())
        result = await self.questioner.select_skill(available_skills=skills)
        self.assertEqual(result, skills[0])
        self.app.handle_question.assert_called_once_with("select_skill", available_skills=skills)

    async def test_get_saved_game(self):
        """Uses _ask_setup_list to show saved games."""
        from pathlib import Path

        files = [{"path": Path("/save1"), "name": "Save 1"}]

        async def resolver():
            await asyncio.sleep(0.1)
            self.questioner.resolve(Path("/save1"))

        asyncio.create_task(resolver())
        result = await self.questioner.get_saved_game(normalized_files=files)
        self.assertEqual(result, Path("/save1"))
        # Should have pushed and popped a setup screen
        self.app.push_screen.assert_called_once()
        self.app.pop_screen.assert_called_once()

    @patch("emberblast.conf.get_configuration")
    async def test_perform_character_creation_questions(self, mock_get_config):
        """Multi-step: resolves name, race, job into a dict."""
        mock_get_config.return_value = {"Elf": {}, "Orc": {}, "Human": {}}

        answers = ["Hero", "Elf", "Knight"]
        call_count = 0

        async def resolver():
            nonlocal call_count
            for answer in answers:
                await asyncio.sleep(0.1)
                self.questioner.resolve(answer)
                call_count += 1

        asyncio.create_task(resolver())
        result = await self.questioner.perform_character_creation_questions(existing_names=["Bot1"])
        self.assertEqual(result["nickname"], "Hero")
        self.assertEqual(result["race"], "Elf")
        self.assertEqual(result["job"], "Knight")
        self.assertEqual(call_count, 3)

    async def test_multiple_sequential_questions(self):
        """Verify questioner can handle multiple questions in sequence."""

        async def resolver1():
            await asyncio.sleep(0.01)
            self.questioner.resolve("attack")

        asyncio.create_task(resolver1())
        result1 = await self.questioner.ask_actions_questions(actions_available=["attack"])
        self.assertEqual(result1, "attack")

        async def resolver2():
            await asyncio.sleep(0.01)
            self.questioner.resolve("B1")

        asyncio.create_task(resolver2())
        result2 = await self.questioner.ask_where_to_move(possibilities=["B1"])
        self.assertEqual(result2, "B1")
