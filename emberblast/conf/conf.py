import yaml
from yaml.scanner import ScannerError
from cerberus import Validator, SchemaError

from .schema import race_section_configuration_schema, game_section_configuration_schema, \
    job_section_configuration_schema, level_up_attributes_configuration_schema, side_effects_configuration_schema, \
    healing_item_validation_schema, recovery_item_validation_schema, equipment_item_validation_schema, \
    items_probabilities_schema, skills_validation_schema, experience_earned_action_configuration_schema
from .logger import get_logger
from emberblast.utils import GAME_SECTION, JOBS_SECTION, RACES_SECTION, LEVEL_UP_INCREMENT, SIDE_EFFECTS_SECTION, \
    ITEMS_SECTION, ITEMS_PROBABILITIES_SECTION, SKILLS_SECTION
from emberblast.utils import get_project_root, deep_get
from emberblast.exception import ConfigFileError
from ..utils.constants import EXPERIENCE_EARNED_ACTION


class Configuration(object):
    def __init__(self, arg) -> None:
        """
        Base constructor of this class, that will be used as a decorator, to create a Singleton entity.
        So, all another classes at runtime, can access this same instantiated object.

        :param arg: General arguments
        :rtype: None
        """
        self._arg = arg
        self._logger = get_logger()
        self.project_module = __import__('emberblast')
        self.parsed_yaml_file = {}
        self.game = {}
        self.jobs = {}
        self.races = {}
        self.level_up_attributes_increment = {}
        self.experience_earned_action = {}
        self.side_effects = {}
        self.items = {}
        self.skills = {}
        self.custom_jobs = {}
        self.custom_races = {}
        self.item_probabilities = {}
        try:
            self.parse_configuration_files()
        except OSError as err:
            self._logger.error(err)
            raise SystemExit('Could not open the game configuration file')
        except ScannerError as err:
            self._logger.error(err)
            raise SystemExit('Could not parse the configuration file')

    def __call__(self, section):
        if section == '':
            return self
        return self.__getattribute__(section)

    def parse_configuration_files(self) -> None:
        """
        Get's the configuration files from the repo, or another location,
        parses and validates them, to make sure everything is fine before starting the game.

        In the case there is an error that may further affect the execution of the game, it
        will panic.

        There are many yaml configuration files, the conf.yaml, items.yaml, side_effects.yaml and
        skill.yaml. In schema.py file there is all the patterns of how each of the sections of those configuration
        files may look like, and the types of each field.

        :rtype: None
        """
        project_root = str(get_project_root())
        config_yaml_file = open(str(get_project_root()) + '/conf/conf.yaml')
        self.parsed_yaml_file = yaml.load(config_yaml_file, Loader=yaml.FullLoader)
        self.validate_config_file()

        side_effects_yaml_file = open(str(get_project_root()) + '/conf/side_effects.yaml')
        self.side_effects = yaml.load(side_effects_yaml_file, Loader=yaml.FullLoader)
        self.validate_side_effects()

        items_yaml_file = open(str(get_project_root()) + '/conf/items.yaml')
        self.items = yaml.load(items_yaml_file, Loader=yaml.FullLoader)
        self.validate_items()

        skills_yaml_file = open(str(get_project_root()) + '/conf/skills.yaml')
        self.skills = yaml.load(skills_yaml_file, Loader=yaml.FullLoader)
        self.validate_skills()

    def validate_config_file(self) -> None:
        """
        There are many yaml configuration files, the conf.yaml, items.yaml, side_effects.yaml and
        skill.yaml. They are separated to keep things organized, this method focus on conf.yaml, which
        has all the declarative configuration of the game.

        :rtype: None
        """
        try:
            self.validate_game_config()
            self.validate_jobs_attributes()
            self.validate_races_attributes()
            self.validate_level_up_increment_attributes()
            self.validate_items_probabilities_attributes()
            self.validate_experience_earned_action()
        except ConfigFileError as err:
            raise SystemExit(str(err))
        except SchemaError as err:
            raise SystemExit(str(err))

    def validate_items(self) -> None:
        """
        Validate all the items from items.yaml, to make sure all of them have been defined properly.

        :rtype: None
        """
        try:
            validated_items = {}
            healing_validator = Validator(healing_item_validation_schema)
            recovery_validator = Validator(recovery_item_validation_schema)
            equipment_validator = Validator(equipment_item_validation_schema)

            for key, value in self.items.items():
                validator = None
                schema = None
                if value.get('type') == 'healing':
                    validator = healing_validator
                    schema = healing_item_validation_schema
                elif value.get('type') == 'recovery':
                    validator = recovery_validator
                    schema = recovery_item_validation_schema
                elif value.get('type') == 'equipment':
                    validator = equipment_validator
                    schema = equipment_item_validation_schema
                else:
                    self._logger.warn(
                        'Item: {item} of unknown type, valid ones are healing, equipment and recovery'.format(item=key))
                    continue

                if not validator.validate(value, schema):
                    self.error_handler(validator.errors, key)

                if 'side_effects' in list(value.keys()):
                    for element in value.get('side_effects', []):
                        if element not in self.side_effects.keys():
                            self._logger.warn(
                                'Item: {item} has an unknown side effect attached to that'.format(item=key))
                            continue
                if 'status' in list(value.keys()):
                    if value.get('status') not in self.side_effects.keys():
                        self._logger.warn(
                            'Item: {item} has an unknown side effect attached to that'.format(item=key))
                        continue
                validated_items[key] = value
        except ConfigFileError as err:
            raise SystemExit(str(err))
        except SchemaError as err:
            raise SystemExit(str(err))

    def error_handler(self, errors=None, section: str = '') -> None:
        """
        General error handler, to format the error message, when a field in the configuration file it's wrong.

        :param errors: The errors to be analysed.
        :param section: The section that contains an error.
        :rtype: None
        """
        if errors is None:
            errors = {}

        formatted_error_string = "There is an error in the configuration file section -> {section}: \n".format(
            section=section)

        for error in errors:
            formatted_error_string = "{string} \n field: {field}, issue: {issue}".format(
                string=formatted_error_string,
                field=error,
                issue=errors[error])

        self._logger.error(formatted_error_string)
        raise ConfigFileError(formatted_error_string)

    def validate_game_config(self) -> None:
        """
        Validates the game section from conf.yaml.

        :rtype: None
        """
        self.game = self.parsed_yaml_file.get(GAME_SECTION, {})
        v = Validator(game_section_configuration_schema)
        if not v.validate(self.game, game_section_configuration_schema):
            self.error_handler(v.errors, GAME_SECTION)

    def validate_jobs_attributes(self):
        """
        Validates the jobs attributes from conf.yaml.

        :rtype: None
        """
        self.jobs = deep_get(self.game, JOBS_SECTION)
        v = Validator(job_section_configuration_schema)
        for key, value in self.jobs.items():
            if not v.validate(value, job_section_configuration_schema):
                self.error_handler(v.errors, key)

    def validate_races_attributes(self):
        """
        Validates the races attributes from conf.yaml.

        :rtype: None
        """
        self.races = deep_get(self.game, RACES_SECTION)
        v = Validator(race_section_configuration_schema)
        for key, value in self.races.items():
            if not v.validate(value, race_section_configuration_schema):
                self.error_handler(v.errors, key)

    def validate_level_up_increment_attributes(self):
        """
        Validates the level up increment attributes from conf.yaml.

        :rtype: None
        """
        self.level_up_attributes_increment = deep_get(self.game, LEVEL_UP_INCREMENT)
        v = Validator(level_up_attributes_configuration_schema)
        if not v.validate(self.level_up_attributes_increment, level_up_attributes_configuration_schema):
            self.error_handler(v.errors, LEVEL_UP_INCREMENT)

    def validate_experience_earned_action(self):
        """
        Validates the experience earned in each action

        :rtype: None
        """
        self.experience_earned_action = deep_get(self.game, EXPERIENCE_EARNED_ACTION)
        v = Validator(experience_earned_action_configuration_schema)
        if not v.validate(self.experience_earned_action, experience_earned_action_configuration_schema):
            self.error_handler(v.errors, EXPERIENCE_EARNED_ACTION)

    def validate_side_effects(self) -> None:
        """
        Validates side_effects.yaml file.

        :rtype: None
        """
        v = Validator(side_effects_configuration_schema)
        for key, value in self.side_effects.items():
            if not v.validate(value, side_effects_configuration_schema):
                self.error_handler(v.errors, key)

    def validate_skills(self) -> None:
        """
        Validates skill.yaml file.

        :rtype: None
        """
        v = Validator(skills_validation_schema)

        for key, value in self.skills.items():

            if not v.validate(value, skills_validation_schema):
                self.error_handler(v.errors, key)

            normalized_skill = v.normalized(value)

            if not normalized_skill.get('job', None) in self.jobs:
                error_string = 'The skill {skill} has an unknown job assigned to it.'.format(skill=normalized_skill.get('name'))
                self._logger.error(error_string)
                raise ConfigFileError(error_string)
            if 'side_effects' in list(normalized_skill.keys()):
                for element in normalized_skill.get('side_effects', []):
                    if element not in self.side_effects.keys():
                        error_string = 'The skill {skill} has an unknown side-effect assigned to it.'.format(
                            skill=normalized_skill.get('name'))
                        self._logger.error(error_string)
                        raise ConfigFileError(error_string)
            self.skills[key] = normalized_skill

    def validate_items_probabilities_attributes(self) -> None:
        """
        Validates items probabilities section from conf.yaml.

        :rtype: None
        """
        self.item_probabilities = deep_get(self.game, ITEMS_PROBABILITIES_SECTION)
        v = Validator(items_probabilities_schema)
        if not v.validate(self.item_probabilities, items_probabilities_schema):
            self.error_handler(v.errors, ITEMS_PROBABILITIES_SECTION)
        sum_of_probabilities = sum([x for x in self.item_probabilities.values()])
        if sum_of_probabilities != 1:
            raise ConfigFileError(
                'The sum of all the probabilities of the items_probabilities must be 1, which is 100%')


@Configuration
def get_configuration():
    pass
