from typing import List, Union

from InquirerPy import prompt
from emojis import emojis

from project.interface import IMovementQuestioner


class MovementQuestionerCMD(IMovementQuestioner):

    def ask_where_to_move(self, possibilities: List[str]) -> Union[str, bool, list, str]:
        questions = [
            {
                'type': 'list',
                'message': emojis.encode(':mount_fuji: Select where to move: '),
                'choices': possibilities,
                'invalid_message': 'You need to select at least one place to move!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=questions)
        return result[0]
