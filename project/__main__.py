import sys

from colorama import Fore
import atexit
from project.game import GameFactory
from project.message import print_greetings


def exit_handler():
    print('My application is ending!')


def run_project(args):
    game_orchestrator = None
    try:
        print_greetings()
        game_factory = GameFactory()
        game_orchestrator = game_factory.new_game()
        game_orchestrator.execute_game()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(Fore.RED + 'System shutdown with unexpected error')


if __name__ == '__main__':
    atexit.register(exit_handler)
    run_project(sys.argv)
