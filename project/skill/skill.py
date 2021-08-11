import sys
from typing import Dict

from project.conf import get_configuration
from project.player import Player
from project.utils import SKILLS_SECTION


class Skill:
    def __init__(self, name: str, description: str, damage: int,
                 level_requirement: int, field: int, job: str) -> None:
        self.name = name
        self.description = description
        self.damage = damage
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
                damage=skill_values.get('damage'),
                level_requirement=skill_values.get('level_requirement'),
                field=skill_values.get('field'),
                job=skill_values.get('job'),
            )
        else:
            dynamic_skill_class = dynamic_skill_class_factory(skill_key, list(skill_values), Skill)
            custom_skill = dynamic_skill_class(name=skill_values.get('name'),
                                               description=skill_values.get('description'),
                                               damage=skill_values.get('damage'),
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

    def __init__(self, name: str, description: str, damage: int, level_requirement: int, field: int, job: str) -> None:
        super().__init__(name, description, damage, level_requirement, field, job)
