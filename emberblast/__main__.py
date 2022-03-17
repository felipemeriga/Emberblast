import sys

from colorama import Fore
import atexit
from emberblast.game import GameFactory
from emberblast.message import print_greetings
from emberblast.save import save_game_state_on_exit


def exit_handler(orchestrator):
    save_game_state_on_exit(orchestrator)
    print('Closing Emberblast!')


def run_project():
    try:
        print_greetings()
        game_factory = GameFactory()
        game_orchestrator = game_factory.pre_initial_settings()
        atexit.register(exit_handler, game_orchestrator)
        game_orchestrator.execute_game()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)
        print(Fore.RED + 'System shutdown with unexpected error')


if __name__ == '__main__':
    run_project()
