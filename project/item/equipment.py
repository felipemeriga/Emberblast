import typing
from typing import List

from .items import EquipmentItem


class Equipment:

    def __init__(self) -> None:
        self.weapon: typing.Union[None, EquipmentItem] = None
        self.armour: typing.Union[None, EquipmentItem] = None
        self.boots: typing.Union[None, EquipmentItem] = None
        self.accessory: List[EquipmentItem] = []

    def equip(self, equipment: EquipmentItem):
        self.__setattr__(equipment.category, equipment)

    def get_attribute_addition(self, attribute: str) -> int:
        result = 0
        item: typing.Union[None, EquipmentItem] = None
        for item in self.__dict__.items():
            if item is not None:
                if item.attribute == attribute:
                    result = result + item.base

        return result

    def remove_equipment(self, category: str):
        self.__setattr__(category, None)
