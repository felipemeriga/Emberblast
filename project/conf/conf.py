import yaml

from project.utils.utils import get_project_root


class Configuration(object):
    def __init__(self, arg):
        self._arg = arg
        a_yaml_file = open(str(get_project_root()) + '/conf/conf.yaml')
        parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
        self.jobs = parsed_yaml_file.get('jobs', {})

    def __call__(self, section):
        return self.__getattribute__(section)


@Configuration
def get_configuration():
    pass
