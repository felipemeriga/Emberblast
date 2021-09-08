from typing import Callable

from .test_game import mock_game
from .test import BaseTestCase, manual_test
from project.action import Move, Hide, Attack, Item, Drop, Pass, Defend, Search, Skill, Equip, Check


@mock_game()
def mock_actions() -> Callable:
    def wrapper(func):
        actions = {'move': Move(True, False, mock_actions.mock_game),
                   'defend': Defend(False, False, mock_actions.mock_game),
                   'hide': Hide(False, False, mock_actions.mock_game),
                   'search': Search(True, False, mock_actions.mock_game),
                   'attack': Attack(False, False, mock_actions.mock_game),
                   'skill': Skill(False, False, mock_actions.mock_game),
                   'item': Item(False, False, mock_actions.mock_game),
                   'equip': Equip(True, True, mock_actions.mock_game),
                   'drop': Drop(True, True, mock_actions.mock_game),
                   'check': Check(True, True, mock_actions.mock_game),
                   'pass': Pass(True, False, mock_actions.mock_game)}
        setattr(func, 'mock_actions', actions)
        return func

    return wrapper


@manual_test
@mock_actions()
class TestModuleActions(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestModuleActions, self).__init__(*args, **kwargs)
