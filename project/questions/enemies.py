from typing import List, Union

from InquirerPy import prompt

from project.player import Player


def ask_enemy_to_check(enemies: List[Player]) -> Union[str, bool, list, Player]:
    """
    Ask which enemy the player wants to know more info.

    :param List[Player] enemies: The unhidden players to analyze.
    :rtype: Union[str, bool, list, Player].
    """
    choices = []
    for enemy in enemies:
        choices.append({
            'name': '{enemy} ({job})'.format(enemy=enemy.name,
                                             job=enemy.job.get_name()),
            'value': enemy
        })
    enemies_questions = [
        {
            'type': 'list',
            'message': 'Select an enemy:',
            'choices': choices,
            'default': 'defend',
            'invalid_message': 'You need to select at least one enemy to check!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]

    result = prompt(questions=enemies_questions)
    selected_enemy = result[0]
    return selected_enemy
