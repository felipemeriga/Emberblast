import multiprocessing
import os
import time
from typing import List

import timg
from colorama import Fore
from emojis import emojis
from termcolor import colored

from emberblast.interface import IInformingSystem, IPlayer, ISkill, ISideEffect, IItem, IEquipmentItem, IRecoveryItem, \
    IHealingItem
from emberblast.utils import get_project_root, convert_number_to_letter


class InformerCMD(IInformingSystem):

    def __init__(self) -> None:
        super().__init__()

    def greetings(self) -> None:
        obj = timg.Renderer()
        project_path = get_project_root()
        obj.load_image_from_file(str(project_path) + '/img/emberblast.png')
        obj.resize(75, 75)
        obj.render(timg.ASCIIMethod)
        print(emojis.encode(colored(':fire: Welcome to Emberblast! :fire: \n\n', 'red')))

    def new_turn(self, turn: int) -> None:
        print(Fore.GREEN + emojis.encode(
            ':fire: Starting Turn {turn}! Embrace Yourselves! :fire: \n\n'.format(turn=turn)))
        print(Fore.RESET)

    def player_turn(self, name: str) -> None:
        print(emojis.encode(
            f':man: {name} Time! \n'))

    def line_separator(self) -> None:
        """
        Display that an user executed one of the available actions

        :param str event: The selected event.
        :rtype: None
        """
        term_size = os.get_terminal_size()
        print(u'\u2500' * term_size.columns)

    def moved(self, player_name: str) -> None:
        print(f'\t{player_name} has just moved to another position \n')

    def player_earned_xp(self, player_name: str, xp: int) -> None:
        print(f'\tPlayer {player_name} earned {xp} xp of experience! \n')

    def player_killed_enemy_earned_xp(self, player_name: str, foe: str, xp: int) -> None:
        print(f'\tPlayer {player_name} got extra {xp} xp of experience, by killing {foe}! \n')

    def player_level_up(self, player_name: str, level: int) -> None:
        print(f'\t{player_name} level up to {level}! \n')

    def player_stats(self, player: IPlayer):
        print(emojis.encode(
            '\n :man: {name} Stats: \n'.format(name=player.name)))
        print(emojis.encode(
            ':bar_chart: Level: {level} \n'
            ':green_heart: Life: {life} \n'
            ':blue_heart: Mana: {mana} \n'
            ':runner: Move Speed: {move} \n'
            ':books: Intelligence: {intelligence} \n'
            ':dart: Accuracy: {accuracy} \n'
            ':punch: Strength: {attack} \n'
            ':shield: Armour: {armour} \n'
            ':cyclone: Magic Resist: {resist} \n'
            ':pray: Will: {will} \n'.format(level=player.level,
                                            life=player.life,
                                            mana=player.mana,
                                            move=player.move_speed,
                                            intelligence=player.intelligence,
                                            accuracy=player.accuracy,
                                            attack=player.strength,
                                            armour=player.armour,
                                            resist=player.magic_resist,
                                            will=player.will)))

    def enemy_status(self, enemy: IPlayer) -> None:
        print(emojis.encode(colored('\n Enemy {name}({job}) is currently at position: {position} \n'
                                    ':bar_chart: Level: {level} \n'
                                    ':green_heart: Life: {life} \n'
                                    ':blue_heart: Mana: {mana} \n'
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
                                                                    life=enemy.life,
                                                                    mana=enemy.mana,
                                                                    move=enemy.move_speed,
                                                                    intelligence=enemy.intelligence,
                                                                    accuracy=enemy.accuracy,
                                                                    attack=enemy.strength,
                                                                    armour=enemy.armour,
                                                                    resist=enemy.magic_resist,
                                                                    will=enemy.will
                                                                    ),
                                    'red')))

    def plain_matrix(self, matrix: List[List[int]]) -> None:
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in matrix]))

    def plain_map(self, matrix: List[List[int]], size: int) -> None:
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

    def map_info(self, player: IPlayer, players: List[IPlayer], matrix: List[List[int]], size: int) -> None:
        foes_positions = []
        print(colored('\n {name} is currently at position: {position}, '
                      'with {life} HP'.format(name=player.name,
                                              position=player.position,
                                              life=player.life),
                      'green'))

        for opponent in players:
            foes_positions.append(opponent.position)
            print(colored('Enemy {name}({job}) is currently at position: {position}, '
                          'with {life} HP'.format(name=opponent.name,
                                                  job=opponent.job.get_name(),
                                                  position=opponent.position,
                                                  life=opponent.life),
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
            print('\n')

    def moving_possibilities(self, player_position: str, possibilities: List[str], matrix: List[List[int]],
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

    def found_item(self, player_name: str, found: bool = False, item_tier: str = None, item_name: str = None) -> None:
        if found:
            print('\t{name} found a {tier} item! {item_name} \n'.format(name=player_name,
                                                                        tier=item_tier,
                                                                        item_name=item_name
                                                                        ))
        else:
            print('\t{name} tried to find some item, but nothing was found! \n'.format(name=player_name))

    def no_foes_attack(self, player: IPlayer) -> None:
        print('There are not any available foes!')
        print('For melee attack, foes must be in the same position as you: {position}'.format(position=player.position))
        print('For ranged attack, foes must be within your range of {range}'.format(
            range=player.get_ranged_attack_area()))

    def no_foes_skill(self, skill_range: int, player_position: str) -> None:
        print('There are not any available foes!')
        if skill_range == 0:
            print('For melee skill, foes must be in the same position as you: {position}'.format(
                position=player_position))
        else:
            print('For ranged skill, foes must be within the skill range of {range}'.format(
                range=skill_range))

    def area_damage(self, skill: ISkill, affected_players: List[IPlayer]) -> None:
        print('\n\t{name} is an area {kind} skill, and it will hit the following players: '.format(name=skill.name,
                                                                                                   kind=skill.kind))
        for opponent in affected_players:
            print(colored('\tEnemy {name}({job}) is currently at position: {position}, '
                          'with {health_points} HP'.format(name=opponent.name,
                                                           job=opponent.job.get_name(),
                                                           position=opponent.position,
                                                           health_points=opponent.life),
                          'red'))
        print('\n')

    def spent_mana(self, name: str, amount: int, skill_name: str) -> None:
        print('\t{player} casted {skill} for {amount} of mana.'.format(player=name, skill=skill_name, amount=amount))

    def add_side_effect(self, name: str, side_effect: ISideEffect) -> None:
        if side_effect.effect_type == 'debuff' and side_effect.occurrence == 'constant':
            side_effect_status = 'debuffed'
        elif side_effect.effect_type == 'debuff' and side_effect.occurrence == 'iterated':
            side_effect_status = 'inflicted'
        else:
            side_effect_status = 'buffed'

        print('\t{player} has been {status} with {effect} side-effect. '.format(player=name,
                                                                                status=side_effect_status,
                                                                                effect=side_effect.name))

    def side_effect_ended(self, name: str, side_effect: ISideEffect) -> None:
        print('\t{effect} has ended for player: {name} \n'.format(effect=side_effect.name,
                                                                  name=name))

    def iterated_side_effect_apply(self, name: str, side_effect: ISideEffect) -> None:
        if side_effect.effect_type == 'buff':
            status = 'increase'
        else:
            status = 'decrease'

        if side_effect.attribute == 'health_points':
            attribute = 'life'
        elif side_effect.attribute == 'magic_points':
            attribute = 'mana'
        else:
            attribute = side_effect.attribute
        print(
            '\t{name} has affected by {effect} side-effect, that will {status} player\'s {attribute} by {value} per '
            'turn. More {turns} are left until the effect ends. \n'.format(name=name,
                                                                           effect=side_effect.name,
                                                                           status=status,
                                                                           attribute=attribute,
                                                                           value=side_effect.base,
                                                                           turns=side_effect.duration))

    def low_mana(self, player: IPlayer) -> None:
        print('{name} has {mana} of mana, considering healing it for casting skills. '.format(name=player.name,
                                                                                              mana=player.mana))

    def heal(self, healer: IPlayer, foe: IPlayer, amount: int) -> None:
        if healer == foe:
            foe_name = 'itself'
        else:
            foe_name = foe.name
        print('\t{name} healed {foe_name} for {amount} of health points!'.format(name=healer.name,
                                                                                 foe_name=foe_name,
                                                                                 amount=amount))
        print('\t{foe_name} now has {life} of life'.format(foe_name=foe.name, life=foe.life))

    def missed(self, player: IPlayer, foe: IPlayer) -> None:
        print('\t{name} tried to attack {foe_name} but missed it.'.format(name=player.name, foe_name=foe.name))

    def trap_activated(self, player: IPlayer, side_effects: List[ISideEffect]) -> None:
        print('\t{player} has fallen into a trap, and got the following side-effects: '.format(player=player.name))
        for side_effect in side_effects:
            print(side_effect.name)

    def suffer_damage(self, attacker: IPlayer, foe: IPlayer, damage: int) -> None:
        print('\t{name} inflicted a damage of {damage} on {foe_name}'.format(name=attacker.name,
                                                                             damage=damage,
                                                                             foe_name=foe.name))
        if not foe.is_alive():
            print(colored('\t{foe_name} it is now dead'.format(foe_name=foe.name), 'red'))
        else:
            print('\t{foe_name} now has {life} of life'.format(foe_name=foe.name, life=foe.life))

    def dice_result(self, name: str, result: int, kind: str, max_sides: int) -> None:
        print('\t{name} rolled the dice and got {result}!'.format(name=name, result=result))
        if result == max_sides:
            print('\tIt is a critical {kind}! You will execute a massive amount of damage!'.format(kind=kind))

    def use_item(self, player_name: str, item_name: str, target_name: str) -> None:
        if target_name == player_name:
            target_name = 'himself'
        print('\t{name} used an item: {item}, on {target}'.format(name=player_name,
                                                                  item=item_name,
                                                                  target=target_name))

    def player_fail_stole_item(self, name: str, foe_name: str) -> None:
        print(f'\tPlayer {name} failed to steal an item from {foe_name} \n')

    def player_stole_item(self, name: str, foe_name: str, item_name: str, tier: str) -> None:
        print('\tPlayer {player} stole an item from {foe}! It was a {item}, of tier {tier}\n'.format(player=name,
                                                                                                     foe=foe_name,
                                                                                                     item=item_name,
                                                                                                     tier=tier))

    def player_won(self, name: str) -> None:
        color = 'green'
        attrs = ['bold', 'blink']

        print(colored('Player {player} won the game! \n'.format(player=name), color, attrs=attrs),
              end="")

    def create_new_character(self, number: int) -> None:
        color = 'green'
        attrs = ['bold', 'blink']

        print(colored('Creating controlled character number: {number}... \n'.format(number=number), color, attrs=attrs),
              end="")

    def event(self, event: str) -> None:
        attrs = ['bold']
        if event == 'attack':
            color = 'red'
            print(emojis.encode(colored(':crossed_swords: ATTACK: ', color, attrs=attrs)))
        elif event == 'skill':
            color = 'blue'
            print(emojis.encode(colored(':fire: SKILL: ', color, attrs=attrs)))
        elif event == 'search':
            color = 'yellow'
            print(emojis.encode(colored(':eye: SEARCH: ', color, attrs=attrs)))
        elif event == 'item':
            color = 'green'
            print(emojis.encode(colored(':test_tube: ITEM: ', color, attrs=attrs)))
        elif event == 'move':
            color = 'cyan'
            print(emojis.encode(colored(':runner: MOVE: ', color, attrs=attrs)))
        elif event == 'side-effect':
            color = 'magenta'
            print(emojis.encode(colored(':grey_exclamation: SIDE-EFFECT: ', color, attrs=attrs)))

    def check_item(self, item: IItem) -> None:
        print(colored('---- Item Description --- \n', 'green'))
        if isinstance(item, IEquipmentItem):
            print(emojis.encode('{name}! is an equipment of {tier} tier  \n'
                                '{description} \n'
                                'Weight: {weight} kg \n'
                                'Attribute: + {base} {attribute} \n'.format(name=item.name,
                                                                            tier=item.tier,
                                                                            description=item.description,
                                                                            weight=item.weight,
                                                                            base=item.base,
                                                                            attribute=item.attribute)))
            if len(item.side_effects) > 0:
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
        if isinstance(item, IRecoveryItem) or isinstance(item, IHealingItem):
            print(emojis.encode('{name}! is an item of {tier} tier  \n'
                                '{description} \n'
                                'Weight: {weight} kg \n'
                                '\n'.format(name=item.name,
                                            tier=item.tier,
                                            description=item.description,
                                            weight=item.weight)))

    def force_loading(self, loading_time: int, prefix: str = '', prefix_attributes: List[str] = None) -> None:
        if prefix != '':
            print(colored(prefix, None, attrs=prefix_attributes))
        p = multiprocessing.Process(target=print_loading)
        p.start()

        p.join(loading_time)

        # If thread is still active
        if p.is_alive():
            p.kill()
            print(" " * len(animation[0]), end="\r")


animation = [
    "          ",
    ".         ",
    "..        ",
    "...       ",
    "....      ",
    ".....     ",
    "......    ",
    ".......   ",
    "........  ",
    "......... ",
    "..........",
    " .........",
    "  ........",
    "   .......",
    "    ......",
    "     .....",
    "      ....",
    "       ...",
    "        ..",
    "         ."
]


def print_loading() -> None:
    notcomplete = True

    i = 0

    while notcomplete:
        print(animation[i % len(animation)], end='\r')
        time.sleep(.05)
        i += 1
