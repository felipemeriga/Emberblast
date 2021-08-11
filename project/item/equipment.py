from typing import Union
from project.interface import IEquipment, IEquipmentItem, IItem


class Equipment(IEquipment):

    def __init__(self) -> None:
        """
        Constructor of Equipment class

        :rtype: None
        """
        self.weapon: Union[None, IEquipmentItem] = None
        self.armour: Union[None, IEquipmentItem] = None
        self.boots: Union[None, IEquipmentItem] = None
        self.accessory: Union[None, IEquipmentItem] = None

    def equip(self, equipment: IEquipmentItem):
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
        item: Union[None, IEquipmentItem]
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

    def is_equipped(self, equipment: IEquipmentItem) -> bool:
        """
        This function will check if an item it's equipped on the player.

        :param EquipmentItem equipment: The equipment to identify.
        :rtype: None
        """
        if self.__getattribute__(equipment.category) == equipment:
            return True
        return False

    def check_and_remove(self, selected_item: IItem):
        """
        Check if item it's equipped, and remove it.

        :param Item selected_item: The equipment to verify.
        :rtype: None
        """
        if isinstance(selected_item, IEquipmentItem):
            for item in self.__dict__.items():
                if item == selected_item:
                    self.remove_equipment(selected_item.category)
