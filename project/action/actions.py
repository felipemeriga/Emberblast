"""
The plan here would be, as actions controls the game,
there will be a Singleton class called actions coordinator, that will
manage all the plays for all the players.

As the actions can be the same for each of the players, they will be considered Singletons
too.

Another thing to remember when creating the actions, is to use function generators and yield
for coordinating the move + another action per turn for each player.

Also, before this, we need to think about how it would be the difference between single player and
multiplayer, considering that it's ideal to use the same game class structure, to avoid copying similar
functionalities
"""
import math
import random
from typing import List

from numpy.random import choice

from project.game import Game
from project.player import Player
from project.questions import ask_check_action, ask_enemy_to_check, ask_where_to_move
from project.message import print_player_stats, print_enemy_status, print_map_info, print_moving_possibilities


class SingletonAction(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonAction, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Action(metaclass=SingletonAction):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        """
        Constructor of the Base Class for Actions.

        :param bool independent: If it's True, the execution of this action will not block others in the same turn.
        :param bool repeatable: If it's True, can be performed many times in a single turn.
        :param Game game: The current Game object, where the actions are going to be placed.
        :rtype: None
        """
        self.independent = independent
        self.repeatable = repeatable
        self.game = game

    def act(self, player: Player) -> None:
        """
        Base function for

        :param player:
        :rtype: None
        """
        pass

    def compute_analytics(self) -> None:
        pass


class Move(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: Player) -> None:
        possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position, player.move_speed)
        print_moving_possibilities(player.position, possibilities, self.game.game_map.graph.matrix,
                                   self.game.game_map.size)
        selected_place = ask_where_to_move(possibilities)
        player.set_position(selected_place)


class Defend(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)


class Hide(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: Player) -> None:
        result = self.game.chose_probability(additional=[0.7])
        # TODO - Print hide result on print.py
        player.set_hidden(result)


class Search(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)


class Attack(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)

    def get_attack_possibilities(self, player: Player, players: List[Player]) -> List[Player]:
        possible_foes = []
        attacker_combat_type = player.job.attack_type

        if attacker_combat_type == 'melee':
            for foe in players:
                if player.position == foe.position:
                    possible_foes.append(foe)
        elif attacker_combat_type == 'ranged':
            # TODO - implement the foes possibilities to ranged attacks
            '''
            For implementing this, considering that the map will still stay in the square matrix architecture,
            to check which foes are within the attacker reach, we just need to draw a circle from the attacker position,
            where the radius of this circle, it's the attacker's reach. Everyone inside that range, will be a possible 
            foe, the only thing that might be good to bear in mind, it's to test the scalability of the ranged attack,
            because the fact of using a circle to determinate foes, it's already a big advantage to ranged based
            players.
            '''
            reach_distance = math.floor(1 + player.accuracy / 3)

        return possible_foes

    def act(self, player: Player) -> None:
        players = self.game.get_remaining_players(player)
        # possible_foes = self.get_attack_possibilities()


class Skill(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)


class Item(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)


class Check(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: Player) -> None:
        check_option = ask_check_action()
        if check_option == 'status':
            print_player_stats(player)
        elif check_option == 'map':
            unhidden_foes = self.game.get_remaining_players(player, include_hidden=True)
            print_map_info(player, unhidden_foes, self.game.game_map.size, self.game.game_map.graph.matrix)
        elif check_option == 'enemy':
            enemies = self.game.get_remaining_players(player, include_hidden=True)
            enemy = ask_enemy_to_check(enemies)
            print_enemy_status(enemy)
        else:
            return


class Pass(Action):
    def __init__(self, independent: bool, repeatable: bool, game: Game) -> None:
        super().__init__(independent, repeatable, game)
