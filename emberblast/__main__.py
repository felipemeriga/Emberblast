from colorama import Fore
import atexit

from emberblast.communicator import communicator_injector
from emberblast.game import GameFactory
from emberblast.interface import IEmberblast
from emberblast.save import save_game_state_on_exit


def exit_handler(orchestrator):
    save_game_state_on_exit(orchestrator)
    print('Closing Emberblast!')


@communicator_injector()
class Emberblast(IEmberblast):
    def run(self):
        try:
            self.communicator.informer.greetings()
            game_factory = GameFactory()
            game_orchestrator = game_factory.pre_initial_settings()
            atexit.register(exit_handler, game_orchestrator)
            game_orchestrator.execute_game()
        except KeyboardInterrupt:
            pass
        except Exception as err:
            print(err)
            print(Fore.RED + 'System shutdown with unexpected error')

    __call__ = run


if __name__ == '__main__':
    Emberblast().run()
