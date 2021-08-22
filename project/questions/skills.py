from typing import Union, List

import emojis
from InquirerPy import prompt

from project.interface import ISkill


def select_skill(available_skills: List[ISkill]) -> Union[str, bool, list, ISkill]:
    choices = []
    for skill in available_skills:
        choices.append({
            'name': emojis.encode('{name} - type: {kind} - {range} damage - {cost} mana :blue_heart:'.format(
                name=skill.name, kind=skill.kind, range='area' if skill.field > 0 else 'single', cost=skill.cost
            )),
            'value': skill
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
