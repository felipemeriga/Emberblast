import random
from typing import List
from emberblast.conf import get_configuration
from emberblast.utils import ITEMS_SECTION
from emberblast.effect import SideEffect, instantiate_side_effects
from emberblast.interface import IItem, IHealingItem, IRecoveryItem, IEquipmentItem, ISideEffect


class Item(IItem):

    def __init__(self, name: str, tier: str, description: str, weight: float) -> None:
        """
        Constructor of Item (Primitive Class)

        :param str name: Name of the item.
        :param str tier: The tier of the item(common, uncommon, rare, legendary),
        :param str description: Description of the item.
        :param float weight: Weight of the item.

        :rtype: None
        """
        self.name = name
        self.tier = tier
        self.description = description
        self.weight = weight


class HealingItem(IHealingItem, Item):

    def __init__(self, name: str, tier: str, description: str, weight: float, attribute: str, base: int) -> None:
        """
        Constructor of HealingItem

        :param str name: Name of the item.
        :param str tier: The tier of the item(common, uncommon, rare, legendary),
        :param str description: Description of the item.
        :param float weight: Weight of the item.
        :param str attribute: Attribute to be healed.
        :param int base: How much the attribute will be healed.

        :rtype: None
        """
        self.attribute = attribute
        self.base = base
        super().__init__(name, tier, description, weight)


class RecoveryItem(IRecoveryItem, Item):

    def __init__(self, name: str, tier: str, description: str, weight: float, status: str) -> None:
        """
        Constructor of RecoveryItem

        :param str name: Name of the item.
        :param str tier: The tier of the item(common, uncommon, rare, legendary),
        :param str description: Description of the item.
        :param float weight: Weight of the item.
        :param str status: The status(side-effect) to be recovered.
        :rtype: None
        """
        self.status = status
        super().__init__(name, tier, description, weight)


class EquipmentItem(IEquipmentItem, Item):

    def __init__(self, name: str, tier: str, description: str, weight: float, attribute: str, base: int,
                 side_effects: List[ISideEffect], category: str, usage: str, wielding: int = 1) -> None:
        """
        Constructor of EquipmentItem

        :param str name: Name of the equipment.
        :param str tier: The tier of the equipment(common, uncommon, rare, legendary).
        :param str description: Description of the item.
        :param float weight: Weight of the item.
        :param str attribute: Attribute that the equip improves.
        :param int base: The value of that attribute that this equip will improve.
        :param List[ISideEffect] side_effects: The side effects of that equipment.
        :param str category: The category of the equipment.
        :param str usage: If the equipment attributes apply to all the cases, to melee attack only or ranged only.

        :rtype: None
        """
        self.attribute = attribute
        self.base = base
        self.side_effects = side_effects
        self.category = category
        self.usage = usage
        self.wielding = wielding
        super().__init__(name, tier, description, weight)


def get_random_item(tier: str, item_type: str) -> Item:
    """
    Function to get a random item along all the items from the items.yaml file,
    considering a specific tier and type.

    :param str tier: The tier of the item.
    :param str item_type: The type of the item(healing, recovery, equipment)
    :rtype: Item
    """
    items_dicts = get_configuration(ITEMS_SECTION)
    item_key = random.choice(
        list({k: v for (k, v) in items_dicts.items() if v.get('tier') == tier and v.get('type') == item_type}.keys()))
    item_dict = items_dicts.get(item_key)

    if item_dict.get('type') == 'healing':
        return HealingItem(name=item_dict.get('name'),
                           tier=item_dict.get('tier'),
                           description=item_dict.get('description'),
                           weight=item_dict.get('weight'),
                           attribute=item_dict.get('attribute'),
                           base=item_dict.get('base'))
    elif item_dict.get('type') == 'recovery':
        return RecoveryItem(name=item_dict.get('name'),
                            tier=item_dict.get('tier'),
                            description=item_dict.get('description'),
                            weight=item_dict.get('weight'),
                            status=item_dict.get('status'))
    elif item_dict.get('type') == 'equipment':
        '''
        Side-effects are instantiated here, because when the user equips the item, the side-effect it's 
        already instantiated and it will be appended into the user's side-effect list, passing the same instance,
        which makes the changes to duration attribute, each time a new turn comes, reflects both in the list of side
        effects and also in the bag. 
        
        '''
        side_effects = instantiate_side_effects(item_dict.get('side_effects'))

        return EquipmentItem(name=item_dict.get('name'),
                             tier=item_dict.get('tier'),
                             description=item_dict.get('description'),
                             weight=item_dict.get('weight'),
                             attribute=item_dict.get('attribute'),
                             base=item_dict.get('base'),
                             side_effects=side_effects,
                             category=item_dict.get('category'),
                             usage=item_dict.get('usage'),
                             wielding=item_dict.get('wielding', 0))
