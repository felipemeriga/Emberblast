import random
from typing import List, TypedDict

from project.conf import get_configuration
from project.utils import ITEMS_SECTION


class Item:

    def __init__(self, name: str, tier: str, description: str, weight: float) -> None:
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


def get_random_item(tier: str) -> Item:
    items_dicts = get_configuration(ITEMS_SECTION)
    item_key = random.choice(list({k: v for (k, v) in items_dicts.items() if v.get('tier') == tier}.keys()))
    item_dict = items_dicts.get(item_key)

    if item_dict.get('type') == 'healing':
        return HealingItem(name=item_key,
                           tier=item_dict.get('type'),
                           description=item_dict.get('description'),
                           weight=item_dict.get('weight'),
                           attribute=item_dict.get('attribute'),
                           base=item_dict.get('base'))
    elif item_dict.get('type') == 'recovery':
        return RecoveryItem(name=item_key,
                            tier=item_dict.get('type'),
                            description=item_dict.get('description'),
                            weight=item_dict.get('weight'),
                            status=item_dict.get('status'))
    elif item_dict.get('type') == 'equipment':
        return EquipmentItem(name=item_key,
                             tier=item_dict.get('type'),
                             description=item_dict.get('description'),
                             weight=item_dict.get('weight'),
                             attribute=item_dict.get('attribute'),
                             base=item_dict.get('base'),
                             side_effects=item_dict.get('side_effects'))
