from typing import List

from project.conf import get_logger
from project.effect import SideEffect
from project.item import Bag, Equipment, Item


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
        self.health_points = self.health_points - damage
        if self.health_points <= 0:
            self.die()

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
        pass

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
        for item in self.side_effects:
            item.duration = item.duration - 1
            if item.duration <= 0:
                self.side_effects.remove(item)
