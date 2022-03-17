from typing import List

from emberblast.conf import get_configuration
from emberblast.interface import ISideEffect


class SideEffect(ISideEffect):

    def __init__(self, name: str, effect_type: str, attribute: str, base: int, duration: int, occurrence: str) -> None:
        """
        Constructor of the Skill parent class.

        :param str name: The name of the side-effect.
        :param str effect_type: The type of it, if it's a debuff or buff.
        :param str attribute: The attribute that the effect will change.
        :param int base: The quantity of the attribute that will be changed.
        :param int duration: The number of turns that this effect stays.
        :param str occurrence: If it applies one single time, or every turn.

        :rtype: None.
        """
        self.name = name
        self.effect_type = effect_type
        self.attribute = attribute
        self.base = base
        self.duration = duration
        self.occurrence = occurrence


def instantiate_side_effects(side_effects_strings: List[str]) -> List[ISideEffect]:
    """
    This class will receive a list of strings that represents the names of each side-effects, those names of
    side-effects will be queried from the configuration, and instantiated to be ready to use.

    :param List[str] side_effects_strings: List with the name os the effects.

    :rtype: List[ISideEffect].
    """
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
