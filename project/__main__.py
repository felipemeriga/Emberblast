import sys

from colorama import Fore

from project.game import GameFactory
from project.message import print_greetings


def run_project(args):
    print_greetings()
    game_factory = GameFactory()
    game_orchestrator = game_factory.new_game()
    game_orchestrator.init_game()


if __name__ == '__main__':
    try:
        run_project(sys.argv)
        # print(colored('*', 'white', attrs=['blink', 'bold']))

    except Exception as err:
        print(Fore.RED + "System shutdown with unexpected error")
        exit()
