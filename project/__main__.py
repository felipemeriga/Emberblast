import sys

import cloudpickle
from colorama import Fore
import atexit
from project.game import GameFactory
from project.message import print_greetings


def exit_handler(orchestrator):
    f = open('store.pckl', 'wb')
    cloudpickle.dump(orchestrator, f)
    f.close()
    print('Closing Emberblast!')


def run_project(args):
    try:
        print_greetings()
        game_factory = GameFactory()
        game_orchestrator = game_factory.new_game()
        atexit.register(exit_handler, game_orchestrator)
        game_orchestrator.execute_game()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(Fore.RED + 'System shutdown with unexpected error')


if __name__ == '__main__':
    run_project(sys.argv)
