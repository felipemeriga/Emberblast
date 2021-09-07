from typing import Callable

from .test import BaseTestCase, manual_test
from .test_map import mock_map
from project.game import bot_factory, DeathMatch
from project.orchestrator import DeathMatchOrchestrator


@mock_map()
def mock_game() -> Callable:
    def wrapper(func):
        bots = bot_factory(5)
        game = DeathMatch(bots[0], bots[1:], mock_game.mock_map)
        setattr(func, 'mock_game', game)
        return func

    return wrapper


@manual_test
@mock_game()
class TestModuleGame(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestModuleGame, self).__init__(*args, **kwargs)

    def test_bots_automated_game(self) -> None:
        game_orchestrator = DeathMatchOrchestrator(self.mock_game)
        game_orchestrator.execute_game()