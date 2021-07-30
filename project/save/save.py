import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import cloudpickle

from project.orchestrator import GameOrchestrator
from project.utils import get_project_root


def save_game_state_on_exit(orchestrator_object: GameOrchestrator) -> None:
    """
    This method it's called whenever the game crashes or it's stopped, and basically it saves all the information
    of a played game, saving all the current instantiated objects in a file, using pickle library.

    :param GameOrchestrator orchestrator_object: The orchestrator, that controls all the game.
    :rtype: None.
    """
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
    """
    Get all the local save files.

    :rtype: List[Path].
    """
    return sorted(Path('{working_directory}/saved_games'.format(working_directory=str(get_project_root())
                                                                )).iterdir(), key=os.path.getmtime, reverse=True)


def get_normalized_saved_files_dict() -> List[Dict]:
    """
    Normalized and format the name of each of the save files, to be presented in a user friendly format in the
    questions.

    :rtype: List[Dict].
    """
    normalized_files = []
    raw_saved_files = get_saved_game_files()

    for raw_file in raw_saved_files:
        split_file_name = raw_file.name.split('-saved-game-')
        normalized_name = '{firs_part} {second_part}'.format(
            firs_part=split_file_name[1].replace('-', ' ').replace('.pckl', ''),
            second_part=split_file_name[0])

        normalized_file_dict = {
            'name': normalized_name,
            'path': raw_file
        }
        normalized_files.append(normalized_file_dict)

    return normalized_files
