import yaml
from yaml.scanner import ScannerError
from cerberus import Validator, SchemaError

from project.conf.constants import JOBS_SECTION, GAME_SECTION
from project.conf.logger import get_logger
from project.conf.schema import job_section_configuration_schema, game_section_configuration_schema
from project.exception.exception import ConfigFileError
from project.utils.utils import get_project_root


class Configuration(object):
    def __init__(self, arg):
        self._arg = arg
        self._logger = get_logger()
        self.parsed_yaml_file = {}
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
        v = Validator(game_section_configuration_schema)
        if not v.validate(self.parsed_yaml_file.get(GAME_SECTION, {}), game_section_configuration_schema):
            self.error_handler(v.errors, GAME_SECTION)

    def validate_jobs_attributes(self):
        jobs = self.parsed_yaml_file.get(JOBS_SECTION)
        v = Validator(job_section_configuration_schema)
        for job in jobs:
            if not v.validate(job, job_section_configuration_schema):
                self.error_handler(v.errors)


@Configuration
def get_configuration():
    pass
