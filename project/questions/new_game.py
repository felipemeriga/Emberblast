import emojis
from prompt_toolkit.validation import Validator, ValidationError

from project.conf import get_configuration
from project.utils import GAME_SECTION, RACES_SECTION, JOBS_SECTION


class MaxBotsInputValidator(Validator):
    def validate(self, document):
        max_bot_number = get_configuration(GAME_SECTION).get('max_number_bots')
        if not document.text.isnumeric():
            raise ValidationError(
                message="Input should be a number",
                cursor_position=document.cursor_position,
            )
        else:
            if int(document.text) > max_bot_number or int(document.text) <= 0:
                raise ValidationError(
                    message="The number of boots needs to be minimum 1 and maximum {maximum}".format(
                        maximum=max_bot_number),
                    cursor_position=document.cursor_position,
                )


BEGIN_GAME_QUESTIONS = [
    {
        "type": "list",
        "message": emojis.encode(':video_game: Select the Game Type '),
        "choices": ["Deathmatch", "Clan"],
        "name": "game"
    },
    {
        "type": "list",
        "message": emojis.encode(':sunrise: Select the map '),
        "choices": ["Millstone Plains", "Firebend Vulcan", "Lerwick Mountains"],
        "name": "map"
    },
    {
        "type": "input",
        "message": emojis.encode(':computer: How many bots are you playing against '),
        "validate": MaxBotsInputValidator(),
        "invalid_message": "Input should be number.",
        "default": "4",
        "name": "bots_number"
    },
    {
        "type": "input",
        "message": emojis.encode(':man: Please enter your character name '),
        "validate": lambda input: 0 < len(input) < 20,
        "invalid_message": "minimum of 1 letters, max of 20 letters",
        "name": "nickname"
    },
    {
        "type": "list",
        "message": emojis.encode(':skull: Please enter your character race? '),
        "choices": get_configuration(RACES_SECTION).keys(),
        "name": "race"
    },
    {
        "type": "list",
        "message": emojis.encode(':name_badge: Please enter your character job? '),
        "choices": get_configuration(JOBS_SECTION).keys(),
        "name": "job"
    },
]