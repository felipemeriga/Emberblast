from InquirerPy import prompt
from project.game.questions import BEGIN_GAME_QUESTIONS
from project.map.map import MapFactory
from project.player.player import ControlledPlayer
from project.utils.constants import GAME_SECTION


class Game:

    def __init__(self, type):
        self.type = type

    def init_game(self):
        raise NotImplementedError('Game::to_string() should be implemented!')


class Deathmatch(Game):

    def __init__(self, type):
        super(type)

    def init_game(self):
        pass


class GameFactory:
    def __init__(self):
        self.begin_question_results = None

    def new_game(self):
        self.begin_question_results = prompt(BEGIN_GAME_QUESTIONS)
        main_player = ControlledPlayer(self.begin_question_results.get('name'),
                                       self.begin_question_results.get('job'),
                                       self.begin_question_results.get('race'))


        if self.begin_question_results.get('game') == 'Deathmatch"':
            game = Deathmatch('Deathmatch')
            return game

    def init_map(self):
        pass

    def init_players(self):
        pass
