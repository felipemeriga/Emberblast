from os import system

import emojis
from colorama import Fore

from project.action.actions import Move, Defend, Hide, Search, Attack, Skill, Item
from project.game.game import Game
from project.player.player import ControlledPlayer, BotPlayer


class GameOrchestrator:

    def __init__(self, game: Game) -> None:
        self.clear = lambda: system('clear')
        self.game = game
        self.actions = {}
        self.init_actions()
        self.actions_left = {}

    def init_actions(self) -> None:
        self.actions['move'] = Move()
        self.actions['defend'] = Defend()
        self.actions['hide'] = Hide()
        self.actions['search'] = Search()
        self.actions['attack'] = Attack()
        self.actions['skill'] = Skill()
        self.actions['item'] = Item()

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
        self.actions_left = self.actions.keys()

