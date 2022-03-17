import random
from copy import copy
from typing import Union, Dict, List

from InquirerPy import prompt
import emojis

from emberblast.conf import get_configuration
from emberblast.utils import LEVEL_UP_INCREMENT, JOBS_SECTION, RACES_SECTION
from emberblast.interface import IJob, IRace, ILevelUpQuestioner


class LevelUpQuestionerCMD(ILevelUpQuestioner):

    def ask_attributes_to_improve(self) -> Union[str, bool, list, List]:
        level_up_increment_attributes = get_configuration(LEVEL_UP_INCREMENT)
        health_points = level_up_increment_attributes.get('health_points', 5)
        magic_points = level_up_increment_attributes.get('magic_points', 5)
        move_speed = level_up_increment_attributes.get('move_speed', 1)
        strength = level_up_increment_attributes.get('strength', 3)
        intelligence = level_up_increment_attributes.get('intelligence', 3)
        accuracy = level_up_increment_attributes.get('accuracy', 1)
        armour = level_up_increment_attributes.get('armour', 3)
        magic_resist = level_up_increment_attributes.get('magic_resist', 3)
        will = level_up_increment_attributes.get('will', 3)

        level_up_questions = [
            {
                "type": "list",
                "message": "Select an action:",
                "choices": [
                    {
                        "name": emojis.encode("+{points} Health Points :green_heart:".format(points=health_points)),
                        "value": {
                            "attribute": "health_points",
                            "value": health_points
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Magic Points :blue_heart:".format(points=magic_points)),
                        "value": {
                            "attribute": "magic_points",
                            "value": magic_points
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Move Speed :runner:".format(points=move_speed)),
                        "value": {
                            "attribute": "move_speed",
                            "value": move_speed
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Strength :punch:".format(points=strength)),
                        "value": {
                            "attribute": "strength",
                            "value": strength
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Intelligence :books:".format(points=intelligence)),
                        "value": {
                            "attribute": "intelligence",
                            "value": intelligence
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Accuracy :dart:".format(points=accuracy)),
                        "value": {
                            "attribute": "accuracy",
                            "value": accuracy
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Armour :anger:".format(points=armour)),
                        "value": {
                            "attribute": "armour",
                            "value": armour
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Magic Resist :cyclone:".format(points=magic_resist)),
                        "value": {
                            "attribute": "magic_resist",
                            "value": magic_resist
                        }
                    },
                    {
                        "name": emojis.encode("+{points} Will :pray:".format(points=will)),
                        "value": {
                            "attribute": "will",
                            "value": will
                        }
                    },
                ],
                "default": None,
                "multiselect": True,
                "validate": lambda selected: len(selected) == 2,
                "invalid_message": "You need to select 2 attributes to improve!",
                "show_cursor": True,
                "max_height": "100"
            },
        ]

        result = prompt(questions=level_up_questions)
        return result[0]


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
