import asyncio
import atexit
import os
import sys

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


def run_textual():
    """Run the game with the Textual TUI."""
    import emberblast.communicator.communicator as comm_mod
    from emberblast.communicator import create_textual_communicator
    from emberblast.interface import IControlledPlayer
    from emberblast.tui.app import EmberblastApp

    app = EmberblastApp()
    textual_comm = create_textual_communicator(app)

    # Override the global communicator singleton so all @communicator_injector classes use it
    comm_mod.communicator = textual_comm

    async def game_task():
        try:
            if not os.environ.get("OPENAI_API_KEY"):
                app.post_combat_log("Warning: OPENAI_API_KEY not set. Bots will use deterministic AI.", "system")
            game_factory = GameFactory()
            game_factory.communicator = textual_comm
            game_orchestrator = await game_factory.pre_initial_settings()

            controlled_names = {
                p.name for p in game_orchestrator.game.get_all_players() if isinstance(p, IControlledPlayer)
            }
            app.switch_to_battle(controlled_names)

            game_orchestrator.communicator = textual_comm
            game_orchestrator.bot_controller.communicator = textual_comm

            # Store orchestrator ref so renderer can pull map/player data
            app._orchestrator = game_orchestrator

            # Render initial map
            from emberblast.events import MapInfoEvent

            all_players = game_orchestrator.game.get_all_players()
            first_player = all_players[0] if all_players else None
            if first_player:
                enemies = [p for p in all_players if p != first_player]
                textual_comm.informer.render(
                    MapInfoEvent(
                        current_player=first_player,
                        enemies=enemies,
                        matrix=game_orchestrator.game.game_map.graph.matrix,
                        size=game_orchestrator.game.game_map.size,
                    )
                )

            await game_orchestrator.execute_game()
        except Exception as err:
            app.post_combat_log(f"Error: {err}", "damage")

    app.set_game_task(game_task)
    app.run()


if __name__ == "__main__":
    if "--classic" in sys.argv:
        asyncio.run(Emberblast().run())
    else:
        run_textual()


# pip cmd initializer
def run_project():
    if "--classic" in sys.argv:
        asyncio.run(Emberblast().run())
    else:
        run_textual()
