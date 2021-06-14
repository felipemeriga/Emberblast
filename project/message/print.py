from typing import List

import timg
from colorama import Fore
from emojis import emojis
from termcolor import colored

from project.utils import get_project_root, convert_number_to_letter


def print_greetings():
    obj = timg.Renderer()
    project_path = get_project_root()
    obj.load_image_from_file(str(project_path) + '/img/emberblast.png')
    obj.resize(100, 100)
    obj.render(timg.ASCIIMethod)
    print(Fore.RED + emojis.encode(':fire: Welcome to Emberblast! :fire: \n\n'))


def print_player_stats(player):
    print(emojis.encode(
        ':man: {name} Stats: \n\n'.format(name=player.name)))
    print(emojis.encode(
        ':bar_chart: Level: {level} \n'
        ':green_heart: Health Points: {health} \n'
        ':blue_heart: Magic Points: {magic} \n'
        ':runner: Move Speed: {move} \n'
        ':books: Intelligence: {intelligence} \n'
        ':dart: Accuracy: {accuracy} \n'
        ':punch: Strength: {attack} \n'
        ':shield: Armour: {armour} \n'
        ':cyclone: Magic Resist: {resist} \n'
        ':pray: Will: {will} \n'.format(level=player.level,
                                        health=player.health_points,
                                        magic=player.magic_points,
                                        move=player.move_speed,
                                        intelligence=player.intelligence,
                                        accuracy=player.accuracy,
                                        attack=player.strength,
                                        armour=player.armour,
                                        resist=player.magic_resist,
                                        will=player.will)))


def print_enemy_status(enemy) -> None:
    print(emojis.encode(colored('Enemy {name}({job}) is currently at position: {position} \n'
                                ':bar_chart: Level: {level} \n'
                                ':green_heart: Health Points: {health} \n'
                                ':blue_heart: Magic Points: {magic} \n'
                                ':runner: Move Speed: {move} \n'
                                ':books: Intelligence: {intelligence} \n'
                                ':dart: Accuracy: {accuracy} \n'
                                ':punch: Strength: {attack} \n'
                                ':shield: Armour: {armour} \n'
                                ':cyclone: Magic Resist: {resist} \n'
                                ':pray: Will: {will} \n'.format(name=enemy.name,
                                                                job=enemy.job.get_name(),
                                                                position=enemy.position,
                                                                level=enemy.level,
                                                                health=enemy.health_points,
                                                                magic=enemy.magic_points,
                                                                move=enemy.move_speed,
                                                                intelligence=enemy.intelligence,
                                                                accuracy=enemy.accuracy,
                                                                attack=enemy.strength,
                                                                armour=enemy.armour,
                                                                resist=enemy.magic_resist,
                                                                will=enemy.will
                                                                ),
                                'red')))


def print_plain_matrix(matrix) -> None:
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in matrix]))


def print_plain_map(matrix, size) -> None:
    # Print the columns first
    print(' ' * 4, end="")
    for column in range(size):
        print('{:4}'.format(column), end="")
    print('\n')
    for row in range(size):
        print('{:7}'.format(convert_number_to_letter(row)), end="")
        for column in range(size):
            print('{:4}'.format('*' if matrix[row][column] == 1 else ' '), end="")
        print('')


def print_map_info(player, players, size, matrix) -> None:
    foes_positions = []
    print(colored('{name} is currently at position: {position}, '
                  'with {health_points} HP'.format(name=player.name,
                                                   position=player.position,
                                                   health_points=player.health_points),
                  'green'))

    for opponent in players:
        foes_positions.append(opponent.position)
        print(colored('Enemy {name}({job}) is currently at position: {position}, '
                      'with {health_points} HP'.format(name=opponent.name,
                                                       job=opponent.job.get_name(),
                                                       position=opponent.position,
                                                       health_points=opponent.health_points),
                      'red'))

    print(' ' * 4, end="")
    for column in range(size):
        print('{:4}'.format(column), end="")
    print('\n')
    for row in range(size):
        print('{:7}'.format(convert_number_to_letter(row)), end="")
        for column in range(size):
            color = 'white'
            attrs = ['bold']
            position = convert_number_to_letter(row) + str(column)

            if player.position == position:
                color = 'green'
                attrs.append('blink')
            elif position in foes_positions:
                color = 'red'
            print(colored('{:4}'.format('*' if matrix[row][column] == 1 else ' '), color, attrs=attrs), end="")
        print('')


def print_moving_possibilities(player_position: str, possibilities: List[str], matrix: List[List[int]],
                               size: int) -> None:
    print('Possibilities of Moving')
    print(colored('You are on the Yellow tile', 'yellow'))
    print(colored('Green tiles are the possibilities', 'green'))
    print(' ' * 4, end="")
    for column in range(size):
        print('{:4}'.format(column), end="")
    print('\n')
    for row in range(size):
        print('{:7}'.format(convert_number_to_letter(row)), end="")
        for column in range(size):
            color = 'white'
            attrs = ['bold']
            position = convert_number_to_letter(row) + str(column)

            if position in possibilities:
                color = 'green'
                attrs.append('blink')
            elif player_position == position:
                color = 'yellow'
                attrs.append('blink')
            print(colored('{:4}'.format('*' if matrix[row][column] == 1 else ' '), color, attrs=attrs), end="")
        print('')
