from emberblast.communicator import communicator_injector
from emberblast.events import EnemyStatusEvent, PlayerStatsEvent
from emberblast.test.test import CommunicatorTestCase, manual_test

from .test_map import mock_map
from .test_player import mock_player


@manual_test
@mock_player()
@mock_map()
@communicator_injector()
class TestModuleMessage(CommunicatorTestCase):
    def test_print_player_stats(self) -> None:
        self.communicator.informer.render(PlayerStatsEvent(player=self.mock_player))

    def test_print_enemy_status(self) -> None:
        self.communicator.informer.render(EnemyStatusEvent(enemy=self.mock_player))

    def test_print_plain_matrix(self) -> None:
        pass
