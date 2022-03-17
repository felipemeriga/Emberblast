from functools import wraps
from typing import List, cast
from emberblast.interface import IBag, IItem, IEquipmentItem, IRecoveryItem, IHealingItem


def weight_compute(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        item: IItem = args[0]
        if 'add_item' in repr(func):
            self.weight = self.weight + item.weight
        elif 'remove_item' in repr(func):
            self.weight = self.weight - item.weight
        return func(self, *args, **kwargs)

    return wrapper


class Bag(IBag):
    def __init__(self) -> None:
        """
        Constructor
        :rtype: None
        """
        self.items: List[IItem] = []
        self.weight = 0

    @weight_compute
    def add_item(self, item: IItem) -> None:
        """
        Adds an item into the bag

        :param IItem item: the Item object to be added
        :rtype: None
        """
        self.items.append(item)

    @weight_compute
    def remove_item(self, item: IItem) -> None:
        """
        It remove one item from the bag

        :param IItem item: the Item object to be removed
        :rtype: None
        """
        self.items.remove(item)

    def get_equipments(self) -> List[IEquipmentItem]:
        """
        It will filter all equipments on your bag

        :rtype List[IEquipmentItem]
        """
        return cast(List[IEquipmentItem], [x for x in filter(
            lambda item: isinstance(item, IEquipmentItem), self.items)])

    def get_usable_items(self) -> List[IItem]:
        """
        It will filter all recovery and healing items from the bag, so the user can use it.

        :rtype: List[IItem]
        """
        return [x for x in filter(
            lambda item: isinstance(item, IHealingItem) or isinstance(item, IRecoveryItem), self.items)]

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
                if isinstance(item, IHealingItem) or isinstance(item, IRecoveryItem):
                    return True
            elif is_equipment:
                if isinstance(item, IEquipmentItem):
                    return True
        return exists
