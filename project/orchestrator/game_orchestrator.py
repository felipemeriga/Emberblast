from os import system
from typing import List

import emojis
from colorama import Fore

from project.action import Move, Defend, Hide, Search, Attack, Skill, Item, Action, Check, Pass, Equip, Drop
from project.game import Game
from project.player import ControlledPlayer, BotPlayer, Player
from project.questions import ask_actions_questions
from project.utils import PASS_ACTION_NAME


class GameOrchestrator:

    def __init__(self, game: Game) -> None:
        self.clear = lambda: system('clear')
        self.game = game
        self.actions = {}
        self.init_actions()
        self.actions_left: List[str] = []

    def init_actions(self) -> None:
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

    def init_game(self):
        raise NotImplementedError('Game::to_string() should be implemented!')


class DeathMatchOrchestrator(GameOrchestrator):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def init_game(self) -> None:
        try:
            turn_list = list(self.game.turns.copy().keys())
            for turn in turn_list:
                self.clear()
                print(Fore.GREEN + emojis.encode(
                    ':fire: Starting Turn {turn}! Embrace Yourselves! :fire: \n\n'.format(turn=turn)))
                for player in self.game.turns.get(turn):
                    print(emojis.encode(
                        ':man: {name} Time! \n\n'.format(name=player.name)))
                    if isinstance(player, ControlledPlayer):
                        self.controlled_decisioning(player)
                    else:
                        self.bot_decisioning(player)
                self.game.calculate_turn_order()
                turn_list.append(turn + 1)
        except Exception as err:
            print(err)

    def bot_decisioning(self, player: BotPlayer) -> None:
        pass

    def hide_invalid_actions(self, player: Player) -> List[str]:
        valid_actions = self.actions_left.copy()

        if 'item' in valid_actions:
            if not player.bag.has_item_type(is_usable=True):
                valid_actions.remove('item')
        if not player.bag.has_item_type(is_equipment=True):
            valid_actions.remove('equip')
        if len(player.bag.items) < 1:
            valid_actions.remove('drop')

        return valid_actions

    def controlled_decisioning(self, player: ControlledPlayer) -> None:
        self.actions_left = list(self.actions.keys())

        while len(self.actions_left) > 2:
            chosen_action_string = ask_actions_questions(self.hide_invalid_actions(player))
            action = self.actions[chosen_action_string]
            self.clear()
            if action.act(player) is None:
                self.compute_player_decisions(action, chosen_action_string)

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
