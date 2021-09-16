from typing import Union, List

import emojis
from InquirerPy import prompt
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

from project.conf import get_configuration
from project.utils import GAME_SECTION, RACES_SECTION, JOBS_SECTION


class DuplicatedNamesValidator(Validator):

    def __init__(self, existing_names: List[str]) -> None:
        self.existing_names = existing_names
        super().__init__()

    def validate(self, document: Document):
        if not 0 < len(document.text) < 20:
            raise ValidationError(
                message="minimum of 1 letters, max of 20 letters",
                cursor_position=document.cursor_position,
            )
        for name in self.existing_names:
            if document.text == name:
                raise ValidationError(
                    message="There is already a player with name: {name}".format(name=name),
                    cursor_position=document.cursor_position,
                )


class MaxPlayersValidator(Validator):
    def validate(self, document: Document):
        """
        This function is used for validating  the number of bots inserted, when creating a new game.

        :param Document document: The document to be validated.
        :rtype: None.
        """
        if not document.text.isnumeric():
            raise ValidationError(
                message="Input should be a number",
                cursor_position=document.cursor_position,
            )
        else:
            if int(document.text) > 3 or int(document.text) <= 0:
                raise ValidationError(
                    message="The number of controlled players needs to be minimum 1 and maximum {maximum}".format(
                        maximum=3),
                    cursor_position=document.cursor_position,
                )


class MaxBotsInputValidator(Validator):
    def validate(self, document: Document):
        """
        This function is used for validating  the number of bots inserted, when creating a new game.

        :param Document document: The document to be validated.
        :rtype: None.
        """
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
        "message": emojis.encode(':computer: How many controlled players are playing '),
        "validate": MaxPlayersValidator(),
        "invalid_message": "Input should be number.",
        "default": "1",
        "name": "controlled_players_number"
    },
    {
        "type": "input",
        "message": emojis.encode(':computer: How many bots are you playing against '),
        "validate": MaxBotsInputValidator(),
        "invalid_message": "Input should be number.",
        "default": "4",
        "name": "bots_number"
    }
]


def perform_first_question() -> Union[str, bool, list, str]:
    """
    This function is used by asking if the player wants to continue or start a new game.

    :rtype: Union[str, bool, list, str].
    """
    choices = [
        {
            'name': emojis.encode('New Game :new:'),
            'value': 'new'
        }, {
            'name': emojis.encode('Continue :repeat:'),
            'value': 'continue'
        }
    ]
    first_game_questions = [
        {
            'type': 'list',
            'message': 'Select an option: ',
            'choices': choices,
            'default': 'new',
            'invalid_message': 'You need to select at least one game type to play!',
            'show_cursor': True,
            'max_height': '100'
        }
    ]
    result = prompt(questions=first_game_questions)
    return result[0]


def perform_game_create_questions() -> Union[str, bool, list, dict]:
    """
    This function is used by asking a new game questions.

    :rtype: Union[str, bool, list, dict].
    """
    return prompt(BEGIN_GAME_QUESTIONS)


def perform_character_creation_questions(existing_names: List[str]) -> Union[str, bool, list, dict]:
    """
    This function is used when creating a new character.

    :rtype: Union[str, bool, list, dict].
    """
    questions = [
        {
            "type": "input",
            "message": emojis.encode(':man: Please enter your character name '),
            "validate": DuplicatedNamesValidator(existing_names),
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

    return prompt(questions)
