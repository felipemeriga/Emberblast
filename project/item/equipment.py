import typing
from typing import List

from .items import EquipmentItem


class Equipment:

    def __init__(self) -> None:
        """
        Constructor of Equipment class

        :rtype: None
        """
        self.weapon: typing.Union[None, EquipmentItem] = None
        self.armour: typing.Union[None, EquipmentItem] = None
        self.boots: typing.Union[None, EquipmentItem] = None
        self.accessory: List[EquipmentItem] = []

    def equip(self, equipment: EquipmentItem):
        """
        Receives an instantiated EquipmentItem object, and set it to this class
        attribute, accordingly to the equipment category (weapon, armour, shield, etc..)

        :param equipment: EquipmentItem: The equipment to be equipped
        :rtype: None
        """
        self.__setattr__(equipment.category, equipment)

    def get_attribute_addition(self, attribute: str) -> int:
        """
        Each of the equipments, may change player's attributes, like HP, MP,
        intelligence, accuracy, this function receives one of that attributes as a string, and
        looks across all the equipments, if some of them improves/increments this attribute.

        :param attribute: str: The string of the attribute to look for increments
        :rtype: str
        """
        result = 0
        item: typing.Union[None, EquipmentItem] = None
        for item in self.__dict__.items():
            if item is not None:
                if item.attribute == attribute:
                    result = result + item.base

        return result

    def remove_equipment(self, category: str):
        """
        This function is used to remove an equipment, it might be used when the user drops the item.

        :param category: str: The string of the category of equipment to remove.
        :rtype: None
        """
        self.__setattr__(category, None)
