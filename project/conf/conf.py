import yaml
from yaml.scanner import ScannerError
from cerberus import Validator, SchemaError

from project.conf.schema import race_section_configuration_schema, game_section_configuration_schema, \
    job_section_configuration_schema, level_up_attributes_configuration_schema
from project.conf.logger import get_logger
from project.exception.exception import ConfigFileError
from project.utils.constants import GAME_SECTION, JOBS_SECTION, RACES_SECTION, LEVEL_UP_INCREMENT
from project.utils.utils import get_project_root, deep_get


class Configuration(object):
    def __init__(self, arg):
        self._arg = arg
        self._logger = get_logger()
        self.project_module = __import__('project')
        self.parsed_yaml_file = {}
        self.game = {}
        self.jobs = {}
        self.races = {}
        self.level_up_attributes_increment = {}
        self.custom_jobs = {}
        self.custom_races = {}
        try:
            a_yaml_file = open(str(get_project_root()) + '/conf/conf.yaml')
            self.parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
            self.validate_config_file()
        except OSError as err:
            self._logger.error(err)
            raise SystemExit('Could not open the game configuration file')
        except ScannerError as err:
            self._logger.error(err)
            raise SystemExit('Could not parse the configuration file')

    def __call__(self, section):
        return self.__getattribute__(section)

    def validate_config_file(self):
        try:
            self.validate_game_config()
            self.validate_jobs_attributes()
            self.validate_races_attributes()
            self.validate_level_up_increment_attributes()
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


@Configuration
def get_configuration():
    pass
