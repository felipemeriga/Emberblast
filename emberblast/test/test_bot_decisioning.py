from .test import BaseTestCase, manual_test
from .test_game import mock_game
from emberblast.bot import BotDecisioning


@manual_test
@mock_game()
class TestModuleBot(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestModuleBot, self).__init__(*args, **kwargs)

    def test_bot_turn_decision(self) -> None:
        self.mock_game.game_map.define_player_initial_position_random(self.mock_game.get_all_players())
        bot_decisioning = BotDecisioning(self.mock_game)
        bot_decisioning.decide(self.mock_game.players[0])
        pass
