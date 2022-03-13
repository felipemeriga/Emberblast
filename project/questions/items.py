from typing import List, Union

import emojis
from InquirerPy import prompt

from project.interface import IItem, IEquipmentItem, IPlayer, IItemsQuestioner


class ItemsQuestionerCMD(IItemsQuestioner):

    def select_item(self, items: List[IItem]) -> Union[str, bool, list, IItem]:
        choices = []
        for item in items:
            choices.append({
                'name': emojis.encode('{item} - {tier}'.format(item=item.name,
                                                               tier=item.tier)),
                'value': item
            })
        choices.append({
            'name': emojis.encode('Cancel :x: '),
            'value': None
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

    def confirm_item_selection(self) -> Union[str, bool, list, bool]:
        questions = [
            {"type": "confirm", "message": "Are you sure?", "name": "confirm", "default": False},
        ]
        result = prompt(questions)
        confirm = result["confirm"]
        return confirm

    def confirm_use_item_on_you(self) -> Union[str, bool, list, bool]:
        questions = [
            {"type": "confirm", "message": "Are you using the item on yourself?", "name": "confirm", "default": False},
        ]
        result = prompt(questions)
        confirm = result["confirm"]
        return confirm

    def display_equipment_choices(self, player: IPlayer) -> Union[str, bool, list, IEquipmentItem]:
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
        choices.append({
            'name': emojis.encode('Cancel :x: '),
            'value': None
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
