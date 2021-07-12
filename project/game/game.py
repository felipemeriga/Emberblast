import functools
import random
from typing import List

from numpy.random import choice

from project.conf import get_configuration
from project.map import Map
from project.player import Player, BotPlayer
from project.player import ControlledPlayer
from project.utils import GAME_SECTION


class Game:

    def __init__(self, main_player: ControlledPlayer, bots: List[BotPlayer], game_map: Map) -> None:
        """
        Base constructor of this class, for creating the game, remember that the constructor arguments of this class
        are instantiated by the Game Factory.

        :param ControlledPlayer main_player: The main controlled player.
        :param List[BotPlayer] bots: The list of bots that will play.
        :param Map game_map: Generated map of the game.
        :rtype: None
        """
        self.main_player = main_player
        self.bots = bots
        self.game_map = game_map
        self.turns = {}
        self.dice_sides = get_configuration(GAME_SECTION).get('dice_sides', 6)

    def calculate_turn_order(self) -> None:
        """
        The turn order is calculated based on the will of the character, the players are sorted
        based on the following equation: (will/5) * (dice result), the number of the dice sides
        can be configured in the main configuration file

        :rtype: None
        """
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
        players.sort(key=lambda x: (x.will / 5) * self.roll_the_dice(),
                     reverse=True)
        self.turns[turn] = players

    def roll_the_dice(self) -> int:
        """
        Roll the dice, for checking the turn order, or attacking and another actions.
        The number of sides of the dice, can be configured in the application configuration file.

        :rtype: int: Result of the dice.
        """
        return random.randrange(self.dice_sides)

    def chose_probability(self, additional: List[float] = None) -> bool:
        """
        Sometimes, some decisioning mechanisms, like being successful in hiding, it's a weighted binary result.
        For example, system will pick randomly True or False, but this can be weighted, for example, 70% of being True
        and 30% of being False. This functions rolls the dice, and as higher is the result, greater will be the
        percentage for resulting a True.

        :param List[float] additional: If you want to add a starting percentage weight for True.
        :rtype: bool.
        """
        if additional is None:
            additional = [0]
        dice_result = self.roll_the_dice()
        positive_percentage = ((1 / self.dice_sides) * dice_result) + functools.reduce(lambda a, b: a + b, additional)
        negative_percentage = max(0, 1 - positive_percentage)
        return \
            choice([True, False], 1, p=[positive_percentage if positive_percentage <= 1 else 1, negative_percentage])[
                0]

    def check_another_players_in_position(self, current_player: Player) -> List[Player]:
        """
        This action will be used many times, for example checking how many another enemies are located in the
        same map position of the current player. It basically gets the current player position, and try to find another
        ones that are in the same. This function is mostly used for checking possible foes, or sorting players in
        the field.

        :param Player current_player: The player that is currently playing on its turn.
        :rtype: List[Player].
        """
        position = current_player.position
        another_players = []
        for player in self.get_all_players():
            if player.position == position and player is not current_player:
                another_players.append(player)

        return another_players

    def get_all_players(self) -> List[Player]:
        """
        Returns the list of all players of the game.

        :rtype: List[Player].
        """
        players = [self.main_player]
        players.extend(self.bots)
        return players

    def get_remaining_players(self, player: Player, include_hidden: bool = False) -> List[Player]:
        """
        Returns the list of all players alive, apart from the current player.
        It also has the parameter include_hidden, for including or not
        hidden players in the result.

        :param Player player: The player that is currently playing on its turn.
        :param bool include_hidden: Whether to include hidden players or not.

        :rtype: List[Player].
        """
        players = self.get_all_players()
        remaining_players = [x for x in filter(lambda a: a.is_alive() and a.name != player.name if not include_hidden
        else a.is_alive() and a.name != player.name and not a.is_hidden()
                                               , players)]
        return remaining_players


class DeathMatch(Game):

    def __init__(self, main_player, bots, game_map):
        """
        There must be many kinds of game, DeathMatch it's basically all vs all,
        and this class represents the implementation of Game.

        :rtype: None.
        """
        super(DeathMatch, self).__init__(main_player, bots, game_map)
