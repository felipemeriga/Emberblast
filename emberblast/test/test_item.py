from typing import Callable

from .test import BaseTestCase
from emberblast.item import get_random_item, Bag
from emberblast.interface import IItem, IHealingItem, IEquipmentItem, IRecoveryItem


def mock_recovery_item(tier: str = 'common') -> Callable:
    def wrapper(func):
        item = get_random_item(tier, 'recovery')
        setattr(func, 'mock_recovery_item', item)
        return func

    return wrapper


def mock_equipment_item(tier: str = 'common') -> Callable:
    def wrapper(func):
        item = get_random_item(tier, 'equipment')
        setattr(func, 'mock_equipment_item', item)
        return func

    return wrapper


def mock_healing_item(tier: str = 'common') -> Callable:
    def wrapper(func):
        item = get_random_item(tier, 'healing')
        setattr(func, 'mock_healing_item', item)
        return func

    return wrapper


class TestModuleItem(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestModuleItem, self).__init__(*args, **kwargs)
        self.bag = Bag()

    def test_get_random_item(self) -> None:
        item = get_random_item(tier='common', item_type='healing')
        self.assertIsInstance(item, IItem)

    def test_get_random_healing(self) -> None:
        item = get_random_item(tier='rare', item_type='healing')
        self.assertIsInstance(item, IHealingItem)

    def test_get_random_equipment(self) -> None:
        item = get_random_item(tier='legendary', item_type='equipment')
        self.assertIsInstance(item, IEquipmentItem)

    def test_get_random_recoverable(self) -> None:
        item = get_random_item(tier='common', item_type='recovery')
        self.assertIsInstance(item, IRecoveryItem)

    def test_bag_get_equipments(self) -> None:
        equipment_item = get_random_item(tier='legendary', item_type='equipment')
        self.bag.add_item(equipment_item)
        self.assertGreater(len(self.bag.get_equipments()), 0)

    def test_bag_get_usable_items(self) -> None:
        item = get_random_item(tier='common', item_type='healing')
        self.bag.add_item(item)
        self.assertGreater(len(self.bag.get_usable_items()), 0)

    def test_bag_weight_measurement(self) -> None:
        item = get_random_item(tier='common', item_type='healing')
        before_new_item_weight = self.bag.weight
        self.bag.add_item(item)
        after_item_add_weight = self.bag.weight
        self.assertEqual(self.bag.weight, before_new_item_weight + item.weight)
        self.bag.remove_item(item)
        self.assertEqual(self.bag.weight, after_item_add_weight - item.weight)

    def test_bag_has_item_type(self) -> None:
        healing_item = get_random_item(tier='common', item_type='healing')
        equipment_item = get_random_item(tier='legendary', item_type='equipment')
        recovery_item = get_random_item(tier='common', item_type='recovery')

        self.bag.add_item(healing_item)
        self.bag.add_item(equipment_item)
        self.bag.add_item(recovery_item)

        self.assertTrue(self.bag.has_item_type(is_usable=True))
        self.assertTrue(self.bag.has_item_type(is_equipment=True))
