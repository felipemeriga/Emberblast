from random import randrange

from ..utils import get_project_root

NAME_GENERATOR_PATH = '{root}/utils/name_generator'.format(root=get_project_root())


def generate_name() -> str:
    """
    This functions works based in two files, the first_name.txt and second_name.txt.
    Each of those files, contains thousands of names, and a first and last name will be randomly
    picked to form a random generated name.

    :rtype: str
    """
    try:
        with open(NAME_GENERATOR_PATH + '/first_name.txt') as names_file:
            names = names_file.read().splitlines()
            with open(NAME_GENERATOR_PATH + '/last_name.txt') as last_names_files:
                last_names = last_names_files.read().splitlines()
                return '{first_name} {last_name}'.format(first_name=names[randrange(len(names))],
                                                         last_name=last_names[randrange(len(last_names))])
    except OSError as err:
        return ''
