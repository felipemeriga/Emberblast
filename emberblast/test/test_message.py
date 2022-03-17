from emberblast.test.test import BaseTestCase
from emberblast.message import print_player_stats, print_enemy_status
from .test_player import mock_player
from .test_map import mock_map


@mock_player()
@mock_map()
class TestModuleMessage(BaseTestCase):
    def test_print_player_stats(self) -> None:
        print_player_stats(self.mock_player)

    def test_print_enemy_status(self) -> None:
        print_enemy_status(self.mock_player)

    def test_print_plain_matrix(self) -> None:
        pass
