from typing import List, Union

import emojis
from InquirerPy import prompt

from project.item import Item, EquipmentItem
from project.player import Player


def select_item(items: List[Item]) -> Union[str, bool, list, Item]:
    """
    Select an item to use, or even get more information about it.

    :param List[Item] items: The available items for the player.
    :rtype: Union[str, bool, list, Item].
    """
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
            'invalid_message': 'You need to select at least one item',
            'show_cursor': True,
            'max_height': '100'
        }
    ]

    result = prompt(questions=items_questions)
    selected_item = result[0]
    return selected_item


def confirm_item_selection() -> Union[str, bool, list, bool]:
    """
    Confirm question, to ensure that player really wants to use the selected item.

    :rtype: Union[str, bool, list, bool].
    """
    questions = [
        {"type": "confirm", "message": "Are you sure?", "name": "confirm", "default": False},
    ]
    result = prompt(questions)
    confirm = result["confirm"]
    return confirm


def confirm_use_item_on_you() -> Union[str, bool, list, bool]:
    """
    Confirm question, to ensure that player really wants to use the selected item on himself.

    :rtype: Union[str, bool, list, bool].
    """
    questions = [
        {"type": "confirm", "message": "Are you using the item on yourself?", "name": "confirm", "default": False},
    ]
    result = prompt(questions)
    confirm = result["confirm"]
    return confirm


def display_equipment_choices(player: Player) -> Union[str, bool, list, EquipmentItem]:
    """
    Will display all the equipments that player has, for equipping one of them.

    :param Player player: The current player.
    :rtype: Union[str, bool, list, EquipmentItem].
    """
    equipments = player.bag.get_equipments()
    choices = []

    for equip in equipments:
        equipped_string = ''
        if player.equipment.is_equipped(equip):
            equipped_string = '  (EQUIPPED)'
        choices.append({
            'name': emojis.encode('{item} - {tier} {equipped_string}'.format(item=equip.name,
                                                                             tier=equip.tier,
                                                                             equipped_string=equipped_string)),
            'value': equip
        })

    equipment_questions = [
        {
            'type': 'list',
            'message': 'Select an Equipment:',
            'choices': choices,
            'invalid_message': 'You need to select at least one item',
            'show_cursor': True,
            'max_height': '100'
        }
    ]

    result = prompt(questions=equipment_questions)
    selected_equipment = result[0]
    return selected_equipment
