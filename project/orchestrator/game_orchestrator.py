from os import system
from typing import List

import emojis
from colorama import Fore

from project.action import Move, Defend, Hide, Search, Attack, Skill, Item, Action, Check, Pass, Equip, Drop
from project.questions import ask_actions_questions
from project.utils import PASS_ACTION_NAME
from project.interface import IGame, IControlledPlayer, IPlayer, IBotPlayer


class GameOrchestrator:

    def __init__(self, game: IGame) -> None:
        """
        Constructor of the Game Orchestrator, which is the Class that receives a Game object,
        and command and coordinate the actions, and the execution of the game based on turns.

        :param Game game: The created game to be executed.
        :rtype: None.
        """
        self.clear = lambda: system('clear')
        self.game = game
        self.actions = {}
        self.init_actions()
        """
        The actions left, it's an array of the available actions of a player on a turn,
        for each player and each turn, this array is modified.
        """
        self.actions_left: List[str] = []
        """
        The turn remaining players manages how many players are left for playing a turn, this variable
        it's very important for saved games, because it helps the game to be continued exactly from the 
        player that was playing when the game was saved.
        """
        self.turn_remaining_players: List[IPlayer] = []

    def init_actions(self) -> None:
        """
        Init the actions available in the game, each of the actions of the game, are represented by Singleton clases
        that coordinates and implements the execution of that action.

        :rtype: None.
        """
        self.actions['move'] = Move(True, False, self.game)
        self.actions['defend'] = Defend(False, False, self.game)
        self.actions['hide'] = Hide(False, False, self.game)
        self.actions['search'] = Search(True, False, self.game)
        self.actions['attack'] = Attack(False, False, self.game)
        self.actions['skill'] = Skill(False, False, self.game)
        self.actions['item'] = Item(False, False, self.game)
        self.actions['equip'] = Equip(True, True, self.game)
        self.actions['drop'] = Drop(True, True, self.game)
        self.actions['check'] = Check(True, True, self.game)
        self.actions['pass'] = Pass(True, False, self.game)

    def execute_game(self) -> None:
        """
        This method should be implement by Styles of Games that Inherits from this superclass.

        :rtype: None.
        """
        raise NotImplementedError('Game::to_string() should be implemented!')


class DeathMatchOrchestrator(GameOrchestrator):

    def __init__(self, game: IGame) -> None:
        """
        Constructor of the DeathMatchOrchestrator.
        :rtype: None.
        """
        super().__init__(game)

    def execute_game(self) -> None:
        """
        The implementation of the superclass method,which is the one for executing each of the calculated turns of
        the game. It's the same method to start a newly created game or a continue.

        :rtype: None.
        """
        try:
            # Getting only the last element of the list, because in the case it's a saved game, it will take the last
            # player turn, and continue from there, if it's a new game, it will only game the first turn, which is the
            # first and the only element of the turns dictionary.
            turn_list = [list(self.game.turns.copy().keys())[-1]]
            for turn in turn_list:
                self.clear()
                print(Fore.GREEN + emojis.encode(
                    ':fire: Starting Turn {turn}! Embrace Yourselves! :fire: \n\n'.format(turn=turn)))

                if not len(self.turn_remaining_players) > 0:
                    # Making a copy of the dict, because dicts are mutable, and without a copy, would alter
                    # the attribute from Game class.
                    # Additionally, the remaining players attributes allow the game to be continued from the player
                    # that was playing when the game was saved.
                    self.turn_remaining_players = self.game.turns.get(turn).copy()

                while len(self.turn_remaining_players) > 0:
                    player = self.turn_remaining_players[0]
                    print(emojis.encode(
                        ':man: {name} Time! \n\n'.format(name=player.name)))
                    if isinstance(player, IControlledPlayer):
                        self.controlled_decisioning(player)
                    else:
                        self.bot_decisioning(player)
                    self.turn_remaining_players.remove(player)

                self.game.calculate_turn_order()
                turn_list.append(turn + 1)
        except Exception as err:
            print(err)

    def bot_decisioning(self, player: IBotPlayer) -> None:
        pass

    def hide_invalid_actions(self, player: IPlayer) -> List[str]:
        valid_actions = self.actions_left.copy()

        if 'item' in valid_actions:
            if not player.bag.has_item_type(is_usable=True):
                valid_actions.remove('item')
        if not player.bag.has_item_type(is_equipment=True):
            valid_actions.remove('equip')
        if len(player.bag.items) < 1:
            valid_actions.remove('drop')

        return valid_actions

    def controlled_decisioning(self, player: IControlledPlayer) -> None:
        self.actions_left = list(self.actions.keys())
        player.compute_iterated_side_effects()

        while len(self.actions_left) > 2:
            chosen_action_string = ask_actions_questions(self.hide_invalid_actions(player))
            action = self.actions[chosen_action_string]
            self.clear()
            if action.act(player) is None:
                self.compute_player_decisions(action, chosen_action_string)
        else:
            player.compute_side_effect_duration()

    def compute_player_decisions(self, action: Action, action_string: str) -> None:
        if action_string == PASS_ACTION_NAME:
            self.actions_left.clear()
        elif action.repeatable:
            return
        elif action.independent:
            self.actions_left.remove(action_string)
        else:
            for key, value in self.actions.items():
                if not value.independent:
                    self.actions_left.remove(key)
