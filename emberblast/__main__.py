import asyncio
import atexit
import os

from emberblast.communicator import communicator_injector
from emberblast.events import GreetingsEvent
from emberblast.game import GameFactory
from emberblast.interface import IEmberblast
from emberblast.save import save_game_state_on_exit


def exit_handler(orchestrator):
    save_game_state_on_exit(orchestrator)
    print("Closing Emberblast!")


@communicator_injector()
class Emberblast(IEmberblast):
    async def run(self):
        try:
            if not os.environ.get("OPENAI_API_KEY"):
                print("Warning: OPENAI_API_KEY not set. Bots will use deterministic AI.")
            self.communicator.informer.render(GreetingsEvent())
            game_factory = GameFactory()
            game_orchestrator = await game_factory.pre_initial_settings()
            atexit.register(exit_handler, game_orchestrator)
            await game_orchestrator.execute_game()
        except KeyboardInterrupt:
            pass
        except Exception as err:
            print(err)
            print("System shutdown with unexpected error")

    def __call__(self):
        asyncio.run(self.run())


if __name__ == "__main__":
    asyncio.run(Emberblast().run())


# pip cmd initializer
def run_project():
    asyncio.run(Emberblast().run())
