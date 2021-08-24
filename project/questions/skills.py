from typing import Union, List

import emojis
from InquirerPy import prompt

from project.interface import ISkill


def select_skill(available_skills: List[ISkill]) -> Union[str, bool, list, ISkill]:
    choices = []
    for skill in available_skills:
        area_range_string = ''

        if skill.ranged == 0:
            area_range_string = '/ melee skill'
        elif skill.ranged > 0 and skill.area == 0:
            area_range_string = '/ ranged skill with range of {range}, single target'.format(range=skill.ranged)
        elif skill.ranged > 0 and skill.area > 0:
            area_range_string = '/ ranged skill with range of {range}, area damage of radius {area}'.format(
                range=skill.ranged, area=skill.area)
        choices.append({
            'name': emojis.encode('{name} / type: {kind} / cost: {cost} mana :blue_heart: {additional}'.format(
                name=skill.name, kind=skill.kind, cost=skill.cost, additional=area_range_string
            )),
            'value': skill
        })
    choices.append({
        'name': emojis.encode('Cancel :x: '),
        'value': None
    })
    skill_questions = [
        {
            'type': 'list',
            'message': emojis.encode('Select a skill: :fire:'),
            'choices': choices,
            'default': available_skills[0],
            'invalid_message': 'You need to select at least one skill',
            'show_cursor': True,
            'max_height': '100'
        }
    ]

    result = prompt(questions=skill_questions)
    selected_skill = result[0]
    return selected_skill
