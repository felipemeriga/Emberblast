import random


def generate_random_adjacent_matrix(size):
    return [[random.randint(0, 1) for x in range(size)] for y in range(size)]


def generate_visited_default_matrix(size):
    return [[False for x in range(size)] for x in range(size)]
