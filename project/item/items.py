import random
from typing import List

from project.conf import get_configuration
from project.utils import ITEMS_SECTION


class Item:

    def __init__(self, name: str, tier: str, description: str, weight: float) -> None:
        self.name = name
        self.tier = tier
        self.description = description
        self.weight = weight


class HealingItem(Item):

    def __init__(self, name: str, tier: str, description: str, weight: float, attribute: str, base: int) -> None:
        self.attribute = attribute
        self.base = base
        super().__init__(name, tier, description, weight)


class RecoveryItem(Item):

    def __init__(self, name: str, tier: str, description: str, weight: float, status: str) -> None:
        self.status = status
        super().__init__(name, tier, description, weight)


class EquipmentItem(Item):

    def __init__(self, name: str, tier: str, description: str, weight: float, attribute: str, base: int,
                 side_effects: List[str]) -> None:
        self.attribute = attribute
        self.base = base
        self.side_effects = side_effects
        super().__init__(name, tier, description, weight)


"""
Function to get a random item among the validated ones from items config file


:param tier str: The tier of the random item
:param type str: The item_type of the random item
:rtype: Item
"""


def get_random_item(tier: str, item_type: str) -> Item:
    items_dicts = get_configuration(ITEMS_SECTION)
    item_key = random.choice(
        list({k: v for (k, v) in items_dicts.items() if v.get('tier') == tier and v.get('type') == item_type}.keys()))
    item_dict = items_dicts.get(item_key)

    if item_dict.get('type') == 'healing':
        return HealingItem(name=item_dict.get('name'),
                           tier=item_dict.get('type'),
                           description=item_dict.get('description'),
                           weight=item_dict.get('weight'),
                           attribute=item_dict.get('attribute'),
                           base=item_dict.get('base'))
    elif item_dict.get('type') == 'recovery':
        return RecoveryItem(name=item_dict.get('name'),
                            tier=item_dict.get('type'),
                            description=item_dict.get('description'),
                            weight=item_dict.get('weight'),
                            status=item_dict.get('status'))
    elif item_dict.get('type') == 'equipment':
        return EquipmentItem(name=item_dict.get('name'),
                             tier=item_dict.get('tier'),
                             description=item_dict.get('description'),
                             weight=item_dict.get('weight'),
                             attribute=item_dict.get('attribute'),
                             base=item_dict.get('base'),
                             side_effects=item_dict.get('side_effects'))
