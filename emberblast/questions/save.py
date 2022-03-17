from pathlib import Path
from typing import Union, List, Dict

import emojis
from InquirerPy import prompt

from emberblast.interface import ISaveLoadQuestioner


class SaveLoadQuestionerCMD(ISaveLoadQuestioner):

    def get_saved_game(self, normalized_files: List[Dict]) -> Union[str, bool, list, Path]:
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
