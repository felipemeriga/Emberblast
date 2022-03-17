from typing import Any
from .test import BaseTestCase
from emberblast.conf import get_configuration


# This is a decorator to be used in all the another tests that
# requires the configuration file data
def get_mock_conf_section(section: str) -> Any:
    def wrapper(func):
        section_result = get_configuration(section)
        setattr(func, section, section_result)
        return func

    return wrapper


class TestModuleConf(BaseTestCase):
    def test_conf(self):
        # this test is self explanatory, as the game configuration class itself, already does a lot of
        # validations on all the required files, params and environment variables, the only test to be done it's
        # to check this class gets instantiated correctly, because as a Singleton, the class has all validators inside
        # its constructor
        configuration_object = get_configuration('')
        self.assertIsNotNone(configuration_object)
