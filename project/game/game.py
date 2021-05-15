from InquirerPy import prompt
from project.game.questions import BEGIN_GAME_QUESTIONS
from project.map.map import MapFactory


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
    def new_game(self):
        game_question_result = prompt(BEGIN_GAME_QUESTIONS)

        if game_question_result[0] == "Deathmatch":

            game = Deathmatch("Deathmatch")
            return game

    def init_map(self):
        pass

    def init_players(self):
        pass