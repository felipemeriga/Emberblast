from typing import List

from InquirerPy import prompt
from emojis import emojis


def ask_where_to_move(possibilities: List[str]) -> str:
    """
    This function is used by asking the player where he wants to move.

    :param List[str] possibilities: The previously calculated possibilities of movement.
    :rtype: Union[str, bool, list, str].
    """
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
