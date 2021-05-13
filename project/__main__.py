import sys

from colorama import Fore
from project.game.game import GameFactory
from project.player.job import Knight
from project.utils.utils import print_greetings


def run_project(args):
    print_greetings()
    game = GameFactory()
    game.new_game()


if __name__ == '__main__':
    try:
        knight = Knight()
        print(2)
        # run_project(sys.argv)
        print(2)
    except Exception as err:
        print(Fore.RED + "System shutdown with unexpected error")
        exit()


