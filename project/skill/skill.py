import sys
from typing import Dict

from project.conf import get_configuration
from project.player import Player
from project.utils import SKILLS_SECTION

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


class Skill:
    def __init__(self, name: str, description: str, base: int,
                 kind: str, level_requirement: int, field: int, job: str) -> None:
        """
        Constructor of the Skill parent class.

        :param str name: The name of the skill.
        :param str name: The name of the skill.
        :param str name: The name of the skill.
        :param str name: The name of the skill.

        :rtype: None.
        """
        self.name = name
        self.description = description
        self.base = base
        self.kind = kind
        self.level_requirement = level_requirement
        self.field = field
        self.job = job

    def execute(self, player: Player) -> None:
        pass


instantiated_skills: Dict = {}


def dynamic_skill_class_factory(name, argument_names, base_class):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in argument_names:
                raise TypeError("Argument %s not valid for %s"
                                % (key, self.__class__.__name__))
        base_class.__init__(self, **kwargs)

    new_class = type(name, (base_class,), {"__init__": __init__})
    return new_class


def get_instantiated_skill(skill_dict: Dict) -> Skill:
    custom_skill = None
    skill_key = list(skill_dict.keys())[0]
    skill_values = skill_dict.get(skill_key)
    if skill_key not in instantiated_skills:
        skill_pkg = sys.modules[__package__].__getattribute__('skill')
        if skill_key in skill_pkg.__dict__:
            prev_defined_class = getattr(skill_pkg, skill_key)
            custom_skill = prev_defined_class(
                name=skill_values.get('name'),
                description=skill_values.get('description'),
                base=skill_values.get('base'),
                kind=skill_values.get('kind'),
                level_requirement=skill_values.get('level_requirement'),
                field=skill_values.get('field'),
                job=skill_values.get('job'),
            )
        else:
            dynamic_skill_class = dynamic_skill_class_factory(skill_key, list(skill_values), Skill)
            custom_skill = dynamic_skill_class(name=skill_values.get('name'),
                                               description=skill_values.get('description'),
                                               base=skill_values.get('base'),
                                               kind=skill_values.get('kind'),
                                               level_requirement=skill_values.get('level_requirement'),
                                               field=skill_values.get('field'),
                                               job=skill_values.get('job'))
        instantiated_skills[skill_key] = custom_skill
    else:
        custom_skill = instantiated_skills[skill_key]

    return custom_skill


def get_player_available_skills(player: Player) -> Dict:
    skill_dicts = get_configuration(SKILLS_SECTION)
    available_skills = {k: v for (k, v) in skill_dicts.items() if
                        player.job.get_name() == v.get('job') and player.level == v.get('level_requirement')}

    return available_skills


class Steal(Skill):

    def __init__(self, name: str, description: str, base: int, kind: str, level_requirement: int, field: int,
                 job: str) -> None:
        super().__init__(name, description, base, kind, level_requirement, field, job)
