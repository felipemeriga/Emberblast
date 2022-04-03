import random
from copy import copy
from typing import Dict

from emberblast.conf import get_configuration
from emberblast.interface import IRace, IJob
from emberblast.utils import LEVEL_UP_INCREMENT, JOBS_SECTION, RACES_SECTION


def improve_attributes_randomly() -> Dict:
    """
    This function can be used by bots and humans, and it will randomly pick 2 attributes to upgrade.

    :rtype: dict.
    """
    level_up_increment_attributes = copy(get_configuration(LEVEL_UP_INCREMENT))
    first_key, first_val = random.choice(list(level_up_increment_attributes.items()))
    level_up_increment_attributes.pop(first_key, None)
    second_key, second_val = random.choice(list(level_up_increment_attributes.items()))

    return {
        first_key: first_val,
        second_key: second_val
    }


def improve_attributes_automatically(job: IJob, race: IRace) -> Dict:
    """
    This function can be used by both bots and humans to upgrade their attributes, this method
    Takes the result of the combination of the attributes from job and race, and select the greater ones to improve.

    :param Job job: base job of the player.
    :param Race race: base race of the player.
    :rtype: dict.
    """
    unsorted_attributes_dict = {}
    chosen_attributes = {}
    job_attribute_points = get_configuration(JOBS_SECTION).get(job)
    race_attribute_points = get_configuration(RACES_SECTION).get(race)
    level_up_increment_attributes = get_configuration(LEVEL_UP_INCREMENT)

    for key, value in level_up_increment_attributes.items():
        unsorted_attributes_dict[key] = job_attribute_points[key] + race_attribute_points[key]

    sorted_list = iter(sorted(unsorted_attributes_dict, key=unsorted_attributes_dict.get, reverse=True))
    first_attribute = next(sorted_list)
    second_attribute = next(sorted_list)
    not_allowed_together_list = ['magic_points', 'health_points']

    # As HP and MP, always have a higher distribution percentage, most probably they will always be the first two
    # elements of the sorted list, so to prevent all bots to always improve only these attributes, this IF is necessary.
    if first_attribute in not_allowed_together_list and second_attribute in not_allowed_together_list:
        second_attribute = next(sorted_list)

    chosen_attributes[first_attribute] = level_up_increment_attributes.get(first_attribute, 0)
    chosen_attributes[second_attribute] = level_up_increment_attributes.get(second_attribute, 0)

    return chosen_attributes
