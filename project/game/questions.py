from prompt_toolkit.validation import Validator, ValidationError

from project.conf.conf import get_configuration
from project.utils.constants import GAME_SECTION


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
        "message": "Select the Game Type",
        "choices": ["Deathmatch", "Clan"],
        "name": "game"
    },
    {
        "type": "list",
        "message": "Select the map",
        "choices": ["Millstone Plains", "Firebend Vulcan", "Lerwick Mountains"],
        "name": "map"
    },
    {
        "type": "input",
        "message": "How many bots are you playing against? ",
        "validate": MaxBotsInputValidator(),
        "invalid_message": "Input should be number.",
        "default": "4",
        "name": "bots_number"
    },
]