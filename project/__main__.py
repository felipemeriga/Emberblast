import sys

from colorama import Fore
from project.game.game import GameFactory
from project.utils.name_generator.fantasy_name_generator import generate_name
from project.utils.utils import print_greetings


def run_project(args):
    print_greetings()
    game = GameFactory()
    game.new_game()


if __name__ == '__main__':
    try:
        name = generate_name()
        run_project(sys.argv)
    except Exception as err:
        print(Fore.RED + "System shutdown with unexpected error")
        exit()


