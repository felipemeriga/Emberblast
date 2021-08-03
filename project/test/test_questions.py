import os
from pathlib import Path
from unittest import skipIf

from .test import BaseTestCase
from .test_player import mock_player
from project.questions import ask_check_action, ask_actions_questions, select_item, ask_enemy_to_check, \
    confirm_item_selection, confirm_use_item_on_you, display_equipment_choices, ask_where_to_move, \
    perform_game_create_questions, perform_first_question, ask_attributes_to_improve
from .test_item import mock_healing_item, mock_recovery_item, mock_equipment_item
from .test_map import mock_map
from project.item import Item, EquipmentItem

# All of the test under this test file are meant to be run manually only, for testing each of the
# questions asked in the game
from ..player import Player


def manual_test(func):
    return skipIf('MANUAL_TESTS' not in os.environ, 'Skipping slow test')(func)


@manual_test
@mock_player()
@mock_map()
@mock_healing_item()
@mock_recovery_item()
@mock_equipment_item()
class TestModuleQuestions(BaseTestCase):
    def test_module(self) -> None:
        pass

    def test_ask_check_action(self) -> None:
        result = ask_check_action()
        assert isinstance(result, str)

    def test_ask_actions_questions(self) -> None:
        result = ask_actions_questions(['move', 'attack', 'skill', 'defend',
                                        'hide', 'search', 'item', 'equip', 'drop',
                                        'check', 'pass'])
        assert isinstance(result, str)

    def test_select_item(self):
        items = [self.mock_equipment_item, self.mock_healing_item, self.mock_recovery_item]
        result = select_item(items)
        assert isinstance(result, Item)

    def test_ask_enemy_to_check(self) -> None:
        result = ask_enemy_to_check([self.mock_player])
        assert isinstance(result, Player)

    def test_confirm_item_selection(self) -> None:
        result = confirm_item_selection()
        assert isinstance(result, bool)

    def test_confirm_use_item_on_you(self) -> None:
        result = confirm_use_item_on_you()
        assert isinstance(result, bool)

    def test_display_equipment_choices(self) -> None:
        self.mock_player.bag.add_item(self.mock_equipment_item)
        result = display_equipment_choices(self.mock_player)
        assert isinstance(result, EquipmentItem)

    def test_ask_where_to_move(self) -> None:
        possibilities = self.mock_map.graph.get_available_nodes_in_range("A0", 5)
        result = ask_where_to_move(possibilities)
        assert isinstance(result, str)

    def test_perform_game_create_questions(self) -> None:
        result = perform_game_create_questions()
        assert isinstance(result, dict)

    def test_perform_first_question(self) -> None:
        result = perform_first_question()
        assert isinstance(result, str)

    def test_ask_attributes_to_improve(self) -> None:
        result = ask_attributes_to_improve()
        assert isinstance(result, list)
