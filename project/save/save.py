import os
from datetime import datetime
from pathlib import Path
from typing import List

import cloudpickle

from project.orchestrator import GameOrchestrator
from project.utils import get_project_root


def save_game_state_on_exit(orchestrator_object: GameOrchestrator) -> None:

    now = datetime.now()
    current_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    save_file_name = '{date}-saved-game-{name}-{job}.pckl'.format(
        date=current_time,
        name=orchestrator_object.game.main_player.name,
        job=orchestrator_object.game.main_player.job.get_name(),
    )

    save_file_path = '{working_directory}/saved_games/{file}'.format(working_directory=str(get_project_root()),
                                                                     file=save_file_name)

    f = open(save_file_path, 'wb')
    cloudpickle.dump(orchestrator_object, f)
    f.close()


def get_saved_game_files() -> List[Path]:
    return sorted(Path('{working_directory}/saved_games'.format(working_directory=str(get_project_root())
                                                                )).iterdir(), key=os.path.getmtime, reverse=True)
