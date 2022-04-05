import os
from unittest import skipIf

from .test import CommunicatorTestCase, manual_test
from .test_player import mock_player
from emberblast.communicator import communicator_injector
from .test_item import mock_healing_item, mock_recovery_item, mock_equipment_item
from .test_map import mock_map
from emberblast.interface import IItem, IEquipmentItem, IPlayer

# All of the test under this test file are meant to be run manually only, for testing each of the
# communicator asked in the game


@manual_test
@mock_player()
@mock_map()
@mock_healing_item()
@mock_recovery_item()
@mock_equipment_item()
@communicator_injector()
class TestModuleQuestions(CommunicatorTestCase):
    def test_module(self) -> None:
        pass

    def test_ask_check_action(self) -> None:
        result = self.communicator.questioner.ask_check_action()
        assert isinstance(result, str)

    def test_ask_actions_questions(self) -> None:
        result = self.communicator.questioner.ask_actions_questions(['move', 'attack', 'skill', 'defend',
                                        'hide', 'search', 'item', 'equip', 'drop',
                                        'check', 'pass'])
        assert isinstance(result, str)

    def test_select_item(self):
        items = [self.mock_equipment_item, self.mock_healing_item, self.mock_recovery_item]
        result = self.communicator.questioner.select_item(items)
        assert isinstance(result, IItem)

    def test_ask_enemy_to_check(self) -> None:
        result = self.questioning_system.enemies_questioner.ask_enemy_to_check([self.mock_player])
        assert isinstance(result, IPlayer)

    def test_confirm_item_selection(self) -> None:
        result = self.communicator.questioner.confirm_item_selection()
        assert isinstance(result, bool)

    def test_confirm_use_item_on_you(self) -> None:
        result = self.communicator.questioner.confirm_use_item_on_you()
        assert isinstance(result, bool)

    def test_display_equipment_choices(self) -> None:
        self.mock_player.bag.add_item(self.mock_equipment_item)
        result = self.communicator.questioner.display_equipment_choices(self.mock_player)
        assert isinstance(result, IEquipmentItem)

    def test_ask_where_to_move(self) -> None:
        possibilities = self.mock_map.graph.get_available_nodes_in_range("A0", 5)
        result = self.questioning_system.movement_questioner.ask_where_to_move(possibilities)
        assert isinstance(result, str)

    def test_perform_game_create_questions(self) -> None:
        result = self.questioning_system.new_game_questioner.perform_game_create_questions()
        assert isinstance(result, dict)

    def test_perform_first_question(self) -> None:
        result = self.questioning_system.new_game_questioner.perform_first_question()
        assert isinstance(result, str)

    def test_ask_attributes_to_improve(self) -> None:
        result = self.questioning_system.level_up_questioner.ask_attributes_to_improve()
        assert isinstance(result, list)
