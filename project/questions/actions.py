import emojis
from InquirerPy import prompt


def ask_actions_questions(actions_available):
    base_actions = {
        'move': {
            'name': emojis.encode('Move: :runner:'),
            'value': {
                'attribute': 'health_points',
                'value': 'move'
            }
        },
        'attack': {
            'name': emojis.encode('Attack: :crossed_swords:'),
            'value': {
                'attribute': 'health_points',
                'value': 'attack'
            }
        },
        'skill': {
            'name': emojis.encode('Skill: :fire:'),
            'value': {
                'attribute': 'health_points',
                'value': 'attack'
            }
        },
        'defend': {
            'name': emojis.encode('Defend: :shield:'),
            'value': {
                'attribute': 'health_points',
                'value': 'attack'
            }
        },
        'hide': {
            'name': emojis.encode('Hide: :ninja:'),
            'value': {
                'attribute': 'health_points',
                'value': 'attack'
            }
        },
        'search': {
            'name': emojis.encode('Search: :eye:'),
            'value': {
                'attribute': 'health_points',
                'value': 'attack'
            }
        },
        'item': {
            'name': emojis.encode('Item: :test_tube:'),
            'value': {
                'attribute': 'health_points',
                'value': 'attack'
            }
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
