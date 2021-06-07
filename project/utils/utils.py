import random
from functools import reduce

from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def generate_random_adjacent_matrix(size):
    choices = [0] * 25 + [1] * 75
    return [[random.choice(choices) for x in range(size)] for y in range(size)]


def generate_visited_default_matrix(size):
    return [[False for x in range(size)] for x in range(size)]


def deep_get(dictionary, *keys):
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)


def find_key_recursively(obj, key):
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            return find_key_recursively(v, key)


def convert_letter_to_number(letter: str) -> int:
    return [ord(char) - 96 for char in letter.lower()][0] - 1


def convert_number_to_letter(number: int) -> str:
    return chr(ord('@') + number + 1)
