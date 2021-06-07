from typing import List, Union

from InquirerPy import prompt


def ask_enemy_to_check(enemies):
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
            'message': 'Select an action:',
            'choices': choices,
            'default': 'defend',
            'invalid_message': 'You need to select at least one action to execute!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]

    result = prompt(questions=enemies_questions)
    selected_enemy = result[0]
    return selected_enemy
