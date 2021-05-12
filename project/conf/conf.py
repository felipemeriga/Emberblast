import yaml
from yaml.scanner import ScannerError
from cerberus import Validator

from project.conf.logger import get_logger
from project.utils.utils import get_project_root


class Configuration(object):
    def __init__(self, arg):
        self._arg = arg
        self._logger = get_logger()
        try:
            a_yaml_file = open(str(get_project_root()) + '/conf/conf.yaml')
            parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
            self.jobs = parsed_yaml_file.get('jobs', {})
            self.validate_conf_file(parsed_yaml_file)
        except OSError as err:
            self._logger.error(err)
            raise SystemExit('Could not open the game configuration file')
        except ScannerError as err:
            self._logger.error(err)
            raise SystemExit('Could not parse the configuration file')

    def __call__(self, section):
        return self.__getattribute__(section)

    def validate_conf_file(self, parsed_yaml_file):
        try:
            schema = eval(open(str(get_project_root()) + '/conf/schema.py', 'r').read())
            v = Validator(schema)
            if not v.validate(parsed_yaml_file, schema):
                # Finish this part
                for error in v.errors:
                    self._logger.error('Your config yaml file, do not have the ' + error + ' section')
                raise SystemExit('Your file is not formatted like the schema')
            print(v.errors)
        except OSError as err:
            self._logger.error(err)
            raise SystemExit('Could not open the schema validator file')


@Configuration
def get_configuration():
    pass
