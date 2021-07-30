from pathlib import Path
from typing import Union, List, Dict

import emojis
from InquirerPy import prompt


def get_saved_game(normalized_files: List[Dict]) -> Union[str, bool, list, Path]:
    """
    Ask the players, which load file he wants to continue playing, the saved games comes in the normalized_files
    parameter, that it's a list of dictionaries that has the file itself, and also a normalized user friendly formatted
    name of this file.

    :param List[Dict] normalized_files: The dictionary of all saved games.
    :rtype: GameOrchestrator.
    """
    choices = []

    for file_dict in normalized_files:
        option = {
            'name': file_dict.get('name'),
            'value': file_dict.get('path')
        }
        choices.append(option)
    choices.append({
        'name': emojis.encode('Cancel :x:'),
        'value': 'cancel'
    })

    select_saved_game_questions = [
        {
            'type': 'list',
            'message': 'Select a game to continue: ',
            'choices': choices,
            'invalid_message': 'You need to select at least one enemy to check!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]
    result = prompt(questions=select_saved_game_questions)
    return result[0]
