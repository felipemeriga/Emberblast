from typing import List

import timg
from emojis import emojis
from termcolor import colored

from project.item import Item, EquipmentItem, RecoveryItem, HealingItem
from project.player import Player
from project.utils import get_project_root, convert_number_to_letter


def print_greetings() -> None:
    """
    Print game greetings.

    :rtype: None
    """
    obj = timg.Renderer()
    project_path = get_project_root()
    obj.load_image_from_file(str(project_path) + '/img/emberblast.png')
    obj.resize(100, 100)
    obj.render(timg.ASCIIMethod)
    print(emojis.encode(colored(':fire: Welcome to Emberblast! :fire: \n\n', 'red')))


def print_player_stats(player: Player):
    """
    Print the current playing player stats and attributes.

    :param Player player: The current player.
    :rtype: None
    """
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


def print_enemy_status(enemy: Player) -> None:
    """
    Print the current status and attributes of a unhidden player.

    :param Player enemy: The selected enemy.
    :rtype: None
    """
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


def print_plain_matrix(matrix: List[List[int]]) -> None:
    """
    Print the matrix, that represents the map.

    :param List[List[int]] matrix: The matrix that represents the map.
    :rtype: None
    """
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in matrix]))


def print_plain_map(matrix: List[List[int]], size: int) -> None:
    """
    Print the plain map, without any additional info.

    :param List[List[int]] matrix: The matrix that represents the map.
    :param int size: Size of the map.
    :rtype: None
    """
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


def print_map_info(player: Player, players: List[Player], matrix: List[List[int]], size: int) -> None:
    """
    Print the current position of all unhidden players in the map, and all the characteristics of it.

    :param Player player: The player that is currently playing.
    :param List[Player] players: Another competitors.
    :param List[List[int]] matrix: The matrix that represents the map.
    :param int size: Size of the map.
    :rtype: None
    """
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
    """
    Print all the possibilities of moving in the map, considering the player's move speed.

    :param str player_position: Original position of the player.
    :param List[str] possibilities: The possibilities of movements, previously calculated.
    :param List[List[int]] matrix: The matrix that represents the map.
    :param int size: Size of the map.
    :rtype: None
    """
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


def print_found_item(player_name: str, found: bool = False, item_tier: str = None, item_name: str = None) -> None:
    """
    Print if an item was found or not.

    :param str player_name: Player's name, whom is currently searching for an item.
    :param bool found: Whether the player has found it.
    :param str item_tier: Tier of the found item.
    :param str item_name: Item name.
    :rtype: None
    """
    if found:
        print('Player: {name} found a {tier} item! {item_name} \n'.format(name=player_name,
                                                                          tier=item_tier,
                                                                          item_name=item_name
                                                                          ))
    else:
        print('Player: {name} tried to find some item, but nothing was found! \n'.format(name=player_name))


def print_check_item(item: Item) -> None:
    """
    Print Item information that was selected by the player

    :param Item item: Item instance that will be printed.
    :rtype: None
    """
    print(colored('---- Item Description --- \n', 'green'))
    if isinstance(item, EquipmentItem):
        print(emojis.encode('{name}! is an equipment of {tier} tier  \n'
                            '{description} \n'
                            'Weight: {weight} kg \n'
                            'Attribute: + {base} {attribute} \n'.format(name=item.name,
                                                                        tier=item.tier,
                                                                        description=item.description,
                                                                        weight=item.weight,
                                                                        base=item.base,
                                                                        attribute=item.attribute)))
        print(colored('Side effects: \n', 'green'))
        for side_effect in item.side_effects:
            print(
                '{name}: {base} {attribute} duration: {duration}, occurrence: {occurrence}\n'.format(
                    name=side_effect.name,
                    base='+{base}'.format(
                        base=side_effect.base) if side_effect.effect_type == 'buff' else '-{base}'.format(
                        base=side_effect.base),
                    attribute=side_effect.attribute,
                    duration=side_effect.duration,
                    occurrence=side_effect.occurrence))
    if isinstance(item, RecoveryItem) or isinstance(item, HealingItem):
        print(emojis.encode('{name}! is an item of {tier} tier  \n'
                            '{description} \n'
                            'Weight: {weight} kg \n'
                            '\n'.format(name=item.name,
                                        tier=item.tier,
                                        description=item.description,
                                        weight=item.weight)))
