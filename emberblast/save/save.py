import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import cloudpickle

from emberblast.interface import IGameOrchestrator
from emberblast.utils import get_project_root


def save_game_state_on_exit(orchestrator_object: IGameOrchestrator) -> None:
    """
    This method it's called whenever the game crashes or it's stopped, and basically it saves all the information
    of a played game, saving all the current instantiated objects in a file, using pickle library.

    :param IGameOrchestrator orchestrator_object: The orchestrator, that controls all the game.
    :rtype: None.
    """
    now = datetime.now()
    current_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    main_player = orchestrator_object.game.players[0]
    save_file_name = '{date}-saved-game-{name}-{job}.pckl'.format(
        date=current_time,
        name=main_player.name,
        job=main_player.job.get_name(),
    )

    save_file_path = '{working_directory}/saved_games/{file}'.format(working_directory=str(get_project_root()),
                                                                     file=save_file_name)

    f = open(save_file_path, 'wb')
    cloudpickle.dump(orchestrator_object, f)
    f.close()


def recover_saved_game_orchestrator(file: Path) -> IGameOrchestrator:
    """
    Get the game orchestrator object from a save file.

    :param Path file: The Path object, where the save file it's located locally.
    :rtype: IGameOrchestrator.
    """
    game_orchestrator = None
    # Load data (deserialize)
    f = open(str(file), 'rb')
    game_orchestrator = cloudpickle.load(f)
    return game_orchestrator


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
    communicator.

    :rtype: List[Dict].
    """
    normalized_files = []
    raw_saved_files = get_saved_game_files()

    for raw_file in raw_saved_files:
        if raw_file.name == "__init__.py" or raw_file.name == "__pycache__":
            continue
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
