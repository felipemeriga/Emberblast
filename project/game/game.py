from InquirerPy import prompt
from project.game.questions import BEGIN_GAME_QUESTIONS

class Game:

    def __init__(self, type, name):
        self.type = type
        self.name = name

    def init_game(self):
        raise NotImplementedError('Game::to_string() should be implemented!')


class Deathmatch(Game):

    def init_game(self):
        pass




class GameFactory:
    def new_game(self):
        result = prompt(BEGIN_GAME_QUESTIONS)