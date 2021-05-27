from os import system

import emojis
from colorama import Fore

from project.action import Move, Defend, Hide, Search, Attack, Skill, Item, Action
from project.game import Game
from project.player import ControlledPlayer, BotPlayer
from project.questions import ask_actions_questions


class GameOrchestrator:

    def __init__(self, game: Game) -> None:
        self.clear = lambda: system('clear')
        self.game = game
        self.actions = {}
        self.init_actions()
        self.actions_left = []

    def init_actions(self) -> None:
        self.actions['move'] = Move(True, False)
        self.actions['defend'] = Defend(False, False)
        self.actions['hide'] = Hide(False, False)
        self.actions['search'] = Search(False, False)
        self.actions['attack'] = Attack(False, False)
        self.actions['skill'] = Skill(False, False)
        self.actions['item'] = Item(False, False)
        self.actions['check'] = Item(True, True)
        self.actions['pass'] = Item(False, False)

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
                        '::man:: {name} Time! \n\n'.format(name=player.name)))
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

    def controlled_decisioning(self, player: ControlledPlayer) -> None:
        self.actions_left = list(self.actions.keys())
        last_action = ''

        while len(self.actions_left) > 2 and last_action != 'pass':
            chosen_action_string = ask_actions_questions(self.actions_left)
            action = self.actions[chosen_action_string].act()
            self.compute_player_decisions(action, chosen_action_string)

    def compute_player_decisions(self, action: Action, action_string: str) -> None:
        if action.repeatable:
            return
        if action.independent:
            self.actions_left.remove(action_string)
        else:
            for key, value in self.actions.values():
                if not value.independent:
                    self.actions_left.remove(key)
