from typing import Callable

from emberblast.game import DeathMatch, bot_factory
from emberblast.orchestrator import DeathMatchOrchestrator

from .test import BaseTestCase, manual_test
from .test_map import mock_map


@mock_map()
def mock_game() -> Callable:
    def wrapper(func):
        bots = bot_factory(5)
        game = DeathMatch(bots, mock_game.mock_map)
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
