import yaml
from yaml.scanner import ScannerError
from cerberus import Validator, SchemaError

from .schema import race_section_configuration_schema, game_section_configuration_schema, \
    job_section_configuration_schema, level_up_attributes_configuration_schema, side_effects_configuration_schema, \
    healing_item_validation_schema, recovery_item_validation_schema, equipment_item_validation_schema, \
    items_probabilities_schema
from .logger import get_logger
from project.utils import GAME_SECTION, JOBS_SECTION, RACES_SECTION, LEVEL_UP_INCREMENT, SIDE_EFFECTS_SECTION, \
    ITEMS_SECTION, ITEMS_PROBABILITIES_SECTION
from project.utils import get_project_root, deep_get
from project.exception import ConfigFileError


class Configuration(object):
    def __init__(self, arg):
        self._arg = arg
        self._logger = get_logger()
        self.project_module = __import__('project')
        self.parsed_yaml_file = {}
        self.parsed_items_file = {}
        self.parsed_side_effects_file = {}
        self.game = {}
        self.jobs = {}
        self.races = {}
        self.level_up_attributes_increment = {}
        self.side_effects = {}
        self.items = {}
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
        return self.__getattribute__(section)

    def parse_configuration_files(self):
        config_yaml_file = open(str(get_project_root()) + '/conf/conf.yaml')
        self.parsed_yaml_file = yaml.load(config_yaml_file, Loader=yaml.FullLoader)
        self.validate_config_file()

        side_effects_yaml_file = open(str(get_project_root()) + '/conf/side_effects.yaml')
        self.parsed_side_effects_file = yaml.load(side_effects_yaml_file, Loader=yaml.FullLoader)
        self.validate_side_effects()

        items_yaml_file = open(str(get_project_root()) + '/conf/items.yaml')
        self.parsed_items_file = yaml.load(items_yaml_file, Loader=yaml.FullLoader)
        self.validate_items()

    def validate_config_file(self):
        try:
            self.validate_game_config()
            self.validate_jobs_attributes()
            self.validate_races_attributes()
            self.validate_level_up_increment_attributes()
            self.validate_items_probabilities_attributes()
        except ConfigFileError as err:
            raise SystemExit(str(err))
        except SchemaError as err:
            raise SystemExit(str(err))

    def validate_items(self):
        try:
            self.items = self.parsed_items_file.get(ITEMS_SECTION, {})
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

                if 'side-effects' in list(value.keys()):
                    for element in value.get('side-effects', []):
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

    def error_handler(self, errors=None, section=''):
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

    def validate_game_config(self):
        self.game = self.parsed_yaml_file.get(GAME_SECTION, {})
        v = Validator(game_section_configuration_schema)
        if not v.validate(self.game, game_section_configuration_schema):
            self.error_handler(v.errors, GAME_SECTION)

    def validate_jobs_attributes(self):
        self.jobs = deep_get(self.game, JOBS_SECTION)
        v = Validator(job_section_configuration_schema)
        for key, value in self.jobs.items():
            if not v.validate(value, job_section_configuration_schema):
                self.error_handler(v.errors, key)

    def validate_races_attributes(self):
        self.races = deep_get(self.game, RACES_SECTION)
        v = Validator(race_section_configuration_schema)
        for key, value in self.races.items():
            if not v.validate(value, race_section_configuration_schema):
                self.error_handler(v.errors, key)

    def validate_level_up_increment_attributes(self):
        self.level_up_attributes_increment = deep_get(self.game, LEVEL_UP_INCREMENT)
        v = Validator(level_up_attributes_configuration_schema)
        if not v.validate(self.level_up_attributes_increment, level_up_attributes_configuration_schema):
            self.error_handler(v.errors, LEVEL_UP_INCREMENT)

    def validate_side_effects(self):
        self.side_effects = self.parsed_side_effects_file.get(SIDE_EFFECTS_SECTION, {})
        v = Validator(side_effects_configuration_schema)
        for key, value in self.side_effects.items():
            if not v.validate(value, side_effects_configuration_schema):
                self.error_handler(v.errors, key)

    def validate_items_probabilities_attributes(self):
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
