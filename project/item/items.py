from typing import List


class Item:

    def __init__(self, tier: str, description: str) -> None:
        self.tier = tier
        self.description = description


class HealingItem(Item):

    def __init__(self, tier: str, description: str, attribute: str, base: int) -> None:
        self.attribute = attribute
        self.base = base
        super().__init__(tier, description)


class RecoveryItem(Item):

    def __init__(self, tier: str, description: str, status: str) -> None:
        self.status = status
        super().__init__(tier, description)


class EquipmentItem(Item):

    def __init__(self, tier: str, description: str, attribute: str, base: int, side_effects: List[str]) -> None:
        self.attribute = attribute
        self.base = base
        self.side_effects = side_effects
        super().__init__(tier, description)
