from random import randrange

from project.utils.utils import get_project_root

NAME_GENERATOR_PATH = '{root}/utils/name_generator'.format(root=get_project_root())


def generate_name():
    try:
        with open(NAME_GENERATOR_PATH + '/first_namasde.txt') as names_file:
            names = names_file.read().splitlines()
            with open(NAME_GENERATOR_PATH + '/last_name.txt') as last_names_files:
                last_names = last_names_files.read().splitlines()
                return '{first_name} {last_name}'.format(first_name=names[randrange(len(names))],
                                                         last_name=last_names[randrange(len(last_names))])
    except OSError as err:
        return ''
