from typing import List, Union

import emojis
from InquirerPy import prompt


def ask_check_action(show_items: bool = False) -> Union[str, bool, list, str]:
    """
    Ask which kind of information player wants to check.

    :param bool show_items: If the player doesn't have items on its bag, this flag will help the
    questions to remove the items question.
    :rtype: Union[str, bool, list, str].
    """
    choices = [
        {
            'name': emojis.encode('Map and Enemies :city_sunset: '),
            'value': 'map'
        },
        {
            'name': emojis.encode('My Status: :bar_chart: '),
            'value': 'status'
        },
        {
            'name': emojis.encode('Single Enemy: :skull: '),
            'value': 'enemy'
        }
    ]
    if show_items:
        choices.append({
            'name': emojis.encode('My Items: :test_tube: '),
            'value': 'item'
        })

    choices.append({
        'name': emojis.encode('Cancel: :x: '),
        'value': 'cancel'
    })
    questions = [
        {
            'type': 'list',
            'message': 'Check: ',
            'choices': choices,
            'default': 'map',
            'invalid_message': 'You need to select at least one check to execute!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]
    result = prompt(questions=questions)
    return result[0]


def ask_actions_questions(actions_available: List[str]) -> Union[str, bool, list, str]:
    """
    Ask which action the player is going to execute.

    :param List[str] actions_available: The actions that the player it's currently allowed to execute.
    :rtype: Union[str, bool, list, str].
    """
    base_actions = {
        'move': {
            'name': emojis.encode('Move: :runner:'),
            'value': 'move'
        },
        'attack': {
            'name': emojis.encode('Attack: :crossed_swords:'),
            'value': 'attack'
        },
        'skill': {
            'name': emojis.encode('Skill: :fire:'),
            'value': 'skill'
        },
        'defend': {
            'name': emojis.encode('Defend: :shield:'),
            'value': 'defend'
        },
        'hide': {
            'name': emojis.encode('Hide: :ninja:'),
            'value': 'hide'
        },
        'search': {
            'name': emojis.encode('Search: :eye:'),
            'value': 'search'
        },
        'item': {
            'name': emojis.encode('Item: :test_tube:'),
            'value': 'item'
        },
        'equip': {
            'name': emojis.encode('Equip: :crossed_swords:'),
            'value': 'equip'
        },
        'drop': {
            'name': emojis.encode('Drop: :arrow_down:'),
            'value': 'drop'
        },
        'check': {
            'name': emojis.encode('Check: :eyes:'),
            'value': 'check'
        },
        'pass': {
            'name': emojis.encode('Pass: :wave:'),
            'value': 'pass'
        },
    }

    authorized_actions = []
    for i in actions_available:
        authorized_actions.append(base_actions.get(i))
    actions_questions = [
        {
            'type': 'list',
            'message': 'Select an action:',
            'choices': authorized_actions,
            'default': 'defend',
            'invalid_message': 'You need to select at least one action to execute!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]
    result = prompt(questions=actions_questions)
    return result[0]
