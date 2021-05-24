import sys

from colorama import Fore

from project.action.actions import Action, Move
from project.game.game import GameFactory
from project.utils.utils import print_greetings


def run_project(args):
    print_greetings()
    game_factory = GameFactory()
    game = game_factory.new_game()
    game.init_game()


if __name__ == '__main__':
    try:
        act1 = Move()
        act2 = Move()

        if act1 == act2:
            print('foiiii')
        run_project(sys.argv)
    except Exception as err:
        print(Fore.RED + "System shutdown with unexpected error")
        exit()
