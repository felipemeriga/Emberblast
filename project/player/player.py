from typing import List

from project.conf import get_logger
from project.effect import SideEffect
from project.item import Bag, Equipment, Item, HealingItem, RecoveryItem


class Player:
    def __init__(self, name, job, race):
        self.job = job
        self.race = race
        self.name = name
        self.health_points = 10
        self.magic_points = 10
        self.move_speed = 0
        self.strength = 2
        self.intelligence = 2
        self.accuracy = 2
        self.armour = 2
        self.magic_resist = 2
        self.will = 2
        self.level = 1
        self.experience = 0
        self.side_effects: List[SideEffect] = []
        self._alive = True
        self.position = 0
        self._hidden = False
        self.bag = Bag()
        self.equipment = Equipment()

        self.add_attributes(self.job)
        self.add_attributes(self.race)

        # As players can suffer damage, or recover, or even cast magic
        # Life will represent the current player life and mana the remaining mana to cast magic
        # Health points and magic points will be the reference value and maximum value that
        # life and mana can reach
        self.life = self.health_points
        self.mana = self.magic_points

    def add_attributes(self, attributes=None):
        self.health_points += attributes.health_points
        self.magic_points += attributes.magic_points
        self.move_speed += attributes.move_speed
        self.strength += attributes.strength
        self.intelligence += attributes.intelligence
        self.accuracy += attributes.accuracy
        self.armour += attributes.armour
        self.magic_resist += attributes.magic_resist
        self.will += attributes.will

    def _level_up(self):
        raise NotImplementedError('Player::to_string() should be implemented!')

    def earn_xp(self, experience):
        self.experience = self.experience + experience
        if self.experience >= 100:
            self.experience = self.experience - 100
            self._level_up()

    def suffer_damage(self, damage: float) -> None:
        self.life = self.life - damage
        if self.life <= 0:
            self.die()

    def heal(self, attribute: str, value: int) -> None:
        if attribute == 'health_points':
            self.life = self.life + value
            if self.life > self.health_points:
                self.life = self.health_points
        elif attribute == 'magic_points':
            self.mana = self.mana + value
            if self.mana > self.magic_points:
                self.mana = self.magic_points

    def die(self) -> None:
        self._alive = False

    def is_alive(self) -> bool:
        return self._alive

    def set_position(self, position: str) -> None:
        self.position = position

    def set_hidden(self, state: bool) -> None:
        self._hidden = state

    def add_side_effect(self):
        side = SideEffect(name="rock", effect_type="buff", attribute="armour", base=3, duration=1,
                          occurrence="constant")
        self.side_effects.append(side)

    def is_hidden(self) -> bool:
        return self._hidden

    def use_item(self, item: Item) -> None:
        if isinstance(item, HealingItem):
            self.heal(item.attribute, item.base)
        elif isinstance(item, RecoveryItem):
            status = item.status
            found_side_effect = filter(lambda side_effect: status == side_effect.name, self.side_effects)
            if found_side_effect:
                self.side_effects.remove(next(found_side_effect))

    def get_attribute_real_value(self, attribute: str) -> int:
        """
        This method it's used for getting the real value of an attribute
        computing and considering buffs/debuffs from side-effects, as well as
        items equipped to him.

        """
        try:
            attribute = self.__getattribute__(attribute)
            result = attribute
            for effect in self.side_effects:
                if effect.attribute == attribute and effect.occurrence == 'constant':
                    result = result + effect.base
            return result
        except:
            logger = get_logger()
            logger.warn(f'Attribute: {attribute} does not exist, provide a valid one')
            return 0

    def compute_side_effect_duration(self) -> None:
        for side_effect in self.side_effects:
            side_effect.duration = side_effect.duration - 1
            if side_effect.duration <= 0:
                self.side_effects.remove(side_effect)
