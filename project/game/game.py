from random import randrange
from typing import List


from project.conf import get_configuration
from project.map import Map
from project.player import Player, BotPlayer
from project.player import ControlledPlayer
from project.utils import GAME_SECTION


class Game:

    def __init__(self, main_player: ControlledPlayer, bots: List[BotPlayer], game_map: Map):
        self.main_player = main_player
        self.bots = bots
        self.game_map = game_map
        self.turns = {}

    # The turn order is calculated based on the will of the character, the players are sorted
    #  based on the following equation: (will/5) * (dice result), the number of the dice sides
    #  can be configured in the main configuration file
    def calculate_turn_order(self):
        players = []
        turn = 0
        if not self.turns:
            turn = 1
            self.turns[turn] = []
        else:
            turn = list(self.turns)[-1] + 1
            self.turns[turn] = []
        players.extend(self.bots)
        players.append(self.main_player)
        players.sort(key=lambda x: (x.will / 5) * randrange(get_configuration(GAME_SECTION).get('dice_sides', 6)),
                     reverse=True)
        self.turns[turn] = players

    def get_all_players(self) -> List[Player]:
        players = [self.main_player]
        players.extend(self.bots)
        return players

    def get_remaining_players(self, player: Player, include_hidden: bool = False) -> List[Player]:
        players = self.get_all_players()
        remaining_players = [x for x in filter(lambda a: a.is_alive() and a.name != player.name if not include_hidden
        else a.is_alive() and a.name != player.name and not a.is_hidden()
                                               , players)]
        return remaining_players


class DeathMatch(Game):

    def __init__(self, main_player, bots, game_map):
        super(DeathMatch, self).__init__(main_player, bots, game_map)
