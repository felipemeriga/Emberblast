import emojis
from InquirerPy import prompt


def ask_actions_questions(actions_available):
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
    }

    authorized_actions = []
    for i in actions_available:
        authorized_actions.append(base_actions.get(i))
    actions_questions = [
        {
            'type': 'list',
            'message': 'Select an action:',
            'choices': authorized_actions,
            'default': 'Defend',
            'invalid_message': 'You need to select at least one action to execute!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]
    result = prompt(questions=actions_questions)
    print(result)
