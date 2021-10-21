from typing import List

from project.conf import get_configuration
from project.interface import ISideEffect


class SideEffect(ISideEffect):
    def __init__(self, name: str, effect_type: str, attribute: str, base: int, duration: int, occurrence: str) -> None:
        self.name = name
        self.effect_type = effect_type
        self.attribute = attribute
        self.base = base
        self.duration = duration
        self.occurrence = occurrence


def instantiate_side_effects(side_effects_strings: List[str]) -> List[ISideEffect]:
    side_effects_library_dict = get_configuration('side_effects')
    side_effects: List[SideEffect] = []

    for side_effect_string in side_effects_strings:
        side_effect_dict = side_effects_library_dict.get(side_effect_string)
        side_effect = SideEffect(name=side_effect_string,
                                 effect_type=side_effect_dict.get('type'),
                                 attribute=side_effect_dict.get('attribute'),
                                 base=side_effect_dict.get('base'),
                                 duration=side_effect_dict.get('duration'),
                                 occurrence=side_effect_dict.get('occurrence'))
        side_effects.append(side_effect)

    return side_effects
