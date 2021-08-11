from typing import List, Union

from project.conf import get_logger
from project.effect import SideEffect
from project.interface import IPlayer, IItem, IHealingItem, IRecoveryItem, IBag, IJob, IRace, IEquipment


class Player(IPlayer):
    def __init__(self, name: str, job: IJob, race: IRace, bag: IBag, equipment: IEquipment) -> None:
        """
       Constructor

        :param str name: Player's name.
        :param IJob job: The selected job.
        :param IRace race: The selected race.
        :param IBag bag: Player's bag.
        :param IEquipment equipment: Player's equipment.
        :rtype: None
        """
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
        self.position = ''
        self._hidden = False
        self.bag = bag
        self.equipment = equipment

        self.add_attributes(self.job)
        self.add_attributes(self.race)

        # As players can suffer damage, or recover, or even cast magic
        # Life will represent the current player life and mana the remaining mana to cast magic
        # Health points and magic points will be the reference value and maximum value that
        # life and mana can reach
        self.life = self.health_points
        self.mana = self.magic_points

    def add_attributes(self, attributes: Union[IJob, IRace] = None) -> None:
        """
       Every action generates experience, and when reaching 100, character will level up.

        :param Union[Job, Race] attributes: Value to be computed.
        :rtype: None
        """
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

    def earn_xp(self, experience: int) -> None:
        """
       Every action generates experience, and when reaching 100, character will level up.

        :param int experience: Value to be computed.
        :rtype: None
        """
        self.experience = self.experience + experience
        if self.experience >= 100:
            self.experience = self.experience - 100
            self._level_up()

    def suffer_damage(self, damage: float) -> None:
        """
       Method that is used when character has suffered some damage.

        :param int damage: Value to be decreased.
        :rtype: None
        """
        self.life = self.life - damage
        if self.life <= 0:
            self.die()

    def spend_mana(self, quantity: int) -> None:
        """
       Method that is used when character has spent mana with some skill, or due
       to side effects.

        :param int quantity: Value to be decreased.
        :rtype: None
        """
        self.mana = self.mana - quantity

    def heal(self, attribute: str, value: int) -> None:
        """
       Method that is used when character has its life or mana recovered,
       from a skill or item.

        :param str attribute: which attribute to be healed.
        :param int value: The life/mana to be healed.
        :rtype: None
        """
        if attribute == 'health_points':
            self.life = self.life + value
            if self.life > self.health_points:
                self.life = self.health_points
        elif attribute == 'magic_points':
            self.mana = self.mana + value
            if self.mana > self.magic_points:
                self.mana = self.magic_points

    def die(self) -> None:
        """
       Kill the character due to damage suffered or a side effect.

        :rtype: None
        """
        self._alive = False

    def is_alive(self) -> bool:
        """
       Check if player is alive or not.

        :rtype: bool
        """
        return self._alive

    def set_position(self, position: str) -> None:
        """
       Set new position of the player, this method is called when player it's moving through the map.

        :param str position: The position where the player is located.
        :rtype: None
        """
        self.position = position

    def set_hidden(self, state: bool) -> None:
        """
       Turn on/off into hidden state, so it can't be found by another players.

        :param bool state: boolean to turn hidden(True) or visible(False).
        :rtype: None
        """
        self._hidden = state

    def add_side_effect(self):
        """
       To add a new side effect in the player.

        :rtype: None
        """
        side = SideEffect(name="poison", effect_type="debuff", attribute="health_points", base=1, duration=3,
                          occurrence="iterated")
        self.side_effects.append(side)

    def is_hidden(self) -> bool:
        """
       Returns if the player is hidden or not.

        :rtype: bool
        """
        return self._hidden

    def use_item(self, item: IItem) -> None:
        """
       This function computes the usage of a healing or recover item.

        :param IItem item: The item to be used.
        :rtype: None
        """
        if isinstance(item, IHealingItem):
            self.heal(item.attribute, item.base)
        elif isinstance(item, IRecoveryItem):
            status = item.status
            found_side_effect = filter(lambda side_effect: status == side_effect.name, self.side_effects)
            if found_side_effect:
                self.side_effects.remove(next(found_side_effect))

    def get_attribute_real_value(self, attribute: str) -> int:
        """
        This method it's used for getting the real value of an attribute
        computing and considering buffs/debuffs from side-effects, as well as
        items equipped to him.

        :param str attribute: Attribute to be computed.
        :rtype: int
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

    def compute_iterated_side_effects(self) -> None:
        """
        There are side effects that are iterated, which means that each turn they will buff/debuff
        the character attributes. So, each turn this method will be called to apply those effects in the player.

        :rtype: None
        """
        iterated_side_effects = [x for x in
                                 filter(lambda effect: effect.occurrence == 'iterated', self.side_effects)]

        for side_effect in iterated_side_effects:
            if side_effect.effect_type == 'buff':
                self.heal(side_effect.attribute, side_effect.base)
            elif side_effect.effect_type == 'debuff':
                if side_effect.attribute == 'health_points':
                    self.suffer_damage(side_effect.base)
                elif side_effect.attribute == 'magic_points':
                    self.spend_mana(side_effect.base)

    def compute_side_effect_duration(self) -> None:
        """
        Each side effects may last in the player depending its duration configuration,
        each turn, this method will be called to compute this duration, when the duration
        reaches to 0, it will be excluded from the character.

        :rtype: None
        """
        for side_effect in self.side_effects:
            side_effect.duration = side_effect.duration - 1
            if side_effect.duration <= 0:
                self.side_effects.remove(side_effect)
