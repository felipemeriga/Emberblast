import os
from unittest import skipIf

from .test import BaseTestCase
from .test_player import mock_player
from project.questions import ask_check_action, ask_actions_questions, select_item
from .test_item import mock_healing_item, mock_recovery_item, mock_equipment_item
from ..item import Item


# All of the test under this test file are meant to be run manually only, for testing each of the
# questions asked in the game
def manual_test(func):
    return skipIf('MANUAL_TESTS' not in os.environ, 'Skipping slow test')(func)


@manual_test
@mock_player()
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

    def test_ask_enemy_to_check(self):
        items = [self.mock_equipment_item, self.mock_healing_item, self.mock_recovery_item]
        result = select_item(items)
        assert isinstance(result, Item)
