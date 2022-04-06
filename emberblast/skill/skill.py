import math
import random
import sys
from typing import Dict, List

from emberblast.communicator import communicator_injector
from emberblast.conf import get_configuration
from emberblast.effect import instantiate_side_effects
from emberblast.interface import IPlayer, ISkill, ISideEffect
from emberblast.utils import SKILLS_SECTION
from emberblast.utils.constants import EXPERIENCE_EARNED_ACTION

"""
This is the base class for defining a Skill, as all the skills are defined dynamically on the skills.yaml file, 
there is a set of attributes required for each skill, and their behavior will be basically the same, inflicting or 
healing players.

For extending this game functionality, concrete classes that extends Skill base class can be created, for modifying 
what happens when a character uses that skill. 

For example, the skill Fireball doesn't need to be override, only defined on skills.yaml file, because the purpose of 
that skill it's only inflicting damage.

Now, imagine Steal skill, instead of inflicting/healing, the purpose it's stealing someone's item. So that skill can
be overrided by a concrete classes, and we can call them custom skills.

So we have dynamic skills that follows the imposed behavior of the parent class Skill, and the custom Skills that 
extents that.
"""


@communicator_injector()
class Skill(ISkill):
    def __init__(self, name: str, description: str, base: int, cost: int,
                 kind: str, level_requirement: int, ranged: int, area: int, job: str,
                 base_attribute: str, side_effects: List[ISideEffect], applies_caster_only: bool,
                 punishment_side_effects: List[ISideEffect]) -> None:
        """
        Constructor of the Skill parent class.

        :param str name: The name of the skill.
        :param str description: Description of the skill.
        :param int base: Base damage/recover capacity if the skill.
        :param int cost: Amount of mana to cast/execute.
        :param str base_attribute: The base attribute that will be evaluated when calculating damage/recover result.
        :param List[ISideEffect] side_effects: Side effects that the skill applies.
        :param List[ISideEffect] punishment_side_effects: Some skills punish the player to execute it, inflicting
        negative side effects on him.

        :rtype: None.
        """
        self.name = name
        self.description = description
        self.base = base
        self.cost = cost
        self.kind = kind
        self.level_requirement = level_requirement
        self.ranged = ranged
        self.area = area
        self.job = job
        self.base_attribute = base_attribute
        self.side_effects = side_effects
        self.applies_caster_only = applies_caster_only
        self.punishment_side_effects = punishment_side_effects

    def calculate_damage(self, player: IPlayer, dice_norm_result: float) -> float:
        return self.base + dice_norm_result * player.get_attribute_real_value(
            self.base_attribute) + player.get_attribute_real_value(self.base_attribute) / 2

    def calculate_defense(self, foe: IPlayer, ) -> int:
        # Skills can be magical, based on intelligence, and physical, based on strength
        # For magical skills,
        # foe will use magic resist and for physical, armour
        if self.base_attribute == 'strength':
            defense_attribute = 'armour'
        else:
            defense_attribute = 'magic_resist'

        return foe.get_defense_value(defense_attribute)

    def calculate_recover(self, player: IPlayer, dice_norm_result: float) -> int:
        return math.ceil(
            self.base + dice_norm_result * player.get_attribute_real_value('intelligence'))

    def execute(self, player: IPlayer, foes: List[IPlayer], dice_norm_result: float) -> None:
        kill = False
        successful_skill = False
        player.spend_mana(self.cost)
        self.communicator.informer.spent_mana(player.name, self.cost, self.name)
        for foe in foes:
            if self.kind == 'inflict':
                damage = self.calculate_damage(player, dice_norm_result)
                defense = self.calculate_defense(foe)
                damage = math.ceil(damage - defense)
                if damage > 0:
                    successful_skill = True
                    foe.suffer_damage(damage)
                    self.communicator.informer.suffer_damage(player, foe, damage)
                else:
                    self.communicator.informer.missed(player, foe)
            elif self.kind == 'recover':
                recover_result = self.calculate_recover(player, dice_norm_result)
                foe.heal('health_points', recover_result)
                self.communicator.informer.heal(player, foe, recover_result)
            for side_effect in self.side_effects:
                if successful_skill:
                    foe.add_side_effect(side_effect)
                    self.communicator.informer.add_side_effect(foe.name, side_effect)
            for side_effect in self.punishment_side_effects:
                player.add_side_effect(side_effect)
                self.communicator.informer.add_side_effect(player.name, side_effect)
            if not foe.is_alive():
                kill = True
            print('\n')
        self.check_experience(player, successful_skill, kill)

    def check_experience(self, player: IPlayer, successful_skill: bool, killed: bool) -> None:
        if successful_skill:
            experience = get_configuration(EXPERIENCE_EARNED_ACTION).get('attack', 0)
            player.earn_xp(experience)
            self.communicator.informer.player_earned_xp(player_name=player.name, xp=experience)
        if killed:
            experience = get_configuration(EXPERIENCE_EARNED_ACTION).get('kill', 0)
            player.earn_xp(experience)
            self.communicator.informer.player_earned_xp(player_name=player.name, xp=experience)


instantiated_skills: Dict = {}


def dynamic_skill_class_factory(name: str, argument_names: List, base_class: type):
    """
    Skills are defined in the configuration file conf.yaml, this class helps in dynamically creating,
    at runtime, classes that can be instantiated with the name of the skill.

    :param str name: The name of the dynamic class.
    :param List argument_names: The attributes list of the class.
    :param type base_class: The base class, from where the dynamic class will inherit properties.

    :rtype: None.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in argument_names:
                raise TypeError("Argument %s not valid for %s"
                                % (key, self.__class__.__name__))
        base_class.__init__(self, **kwargs)

    new_class = type(name, (base_class,), {"__init__": __init__})
    return new_class


def get_instantiated_skill(skill_dict: Dict) -> ISkill:
    """
    Receiving a dictionary with all the characteristics of a Skill, this dictionary will be instantiated in a class that
    represents this Skill.

    :param Dict skill_dict: The name of the dynamic class.

    :rtype: ISkill.
    """
    custom_skill = None
    skill_name = list(skill_dict.keys())[0]
    if skill_name not in instantiated_skills:
        skill_values = skill_dict.get(skill_name)
        skill_pkg = sys.modules[__package__].__getattribute__('skill')
        side_effects = instantiate_side_effects(skill_values.get('side_effects'))
        punishment_side_effects = instantiate_side_effects(skill_values.get('punishment_side_effects'))

        if skill_name in skill_pkg.__dict__:
            prev_defined_class = getattr(skill_pkg, skill_name)
            custom_skill = prev_defined_class(
                name=skill_values.get('name'),
                description=skill_values.get('description'),
                base=skill_values.get('base'),
                cost=skill_values.get('cost'),
                kind=skill_values.get('kind'),
                level_requirement=skill_values.get('level_requirement'),
                ranged=skill_values.get('ranged'),
                area=skill_values.get('area'),
                job=skill_values.get('job'),
                base_attribute=skill_values.get('base_attribute'),
                side_effects=side_effects,
                applies_caster_only=skill_values.get('applies_caster_only'),
                punishment_side_effects=punishment_side_effects)
        else:
            dynamic_skill_class = dynamic_skill_class_factory(skill_name, list(skill_values), Skill)
            custom_skill = dynamic_skill_class(name=skill_values.get('name'),
                                               description=skill_values.get('description'),
                                               base=skill_values.get('base'),
                                               cost=skill_values.get('cost'),
                                               kind=skill_values.get('kind'),
                                               level_requirement=skill_values.get('level_requirement'),
                                               ranged=skill_values.get('ranged'),
                                               area=skill_values.get('area'),
                                               job=skill_values.get('job'),
                                               base_attribute=skill_values.get('base_attribute'),
                                               side_effects=side_effects,
                                               applies_caster_only=skill_values.get('applies_caster_only'),
                                               punishment_side_effects=punishment_side_effects)
        instantiated_skills[skill_name] = custom_skill
    else:
        custom_skill = instantiated_skills[skill_name]

    return custom_skill


def get_player_available_skills(player: IPlayer) -> List[ISkill]:
    """
    Skills can be unlocked/revealed for players depending their levels and jobs, this method compare the current
    attributes of a player, will all the skills, to check which ones this current player has eligibility to use.

    :param IPlayer player: The current player to discover new skills.

    :rtype: List[ISkill].
    """
    skill_dicts = get_configuration(SKILLS_SECTION)
    available_skills: List[ISkill] = []

    for key, value in skill_dicts.items():
        if player.job.get_name() == value.get('job') and player.level >= value.get(
                'level_requirement') and player.mana > value.get('cost'):
            available_skills.append(get_instantiated_skill({key: value}))

    return available_skills


"""
--------------- EXTENDED SKILLS ---------------

For default, skills are intended to heal or cause damage to one player, that is why all the skills present in the
skills configuration file, has a default instantiating mechanism that inherits from Skill parent class, that has the 
execute method, which simply executes the skill. But you can override the functionality of skills from configuration
file, creating a concrete class above here and override the methods from Skill class.

This functionally extends the basic implementation, adding more possibilities to the skills in the game. For example,
the Steal skill from Rogue class, instead of it causing damage or healing someone, this class is written above, 
making possible from a player to steal the item from another one.

"""


class Steal(Skill):

    def __init__(self, name: str, description: str, base: int, cost: int, kind: str, level_requirement: int,
                 ranged: int, area: int, job: str, base_attribute: str, side_effects: List[ISideEffect],
                 applies_caster_only: bool, punishment_side_effects: List[ISideEffect]) -> None:
        super().__init__(name, description, base, cost, kind, level_requirement, ranged, area, job,
                         base_attribute, side_effects, applies_caster_only, punishment_side_effects)

    def execute(self, player: IPlayer, foes: List[IPlayer], dice_norm_result: float) -> None:
        successful_steal = False
        foe = foes[0]
        items = foe.bag.items
        if len(items) > 0:
            stolen_item = random.choice(items)
            foe.bag.remove_item(stolen_item)
            player.bag.add_item(stolen_item)
            self.communicator.informer.player_stole_item(player.name, foe.name, stolen_item.name, stolen_item.tier)
            successful_steal = True
        else:
            self.communicator.informer.player_fail_stole_item(player.name, foe.name)
        self.check_experience(player, successful_steal, False)


class Leech(Skill):

    def __init__(self, name: str, description: str, base: int, cost: int, kind: str, level_requirement: int,
                 ranged: int, area: int, job: str, base_attribute: str, side_effects: List[ISideEffect],
                 applies_caster_only: bool, punishment_side_effects: List[ISideEffect]) -> None:
        super().__init__(name, description, base, cost, kind, level_requirement, ranged, area, job, base_attribute,
                         side_effects, applies_caster_only, punishment_side_effects)

    def execute(self, player: IPlayer, foes: List[IPlayer], dice_norm_result: float) -> None:
        successful_skill = False
        kill = False

        player.spend_mana(self.cost)
        self.communicator.informer.spent_mana(player.name, self.cost, self.name)
        foe = foes[0]
        damage = int(self.calculate_damage(player, dice_norm_result))
        defense = self.calculate_defense(foe)
        foe.suffer_damage(damage - defense)
        self.communicator.informer.suffer_damage(player, foe, damage)
        player.heal('health_points', damage)
        self.communicator.informer.heal(player, player, damage)

        if damage - defense > 0:
            successful_skill = True
        if not foe.is_alive():
            kill = True

        self.check_experience(player, successful_skill, kill)
