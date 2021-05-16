from random import randrange


def line_appender(file_path, target):
    file = open(file_path, "r")
    splitfile = file.read().splitlines()
    for line in splitfile:
        target.append(line)


def name_selector(target_list):
    selected = target_list[randrange(len(target_list))]
    return selected


def name_builder(first_name_list_path):
    first_name_list = []
    last_name_list = []
    last_name_list_path = 'last_name.txt'

    line_appender(first_name_list_path, first_name_list)
    line_appender(last_name_list_path, last_name_list)

    first_name_selected = name_selector(first_name_list)
    last_name_selected = name_selector(last_name_list)

    name = first_name_selected + " " + last_name_selected
    return name


def generate_name(gender):
    first_name_list_path = ''
    if gender == 'Female':
        first_name_list_path = 'first_name_female.txt'
    else:
        first_name_list_path = 'first_name_male.txt'
    return name_builder(first_name_list_path)

