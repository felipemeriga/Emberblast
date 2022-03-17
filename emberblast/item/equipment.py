from typing import Union
from emberblast.interface import IEquipment, IEquipmentItem, IItem, ISideEffect


class Equipment(IEquipment):

    def __init__(self) -> None:
        """
        Constructor of Equipment class

        :rtype: None
        """
        self.weapon: Union[None, IEquipmentItem] = None
        self.shield: Union[None, IEquipmentItem] = None
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
        # This if clause it's handling 2 handed weapons, in the case it's 2 handed, it will remove shields.
        if equipment.category == 'weapon' and equipment.wielding == 2:
            self.remove_equipment('shield')
        self.__setattr__(equipment.category, equipment)

    def get_attribute_addition(self, attribute: str, usage: str = 'all') -> int:
        """
        Each of the equipments, may change player's attributes, like HP, MP,
        intelligence, accuracy, this function receives one of that attributes as a string, and
        looks across all the equipments, if some of them improves/increments this attribute.

        :param str attribute: The string of the attribute to look for increments
        :param str usage: If it will get melee, ranged or all equipments.
        :rtype: int
        """
        result = 0
        for item in list(self.__dict__.values()):
            if item is not None:
                if item.attribute == attribute and item.usage == usage:
                    result = result + item.base

        return result

    def remove_equipment(self, category: str) -> None:
        """
        This function is used to remove an equipment, it might be used when the user drops the item.

        :param category: str: The string of the category of equipment to remove.
        :rtype: None
        """
        self.__setattr__(category, None)

    def get_previous_equipped_item(self, category: str) -> Union[None, IEquipmentItem]:
        """
        When equipping an item, the previous equipped item needs to be retrieved, to compute the
        removal of possible side effects on player.

        :param category: str: The string of the category of equipment to get.
        :rtype: Union[None, IEquipmentItem]
        """
        return self.__getattribute__(category)

    def is_equipped(self, equipment: IEquipmentItem) -> bool:
        """
        This function will check if an item it's equipped on the player.

        :param IEquipmentItem equipment: The equipment to identify.
        :rtype: bool
        """
        if self.__getattribute__(equipment.category) == equipment:
            return True
        return False

    def check_and_remove(self, selected_item: IItem) -> None:
        """
        Check if item it's equipped, and remove it.

        :param IItem selected_item: The equipment to verify.
        :rtype: None
        """
        if isinstance(selected_item, IEquipmentItem):
            for item in list(self.__dict__.values()):
                if item == selected_item:
                    self.remove_equipment(selected_item.category)

    def remove_side_effect(self, side_effect: ISideEffect) -> None:
        """
        Remove a side-effect from an equipment, when the duration has gone.

        :param ISideEffect side_effect: Side effect to be removed.
        :rtype: None
        """
        for item in list(self.__dict__.values()):
            if item is not None:
                for item_side_effect in item.side_effects:
                    if item_side_effect == side_effect:
                        item.side_effects.remove(side_effect)
