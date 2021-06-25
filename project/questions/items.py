from typing import List, Union

import emojis
from InquirerPy import prompt

from project.item import Item


def ask_item_to_check(items: List[Item]) -> Union[str, bool, list, Item]:
    choices = []
    for item in items:
        choices.append({
            'name': emojis.encode('{item} - {tier}'.format(item=item.name,
                                                           tier=item.tier)),
            'value': item
        })
    items_questions = [
        {
            'type': 'list',
            'message': 'Select an item:',
            'choices': choices,
            'default': items[0],
            'invalid_message': 'You need to select at least one item to check',
            'show_cursor': True,
            'max_height': '100'
        }
    ]

    result = prompt(questions=items_questions)
    selected_item = result[0]
    return selected_item
