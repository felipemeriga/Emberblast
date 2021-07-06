from typing import List, cast
from .items import Item, EquipmentItem, HealingItem, RecoveryItem


class Bag:

    def __init__(self) -> None:
        self.items: List[Item] = []
        self.weight = 0

    def add_item(self, item: Item) -> None:
        self.weight = self.weight + item.weight
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        self.weight = self.weight - item.weight
        self.items.remove(item)

    def get_equipments(self) -> List[EquipmentItem]:
        return cast(List[EquipmentItem], [x for x in filter(
            lambda item: isinstance(item, EquipmentItem), self.items)])

    def has_item_type(self, is_usable: bool = False, is_equipment: bool = False) -> bool:
        """
        Function for checking if an item of determined type exists in the bag, and return
        a boolean if they are found.

        :param bool is_usable: It will look for healing or recovery items in the bag.
        :param bool is_equipment: It will look for equipment items in the bag.
        :rtype: bool
        """
        exists = False

        for item in self.items:
            if is_usable:
                if isinstance(item, HealingItem) or isinstance(item, RecoveryItem):
                    return True
            elif is_equipment:
                if isinstance(item, EquipmentItem):
                    return True
        return exists
