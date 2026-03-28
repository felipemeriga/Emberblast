from pathlib import Path
from typing import Dict, List, Union

from InquirerPy import prompt
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator

from emberblast.conf import get_configuration
from emberblast.interface.interface import IEquipmentItem, IItem, IPlayer, IQuestioningSystem, ISkill
from emberblast.utils import GAME_SECTION, JOBS_SECTION, LEVEL_UP_INCREMENT, RACES_SECTION


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
            {"name": "Map and Enemies \U0001f307", "value": "map"},
            {"name": "My Status \U0001f4ca", "value": "status"},
            {"name": "Single Enemy \U0001f480", "value": "enemy"},
        ]
        if show_items:
            choices.append({"name": "My Items \U0001f9ea", "value": "item"})

        choices.append({"name": "Cancel \u274c", "value": "cancel"})
        questions = [
            {
                "type": "list",
                "message": "Check: ",
                "choices": choices,
                "default": "map",
                "invalid_message": "You need to select at least one check to execute!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]
        result = prompt(questions=questions)
        return result[0]

    def ask_actions_questions(self, actions_available: List[str]) -> Union[str, bool, list, str]:
        base_actions = {
            "move": {"name": "Move \U0001f3c3", "value": "move"},
            "attack": {"name": "Attack \u2694\ufe0f", "value": "attack"},
            "skill": {"name": "Skill \U0001f525", "value": "skill"},
            "defend": {"name": "Defend \U0001f6e1\ufe0f", "value": "defend"},
            "hide": {"name": "Hide \U0001f977", "value": "hide"},
            "search": {"name": "Search \U0001f441\ufe0f", "value": "search"},
            "item": {"name": "Item \U0001f9ea", "value": "item"},
            "equip": {"name": "Equip \u2694\ufe0f", "value": "equip"},
            "drop": {"name": "Drop \u2b07\ufe0f", "value": "drop"},
            "check": {"name": "Check \U0001f440", "value": "check"},
            "pass": {"name": "Pass \U0001f44b", "value": "pass"},
        }

        authorized_actions = []
        for i in actions_available:
            authorized_actions.append(base_actions.get(i))
        actions_questions = [
            {
                "type": "list",
                "message": "Select an action:",
                "choices": authorized_actions,
                "default": "defend",
                "invalid_message": "You need to select at least one action to execute!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]
        result = prompt(questions=actions_questions)
        print("\033[A" + 100 * " " + "\033[A")  # ansi escape arrow up then overwrite the line
        return result[0]

    def ask_enemy_to_check(self, enemies: List[IPlayer]) -> Union[str, bool, list, IPlayer]:
        choices = []
        for enemy in enemies:
            choices.append(
                {"name": "{enemy} ({job})".format(enemy=enemy.name, job=enemy.job.get_name()), "value": enemy}
            )
        enemies_questions = [
            {
                "type": "list",
                "message": "Select an enemy:",
                "choices": choices,
                "invalid_message": "You need to select at least one enemy to check!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]

        result = prompt(questions=enemies_questions)
        selected_enemy = result[0]
        return selected_enemy

    def ask_enemy_to_attack(self, enemies: List[IPlayer], skill_type: str = "") -> Union[str, bool, list, IPlayer]:
        choices = []
        action_type = "attack \U0001f44a"

        if skill_type == "recover":
            action_type = "recover \U0001f49a"
        elif skill_type == "buff":
            action_type = "buff"
        elif skill_type == "debuff":
            action_type = "debuff"

        for enemy in enemies:
            choices.append(
                {
                    "name": "{enemy} ({job}) (life: {life})".format(
                        enemy=enemy.name, job=enemy.job.get_name(), life=enemy.life
                    ),
                    "value": enemy,
                }
            )
        choices.append({"name": "Cancel \u274c", "value": None})
        enemies_questions = [
            {
                "type": "list",
                "message": ("Select an enemy to {action}".format(action=action_type)),
                "choices": choices,
                "invalid_message": "You need to select at least one enemy to attack!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]
        result = prompt(questions=enemies_questions)
        selected_enemy = result[0]
        return selected_enemy

    def select_item(self, items: List[IItem]) -> Union[str, bool, list, IItem]:
        choices = []
        for item in items:
            choices.append({"name": ("{item} - {tier}".format(item=item.name, tier=item.tier)), "value": item})
        choices.append({"name": "Cancel \u274c", "value": None})
        items_questions = [
            {
                "type": "list",
                "message": "Select an item:",
                "choices": choices,
                "default": items[0],
                "invalid_message": "You need to select at least one item",
                "show_cursor": True,
                "max_height": "100",
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
            equipped_string = ""
            if player.equipment.is_equipped(equip):
                equipped_string = "  (EQUIPPED)"
            choices.append(
                {
                    "name": (
                        "{item} - {tier} {equipped_string}".format(
                            item=equip.name, tier=equip.tier, equipped_string=equipped_string
                        )
                    ),
                    "value": equip,
                }
            )
        choices.append({"name": "Cancel \u274c", "value": None})

        equipment_questions = [
            {
                "type": "list",
                "message": "Select an Equipment:",
                "choices": choices,
                "invalid_message": "You need to select at least one item",
                "show_cursor": True,
                "max_height": "100",
            }
        ]

        result = prompt(questions=equipment_questions)
        selected_equipment = result[0]
        return selected_equipment

    def ask_attributes_to_improve(self) -> Union[str, bool, list, List]:
        level_up_increment_attributes = get_configuration(LEVEL_UP_INCREMENT)
        health_points = level_up_increment_attributes.get("health_points", 5)
        magic_points = level_up_increment_attributes.get("magic_points", 5)
        move_speed = level_up_increment_attributes.get("move_speed", 1)
        strength = level_up_increment_attributes.get("strength", 3)
        intelligence = level_up_increment_attributes.get("intelligence", 3)
        accuracy = level_up_increment_attributes.get("accuracy", 1)
        armour = level_up_increment_attributes.get("armour", 3)
        magic_resist = level_up_increment_attributes.get("magic_resist", 3)
        will = level_up_increment_attributes.get("will", 3)

        level_up_questions = [
            {
                "type": "list",
                "message": "Select an action:",
                "choices": [
                    {
                        "name": f"+{health_points} Health Points \U0001f49a",
                        "value": {"attribute": "health_points", "value": health_points},
                    },
                    {
                        "name": f"+{magic_points} Magic Points \U0001f499",
                        "value": {"attribute": "magic_points", "value": magic_points},
                    },
                    {
                        "name": f"+{move_speed} Move Speed \U0001f3c3",
                        "value": {"attribute": "move_speed", "value": move_speed},
                    },
                    {
                        "name": f"+{strength} Strength \U0001f44a",
                        "value": {"attribute": "strength", "value": strength},
                    },
                    {
                        "name": f"+{intelligence} Intelligence \U0001f4da",
                        "value": {"attribute": "intelligence", "value": intelligence},
                    },
                    {
                        "name": f"+{accuracy} Accuracy \U0001f3af",
                        "value": {"attribute": "accuracy", "value": accuracy},
                    },
                    {
                        "name": f"+{armour} Armour \U0001f4a2",
                        "value": {"attribute": "armour", "value": armour},
                    },
                    {
                        "name": f"+{magic_resist} Magic Resist \U0001f300",
                        "value": {"attribute": "magic_resist", "value": magic_resist},
                    },
                    {
                        "name": f"+{will} Will \U0001f64f",
                        "value": {"attribute": "will", "value": will},
                    },
                ],
                "default": None,
                "multiselect": True,
                "validate": lambda selected: len(selected) == 2,
                "invalid_message": "You need to select 2 attributes to improve!",
                "show_cursor": True,
                "max_height": "100",
            },
        ]

        result = prompt(questions=level_up_questions)
        return result[0]

    def ask_where_to_move(self, possibilities: List[str]) -> Union[str, bool, list, str]:
        questions = [
            {
                "type": "list",
                "message": "\U0001f5fb Select where to move: ",
                "choices": possibilities,
                "invalid_message": "You need to select at least one place to move!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]
        result = prompt(questions=questions)
        return result[0]

    def perform_first_question(self) -> Union[str, bool, list, str]:
        choices = [
            {"name": "New Game \U0001f195", "value": "new"},
            {"name": "Continue \U0001f501", "value": "continue"},
        ]
        first_game_questions = [
            {
                "type": "list",
                "message": "Select an option: ",
                "choices": choices,
                "default": "new",
                "invalid_message": "You need to select at least one game type to play!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]
        result = prompt(questions=first_game_questions)
        return result[0]

    def perform_game_create_questions(self) -> Union[str, bool, list, dict]:
        begin_game_questions = [
            {
                "type": "list",
                "message": "\U0001f3ae Select the Game Type ",
                "choices": ["Deathmatch", "Clan"],
                "name": "game",
            },
            {
                "type": "list",
                "message": "\U0001f305 Select the map ",
                "choices": ["Millstone Plains", "Firebend Vulcan", "Lerwick Mountains"],
                "name": "map",
            },
            {
                "type": "input",
                "message": "\U0001f4bb How many controlled players are playing ",
                "validate": MaxPlayersValidator(),
                "invalid_message": "Input should be number.",
                "default": "1",
                "name": "controlled_players_number",
            },
            {
                "type": "input",
                "message": "\U0001f4bb How many bots are you playing against ",
                "validate": MaxBotsInputValidator(),
                "invalid_message": "Input should be number.",
                "default": "4",
                "name": "bots_number",
            },
        ]

        return prompt(begin_game_questions)

    def perform_character_creation_questions(self, existing_names: List[str]) -> Union[str, bool, list, dict]:
        questions = [
            {
                "type": "input",
                "message": "\U0001f468 Please enter your character name ",
                "validate": DuplicatedNamesValidator(existing_names),
                "invalid_message": "minimum of 1 letters, max of 20 letters",
                "name": "nickname",
            },
            {
                "type": "list",
                "message": "\U0001f480 Please enter your character race? ",
                "choices": get_configuration(RACES_SECTION).keys(),
                "name": "race",
            },
            {
                "type": "list",
                "message": "\U0001f4db Please enter your character job? ",
                "choices": get_configuration(JOBS_SECTION).keys(),
                "name": "job",
            },
        ]

        return prompt(questions)

    def get_saved_game(self, normalized_files: List[Dict]) -> Union[str, bool, list, Path]:
        choices = []

        for file_dict in normalized_files:
            option = {"name": file_dict.get("name"), "value": file_dict.get("path")}
            choices.append(option)
        choices.append({"name": "Cancel \u274c", "value": "cancel"})

        select_saved_game_questions = [
            {
                "type": "list",
                "message": "Select a game to continue: ",
                "choices": choices,
                "invalid_message": "You need to select at least one enemy to check!",
                "show_cursor": True,
                "max_height": "100",
            }
        ]
        result = prompt(questions=select_saved_game_questions)
        return result[0]

    def select_skill(self, available_skills: List[ISkill]) -> Union[str, bool, list, ISkill]:
        choices = []
        for skill in available_skills:
            area_range_string = ""
            if skill.ranged == 0:
                area_range_string = "/ melee skill"
            elif skill.ranged > 0 and skill.area == 0:
                area_range_string = "/ ranged skill with range of {range}, single target".format(range=skill.ranged)
            elif skill.ranged > 0 and skill.area > 0:
                area_range_string = "/ ranged skill with range of {range}, area damage of radius {area}".format(
                    range=skill.ranged, area=skill.area
                )
            choices.append(
                {
                    "name": (
                        "{name} / type: {kind} / cost: {cost} mana \U0001f499 {additional}".format(
                            name=skill.name, kind=skill.kind, cost=skill.cost, additional=area_range_string
                        )
                    ),
                    "value": skill,
                }
            )
        choices.append({"name": "Cancel \u274c", "value": None})
        skill_questions = [
            {
                "type": "list",
                "message": "Select a skill \U0001f525",
                "choices": choices,
                "default": available_skills[0],
                "invalid_message": "You need to select at least one skill",
                "show_cursor": True,
                "max_height": "100",
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
                        maximum=3
                    ),
                    cursor_position=document.cursor_position,
                )


class MaxBotsInputValidator(Validator):
    def validate(self, document: Document):
        """
        This function is used for validating  the number of bots inserted, when creating a new game.

        :param Document document: The document to be validated.
        :rtype: None.
        """
        max_bot_number = get_configuration(GAME_SECTION).get("max_number_bots")
        if not document.text.isnumeric():
            raise ValidationError(
                message="Input should be a number",
                cursor_position=document.cursor_position,
            )
        else:
            if int(document.text) > max_bot_number or int(document.text) <= 0:
                raise ValidationError(
                    message="The number of boots needs to be minimum 1 and maximum {maximum}".format(
                        maximum=max_bot_number
                    ),
                    cursor_position=document.cursor_position,
                )
