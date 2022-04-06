import math
from typing import Union, List, Dict

from emberblast.conf import get_logger
from emberblast.effect import SideEffect
from emberblast.interface import IPlayer, IItem, IHealingItem, IRecoveryItem, IBag, IJob, IRace, IEquipment, ISideEffect
from emberblast.skill import get_player_available_skills


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
        self.health_points = 25
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
        self.side_effects = []
        self.skills = []
        self._alive = True
        self.position = ''
        self._hidden = False
        self._defense_mode = False
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

    def level_up(self, improvements: Union[List, Dict]):
        raise NotImplementedError('Player::to_string() should be implemented!')

    def earn_xp(self, experience: int) -> None:
        """
        Every action generates experience, and when reaching 100, character will level up.

        :param int experience: Value to be computed.
        :rtype: None
        """
        self.experience = self.experience + experience

    def suffer_damage(self, damage: float) -> None:
        """
        Method that is used when character has suffered some damage.

        :param int damage: Value to be decreased.
        :rtype: None
        """
        self.life = int(self.life - damage)
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

    def get_ranged_attack_area(self) -> int:
        """
        Get the radius of the reach of ranged attacks

        :rtype: int
        """
        if self.job.attack_type == 'melee':
            return 0
        return math.floor(1 + self.accuracy / 3)

    def set_hidden(self, state: bool) -> None:
        """
        Turn on/off into hidden state, so it can't be found by another players.

        :param bool state: boolean to turn hidden(True) or visible(False).
        :rtype: None
        """
        self._hidden = state

    def is_hidden(self) -> bool:
        """
        Returns if the player is hidden or not.

        :rtype: bool
        """
        return self._hidden

    def reset_last_action(self) -> None:
        """
        Players can get into hidden or defensive state, until they play again in the next turn, this method is called
        everytime a player is supposed to start its turn, in order to reset actions from turns before.

        :rtype: bool
        """
        self.set_hidden(False)
        self.set_defense_mode(False)

    def set_defense_mode(self, state: bool) -> None:
        """
        Turn on/off into defensive state, in this state player's defenses are increased by double until his next play.

        :param bool state: boolean to turn hidden(True) or visible(False).
        :rtype: None
        """
        self._defense_mode = state

    def is_defending(self) -> bool:
        """
        Returns if the player is in defensive state.

        :rtype: bool
        """
        return self._defense_mode

    def get_defense_value(self, kind: str) -> int:
        """
        When in defensive state, players base armour and magic resist may be increased by double, this methods compute
        all those conditions and return the right value.

        :param str kind: If it's magical defense or armour.
        :rtype: int
        """
        base_defense = 0
        if kind == 'magic_resist':
            base_defense = self.magic_resist
        elif kind == 'armour':
            base_defense = self.armour

        return base_defense * 2 if self.is_defending() else base_defense

    def add_side_effect(self, new_side_effect: ISideEffect) -> None:
        """
       To add a new side effect in the player.

        :rtype: None
        """
        for i in range(len(self.side_effects)):
            existing_side_effect = self.side_effects[i]
            if existing_side_effect.name == new_side_effect.name:
                self.side_effects[i] = new_side_effect
                return
        self.side_effects.append(new_side_effect)

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

    def get_attribute_real_value(self, attribute: str, usage: str = 'all') -> int:
        """
        This method it's used for getting the real value of an attribute
        computing and considering buffs/debuffs from side-effects, as well as
        items equipped to him.

        :param str attribute: Attribute to be computed.
        :param str usage: If it will get melee, ranged or all equipments.
        :rtype: int
        """
        try:
            if attribute == 'armour' or attribute == 'magic_resist':
                result = self.get_defense_value(attribute)
            else:
                result = self.__getattribute__(attribute)
            for effect in self.side_effects:
                if effect.attribute == attribute and effect.occurrence == 'constant':
                    result = result + effect.base

            result = result + self.equipment.get_attribute_addition(attribute, usage)
            return result
        except:
            logger = get_logger()
            logger.warn(f'Attribute: {attribute} does not exist, provide a valid one')
            return 0

    def remove_side_effects(self, side_effects: List[ISideEffect]) -> None:
        """
        Method for helping removing a list of side effects from player.

        :param List[SideEffect] side_effects: side effects to be removed.
        :rtype: None
        """
        for side_effect in side_effects:
            if side_effect in self.side_effects:
                self.side_effects.remove(side_effect)

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

    def compute_side_effect_duration(self) -> List[ISideEffect]:
        """
        Each side effects may last in the player depending its duration configuration,
        each turn, this method will be called to compute this duration, when the duration
        reaches to 0, it will be excluded from the character.

        :rtype: None
        """
        ended_side_effects = []
        for side_effect in self.side_effects:
            side_effect.duration = side_effect.duration - 1
            if side_effect.duration <= 0:
                ended_side_effects.append(side_effect)
                self.side_effects.remove(side_effect)
                self.equipment.remove_side_effect(side_effect)
        return ended_side_effects

    def refresh_skills_list(self) -> None:
        """
        Depending on player's level, new skills can be revealed, this method checks if the player has new skills
        to learn, and ideally should be executed in the beginning of the game of when the player levels up.

        :rtype: None
        """
        available_skills = get_player_available_skills(self)
        self.skills = available_skills
