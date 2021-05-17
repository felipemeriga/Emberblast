from InquirerPy import prompt
from project.game.questions import BEGIN_GAME_QUESTIONS
from project.map.map import MapFactory
from project.player.job import dynamic_jobs_classes
from project.player.player import ControlledPlayer, bot_factory
from project.player.race import dynamic_races_classes
from project.utils.constants import GAME_SECTION


class Game:

    def __init__(self, main_player, bots, game_map):
        self.main_player = main_player
        self.bots = bots
        self.game_map = game_map

    def init_game(self):
        raise NotImplementedError('Game::to_string() should be implemented!')


class Deathmatch(Game):

    def __init__(self, main_player, bots, game_map):
        super(Deathmatch, self).__init__(main_player, bots, game_map)

    def init_game(self):
        pass


class GameFactory:
    def __init__(self):
        self.begin_question_results = None

    def new_game(self):
        self.begin_question_results = prompt(BEGIN_GAME_QUESTIONS)
        main_player = self.init_players()

        bots = self.init_bots()

        game_map = self.init_map()

        if self.begin_question_results.get('game') == 'Deathmatch"':
            game = Deathmatch(main_player, bots, game_map)
            return game

    def init_map(self):
        return MapFactory().create_map()

    def init_players(self):
        return ControlledPlayer(self.begin_question_results.get('name'),
                                dynamic_jobs_classes[self.begin_question_results.get('job')](),
                                dynamic_races_classes[self.begin_question_results.get('race')]())

    def init_bots(self):
        return bot_factory(self.begin_question_results.get('bots_number'))
