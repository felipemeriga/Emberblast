from emberblast.test.test import manual_test, CommunicatorTestCase
from .test_player import mock_player
from .test_map import mock_map
from emberblast.communicator import communicator_injector


@manual_test
@mock_player()
@mock_map()
@communicator_injector()
class TestModuleMessage(CommunicatorTestCase):
    def test_print_player_stats(self) -> None:
        self.communicator.informer.player_stats(self.mock_player)

    def test_print_enemy_status(self) -> None:
        self.communicator.informer.enemy_status(self.mock_player)

    def test_print_plain_matrix(self) -> None:
        pass
