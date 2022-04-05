from pathlib import Path
from typing import List, Union, Dict

from InquirerPy import prompt
from emojis import emojis
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

from emberblast.conf import get_configuration
from emberblast.interface.interface import IQuestioningSystem, IPlayer, IEquipmentItem, IItem, ISkill
from emberblast.utils import LEVEL_UP_INCREMENT, GAME_SECTION, JOBS_SECTION, RACES_SECTION


class QuestionerCMD(IQuestioningSystem):

    def __init__(self) -> None:
        super().__init__()

    def ask_check_action(self, show_items: bool = False) -> Union[str, bool, list, str]:
        """
        Ask which kind of information player wants to check.

        :param bool show_items: If the player doesn't have items on its bag, this flag will help the
        communicator to remove the items question.
        :rtype: Union[str, bool, list, str].
        """
        choices = [
            {
                'name': emojis.encode('Map and Enemies :city_sunset: '),
                'value': 'map'
            },
            {
                'name': emojis.encode('My Status: :bar_chart: '),
                'value': 'status'
            },
            {
                'name': emojis.encode('Single Enemy: :skull: '),
                'value': 'enemy'
            }
        ]
        if show_items:
            choices.append({
                'name': emojis.encode('My Items: :test_tube: '),
                'value': 'item'
            })

        choices.append({
            'name': emojis.encode('Cancel: :x: '),
            'value': 'cancel'
        })
        questions = [
            {
                'type': 'list',
                'message': 'Check: ',
                'choices': choices,
                'default': 'map',
                'invalid_message': 'You need to select at least one check to execute!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=questions)
        return result[0]

    def ask_actions_questions(self, actions_available: List[str]) -> Union[str, bool, list, str]:
        base_actions = {
            'move': {
                'name': emojis.encode('Move: :runner:'),
                'value': 'move'
            },
            'attack': {
                'name': emojis.encode('Attack: :crossed_swords:'),
                'value': 'attack'
            },
            'skill': {
                'name': emojis.encode('Skill: :fire:'),
                'value': 'skill'
            },
            'defend': {
                'name': emojis.encode('Defend: :shield:'),
                'value': 'defend'
            },
            'hide': {
                'name': emojis.encode('Hide: :ninja:'),
                'value': 'hide'
            },
            'search': {
                'name': emojis.encode('Search: :eye:'),
                'value': 'search'
            },
            'item': {
                'name': emojis.encode('Item: :test_tube:'),
                'value': 'item'
            },
            'equip': {
                'name': emojis.encode('Equip: :crossed_swords:'),
                'value': 'equip'
            },
            'drop': {
                'name': emojis.encode('Drop: :arrow_down:'),
                'value': 'drop'
            },
            'check': {
                'name': emojis.encode('Check: :eyes:'),
                'value': 'check'
            },
            'pass': {
                'name': emojis.encode('Pass: :wave:'),
                'value': 'pass'
            },
        }

        authorized_actions = []
        for i in actions_available:
            authorized_actions.append(base_actions.get(i))
        actions_questions = [
            {
                'type': 'list',
                'message': 'Select an action:',
                'choices': authorized_actions,
                'default': 'defend',
                'invalid_message': 'You need to select at least one action to execute!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=actions_questions)
        print("\033[A" + 100 * " " + "\033[A")  # ansi escape arrow up then overwrite the line
        return result[0]

    def ask_enemy_to_check(self, enemies: List[IPlayer]) -> Union[str, bool, list, IPlayer]:
        choices = []
        for enemy in enemies:
            choices.append({
                'name': '{enemy} ({job})'.format(enemy=enemy.name,
                                                 job=enemy.job.get_name()),
                'value': enemy
            })
        enemies_questions = [
            {
                'type': 'list',
                'message': 'Select an enemy:',
                'choices': choices,
                'invalid_message': 'You need to select at least one enemy to check!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]

        result = prompt(questions=enemies_questions)
        selected_enemy = result[0]
        return selected_enemy

    def ask_enemy_to_attack(self, enemies: List[IPlayer], skill_type: str = '') -> Union[str, bool, list, IPlayer]:
        choices = []
        action_type = 'attack: :punch:'

        if skill_type == 'recover':
            action_type = 'recover: :green_heart:'
        elif skill_type == 'buff':
            action_type = 'buff:'
        elif skill_type == 'debuff':
            action_type = 'debuff:'

        for enemy in enemies:
            choices.append({
                'name': '{enemy} ({job}) (life: {life})'.format(enemy=enemy.name,
                                                                job=enemy.job.get_name(),
                                                                life=enemy.life),
                'value': enemy
            })
        choices.append({
            'name': emojis.encode('Cancel :x: '),
            'value': None
        })
        enemies_questions = [
            {
                'type': 'list',
                'message': emojis.encode('Select an enemy to {action}'.format(action=action_type)),
                'choices': choices,
                'invalid_message': 'You need to select at least one enemy to attack!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=enemies_questions)
        selected_enemy = result[0]
        return selected_enemy

    def select_item(self, items: List[IItem]) -> Union[str, bool, list, IItem]:
        choices = []
        for item in items:
            choices.append({
                'name': emojis.encode('{item} - {tier}'.format(item=item.name,
                                                               tier=item.tier)),
                'value': item
            })
        choices.append({
            'name': emojis.encode('Cancel :x: '),
            'value': None
        })
        items_questions = [
            {
                'type': 'list',
                'message': 'Select an item:',
                'choices': choices,
                'default': items[0],
                'invalid_message': 'You need to select at least one item',
                'show_cursor': True,
                'max_height': '100'
            }
        ]

        result = prompt(questions=items_questions)
        selected_item = result[0]
        return selected_item

    def confirm_item_selection(self) -> Union[str, bool, list, bool]:
        questions = [
            {"type": "confirm", "message": "Are you sure?", "name": "confirm", "default": False},
        ]
        result = prompt(questions)
        confirm = result["confirm"]
        return confirm

    def confirm_use_item_on_you(self) -> Union[str, bool, list, bool]:
        questions = [
            {"type": "confirm", "message": "Are you using the item on yourself?", "name": "confirm", "default": False},
        ]
        result = prompt(questions)
        confirm = result["confirm"]
        return confirm

    def display_equipment_choices(self, player: IPlayer) -> Union[str, bool, list, IEquipmentItem]:
        equipments = player.bag.get_equipments()
        choices = []

        for equip in equipments:
            equipped_string = ''
            if player.equipment.is_equipped(equip):
                equipped_string = '  (EQUIPPED)'
            choices.append({
                'name': emojis.encode('{item} - {tier} {equipped_string}'.format(item=equip.name,
                                                                                 tier=equip.tier,
                                                                                 equipped_string=equipped_string)),
                'value': equip
            })
        choices.append({
            'name': emojis.encode('Cancel :x: '),
            'value': None
        })

        equipment_questions = [
            {
                'type': 'list',
                'message': 'Select an Equipment:',
                'choices': choices,
                'invalid_message': 'You need to select at least one item',
                'show_cursor': True,
                'max_height': '100'
            }
        ]

        result = prompt(questions=equipment_questions)
        selected_equipment = result[0]
        return selected_equipment

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

    def ask_where_to_move(self, possibilities: List[str]) -> Union[str, bool, list, str]:
        questions = [
            {
                'type': 'list',
                'message': emojis.encode(':mount_fuji: Select where to move: '),
                'choices': possibilities,
                'invalid_message': 'You need to select at least one place to move!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=questions)
        return result[0]

    def perform_first_question(self) -> Union[str, bool, list, str]:
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

    def perform_game_create_questions(self) -> Union[str, bool, list, dict]:
        begin_game_questions = [
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

        return prompt(begin_game_questions)

    def perform_character_creation_questions(self, existing_names: List[str]) -> Union[str, bool, list, dict]:
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

    def get_saved_game(self, normalized_files: List[Dict]) -> Union[str, bool, list, Path]:
        choices = []

        for file_dict in normalized_files:
            option = {
                'name': file_dict.get('name'),
                'value': file_dict.get('path')
            }
            choices.append(option)
        choices.append({
            'name': emojis.encode('Cancel :x:'),
            'value': 'cancel'
        })

        select_saved_game_questions = [
            {
                'type': 'list',
                'message': 'Select a game to continue: ',
                'choices': choices,
                'invalid_message': 'You need to select at least one enemy to check!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=select_saved_game_questions)
        return result[0]

    def select_skill(self, available_skills: List[ISkill]) -> Union[str, bool, list, ISkill]:
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
