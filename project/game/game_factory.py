from InquirerPy import prompt
from typing import List

from project.game import DeathMatch
from project.map import MapFactory, Map
from project.orchestrator import GameOrchestrator, DeathMatchOrchestrator
from project.player import ControlledPlayer, dynamic_jobs_classes, dynamic_races_classes, bot_factory, BotPlayer
from project.questions import BEGIN_GAME_QUESTIONS


class GameFactory:
    def __init__(self):
        self.begin_question_results = None

    def new_game(self) -> GameOrchestrator:
        self.begin_question_results = prompt(BEGIN_GAME_QUESTIONS)
        main_player = self.init_players()

        bots = self.init_bots()

        game_map = self.init_map(len(bots) + 1)

        if self.begin_question_results.get('game') == 'Deathmatch':
            game = DeathMatch(main_player, bots, game_map)
            game.calculate_turn_order()
            orchestrator = DeathMatchOrchestrator(game)
            return orchestrator

    def init_map(self, map_size: int) -> Map:
        return MapFactory().create_map(map_size)

    def init_players(self) -> ControlledPlayer:
        return ControlledPlayer(self.begin_question_results.get('nickname'),
                                dynamic_jobs_classes[self.begin_question_results.get('job')](),
                                dynamic_races_classes[self.begin_question_results.get('race')]())

    def init_bots(self) -> List[BotPlayer]:
        return bot_factory(self.begin_question_results.get('bots_number'))
