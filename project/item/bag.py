from typing import List, cast
from .items import Item, EquipmentItem


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
