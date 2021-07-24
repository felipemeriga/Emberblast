import sys

from colorama import Fore

from project.game import GameFactory
from project.message import print_greetings

def run_project(args):
    game_orchestrator = None
    try:
        print_greetings()
        game_factory = GameFactory()
        game_orchestrator = game_factory.new_game()
        game_orchestrator.execute_game()
    except Exception as err:
        print(Fore.RED + "System shutdown with unexpected error")
        exit()


if __name__ == '__main__':
    run_project(sys.argv)
