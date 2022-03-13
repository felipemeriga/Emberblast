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
from typing import List, Optional

from project.interface import IGame, IPlayer, IAction


class SingletonAction(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonAction, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Action(IAction, metaclass=SingletonAction):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
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

    def act(self, player: IPlayer) -> Optional[bool]:
        """
        Base function for executing the action, it has an Optional
        return boolean value, which means that, in the case the action
        is cancelled, it will return True

        :param player:
        :rtype: Optional[bool]
        """
        pass

    def get_attack_possibilities(self, attack_range: int, player: IPlayer, players: List[IPlayer]) -> List[IPlayer]:
        """
        This function computes which enemies a player can attack, considering its attack style,
        ranged or melee.

        :param int attack_range: The range of skill/attack, zero means melee attack/skill.
        :param Player player: The player that will execute the attack action.
        :param List[Player] players: The another players playing against.
        :rtype: List[Player] players: The list of enemies to attack.
        """
        possible_foes = []

        if attack_range == 0:
            for foe in players:
                if player.position == foe.position:
                    possible_foes.append(foe)
        elif attack_range > 0:
            ranged_attack_possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position,
                                                                                                attack_range)
            ranged_attack_possibilities.append(player.position)
            for foe in players:
                if foe.position in ranged_attack_possibilities:
                    possible_foes.append(foe)

        return possible_foes

    def compute_analytics(self) -> None:
        pass
