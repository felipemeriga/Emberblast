# from typing import List
#
# import timg
# from emojis import emojis
# from termcolor import colored
#
# from emberblast.interface import IPlayer, IItem, IEquipmentItem, IRecoveryItem, IHealingItem, ISkill, ISideEffect
# from emberblast.utils import get_project_root, convert_number_to_letter
#
#
# def print_greetings() -> None:
#     """
#     Print game greetings.
#
#     :rtype: None
#     """
#     obj = timg.Renderer()
#     project_path = get_project_root()
#     obj.load_image_from_file(str(project_path) + '/img/emberblast.png')
#     obj.resize(75, 75)
#     obj.render(timg.ASCIIMethod)
#     print(emojis.encode(colored(':fire: Welcome to Emberblast! :fire: \n\n', 'red')))
#
#
# def print_player_earned_xp(player_name: str, xp: int) -> None:
#     """
#     Print that a player as leveled up.
#
#     :param str player_name: The name of the player.
#     :param int xp: The amount of experience earned.
#     :rtype: None
#     """
#     print(f'\tPlayer {player_name} earned {xp} of experience! \n')
#
#
# def print_player_level_up(player_name: str, level: int) -> None:
#     """
#     Print that a player as leveled up.
#
#     :param str player_name: The name of the player.
#     :param int level: New level.
#     :rtype: None
#     """
#     print(f'\tPlayer {player_name} level up to {level}! \n')
#
#
# def print_player_stats(player: IPlayer):
#     """
#     Print the current playing player stats and attributes.
#
#     :param IPlayer player: The current player.
#     :rtype: None
#     """
#     print(emojis.encode(
#         '\n :man: {name} Stats: \n'.format(name=player.name)))
#     print(emojis.encode(
#         ':bar_chart: Level: {level} \n'
#         ':green_heart: Life: {life} \n'
#         ':blue_heart: Mana: {mana} \n'
#         ':runner: Move Speed: {move} \n'
#         ':books: Intelligence: {intelligence} \n'
#         ':dart: Accuracy: {accuracy} \n'
#         ':punch: Strength: {attack} \n'
#         ':shield: Armour: {armour} \n'
#         ':cyclone: Magic Resist: {resist} \n'
#         ':pray: Will: {will} \n'.format(level=player.level,
#                                         life=player.life,
#                                         mana=player.mana,
#                                         move=player.move_speed,
#                                         intelligence=player.intelligence,
#                                         accuracy=player.accuracy,
#                                         attack=player.strength,
#                                         armour=player.armour,
#                                         resist=player.magic_resist,
#                                         will=player.will)))
#
#
# def print_enemy_status(enemy: IPlayer) -> None:
#     """
#     Print the current status and attributes of a unhidden player.
#
#     :param IPlayer enemy: The selected enemy.
#     :rtype: None
#     """
#     print(emojis.encode(colored('\n Enemy {name}({job}) is currently at position: {position} \n'
#                                 ':bar_chart: Level: {level} \n'
#                                 ':green_heart: Life: {life} \n'
#                                 ':blue_heart: Mana: {mana} \n'
#                                 ':runner: Move Speed: {move} \n'
#                                 ':books: Intelligence: {intelligence} \n'
#                                 ':dart: Accuracy: {accuracy} \n'
#                                 ':punch: Strength: {attack} \n'
#                                 ':shield: Armour: {armour} \n'
#                                 ':cyclone: Magic Resist: {resist} \n'
#                                 ':pray: Will: {will} \n'.format(name=enemy.name,
#                                                                 job=enemy.job.get_name(),
#                                                                 position=enemy.position,
#                                                                 level=enemy.level,
#                                                                 life=enemy.life,
#                                                                 mana=enemy.mana,
#                                                                 move=enemy.move_speed,
#                                                                 intelligence=enemy.intelligence,
#                                                                 accuracy=enemy.accuracy,
#                                                                 attack=enemy.strength,
#                                                                 armour=enemy.armour,
#                                                                 resist=enemy.magic_resist,
#                                                                 will=enemy.will
#                                                                 ),
#                                 'red')))
#
#
# def print_plain_matrix(matrix: List[List[int]]) -> None:
#     """
#     Print the matrix, that represents the map.
#
#     :param List[List[int]] matrix: The matrix that represents the map.
#     :rtype: None
#     """
#     print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                      for row in matrix]))
#
#
# def print_plain_map(matrix: List[List[int]], size: int) -> None:
#     """
#     Print the plain map, without any additional info.
#
#     :param List[List[int]] matrix: The matrix that represents the map.
#     :param int size: Size of the map.
#     :rtype: None
#     """
#     # Print the columns first
#     print(' ' * 4, end="")
#     for column in range(size):
#         print('{:4}'.format(column), end="")
#     print('\n')
#     for row in range(size):
#         print('{:7}'.format(convert_number_to_letter(row)), end="")
#         for column in range(size):
#             print('{:4}'.format('*' if matrix[row][column] == 1 else ' '), end="")
#         print('')
#
#
# def print_map_info(player: IPlayer, players: List[IPlayer], matrix: List[List[int]], size: int) -> None:
#     """
#     Print the current position of all unhidden players in the map, and all the characteristics of it.
#
#     :param IPlayer player: The player that is currently playing.
#     :param List[IPlayer] players: Another competitors.
#     :param List[List[int]] matrix: The matrix that represents the map.
#     :param int size: Size of the map.
#     :rtype: None
#     """
#     foes_positions = []
#     print(colored('\n {name} is currently at position: {position}, '
#                   'with {life} HP'.format(name=player.name,
#                                           position=player.position,
#                                           life=player.life),
#                   'green'))
#
#     for opponent in players:
#         foes_positions.append(opponent.position)
#         print(colored('Enemy {name}({job}) is currently at position: {position}, '
#                       'with {life} HP'.format(name=opponent.name,
#                                               job=opponent.job.get_name(),
#                                               position=opponent.position,
#                                               life=opponent.life),
#                       'red'))
#
#     print(' ' * 4, end="")
#     for column in range(size):
#         print('{:4}'.format(column), end="")
#     print('\n')
#     for row in range(size):
#         print('{:7}'.format(convert_number_to_letter(row)), end="")
#         for column in range(size):
#             color = 'white'
#             attrs = ['bold']
#             position = convert_number_to_letter(row) + str(column)
#
#             if player.position == position:
#                 color = 'green'
#                 attrs.append('blink')
#             elif position in foes_positions:
#                 color = 'red'
#             print(colored('{:4}'.format('*' if matrix[row][column] == 1 else ' '), color, attrs=attrs), end="")
#         print('\n')
#
#
# def print_moving_possibilities(player_position: str, possibilities: List[str], matrix: List[List[int]],
#                                size: int) -> None:
#     """
#     Print all the possibilities of moving in the map, considering the player's move speed.
#
#     :param str player_position: Original position of the player.
#     :param List[str] possibilities: The possibilities of movements, previously calculated.
#     :param List[List[int]] matrix: The matrix that represents the map.
#     :param int size: Size of the map.
#     :rtype: None
#     """
#     print('Possibilities of Moving')
#     print(colored('You are on the Yellow tile', 'yellow'))
#     print(colored('Green tiles are the possibilities', 'green'))
#     print(' ' * 4, end="")
#     for column in range(size):
#         print('{:4}'.format(column), end="")
#     print('\n')
#     for row in range(size):
#         print('{:7}'.format(convert_number_to_letter(row)), end="")
#         for column in range(size):
#             color = 'white'
#             attrs = ['bold']
#             position = convert_number_to_letter(row) + str(column)
#
#             if position in possibilities:
#                 color = 'green'
#                 attrs.append('blink')
#             elif player_position == position:
#                 color = 'yellow'
#                 attrs.append('blink')
#             print(colored('{:4}'.format('*' if matrix[row][column] == 1 else ' '), color, attrs=attrs), end="")
#         print('')
#
#
# def print_found_item(player_name: str, found: bool = False, item_tier: str = None, item_name: str = None) -> None:
#     """
#     Print if an item was found or not.
#
#     :param str player_name: Player's name, whom is currently searching for an item.
#     :param bool found: Whether the player has found it.
#     :param str item_tier: Tier of the found item.
#     :param str item_name: Item name.
#     :rtype: None
#     """
#     if found:
#         print('\t{name} found a {tier} item! {item_name} \n'.format(name=player_name,
#                                                                   tier=item_tier,
#                                                                   item_name=item_name
#                                                                   ))
#     else:
#         print('\t{name} tried to find some item, but nothing was found! \n'.format(name=player_name))
#
#
# def print_no_foes_attack(player: IPlayer) -> None:
#     """
#     Print that there is not foe, within the attackers range.
#
#     :param IPlayer player: The attacker.
#     :rtype: None
#     """
#     print('There are not any available foes!')
#     print('For melee attack, foes must be in the same position as you: {position}'.format(position=player.position))
#     print('For ranged attack, foes must be within your range of {range}'.format(
#         range=player.get_ranged_attack_area()))
#
#
# def print_no_foes_skill(skill_range: int, player_position: str) -> None:
#     """
#     Print that there is not foe, within the attackers skill range.
#
#     :param int skill_range: The skill range.
#     :param str player_position: The attacker position.
#     :rtype: None
#     """
#     print('There are not any available foes!')
#     if skill_range == 0:
#         print('For melee skill, foes must be in the same position as you: {position}'.format(position=player_position))
#     else:
#         print('For ranged skill, foes must be within the skill range of {range}'.format(
#             range=skill_range))
#
#
# def print_area_damage(skill: ISkill, affected_players: List[IPlayer]) -> None:
#     """
#     Print that some skill affects an entire area.
#
#     :param ISkill skill: The casting skill.
#     :param List[IPlayer] affected_players: The players that will be affected by the skill.
#     :rtype: None
#     """
#     print('\n\t{name} is an area {kind} skill, and it will hit the following players: '.format(name=skill.name,
#                                                                                               kind=skill.kind))
#     for opponent in affected_players:
#         print(colored('\tEnemy {name}({job}) is currently at position: {position}, '
#                       'with {health_points} HP'.format(name=opponent.name,
#                                                        job=opponent.job.get_name(),
#                                                        position=opponent.position,
#                                                        health_points=opponent.life),
#                       'red'))
#     print('\n')
#
#
# def print_spent_mana(name: str, amount: int, skill_name: str) -> None:
#     """
#     Print that the player spent mana when casting a skill.
#
#     :param str name: Name of the player.
#     :param int amount: The amount spent.
#     :param str skill_name: The name of the skill.
#     :rtype: None
#     """
#     print('\t{player} casted {skill} for {amount} of mana.'.format(player=name, skill=skill_name, amount=amount))
#
#
# def print_add_side_effect(name: str, side_effect: ISideEffect) -> None:
#     """
#     Print that the player has got a side-effect.
#
#     :param str name: Name of the player.
#     :param ISideEffect side_effect: The side-effect that will be applied.
#     :rtype: None
#     """
#     if side_effect.effect_type == 'debuff' and side_effect.occurrence == 'constant':
#         side_effect_status = 'debuffed'
#     elif side_effect.effect_type == 'debuff' and side_effect.occurrence == 'iterated':
#         side_effect_status = 'inflicted'
#     else:
#         side_effect_status = 'buffed'
#
#     print('\t{player} has been {status} with {effect} side-effect. '.format(player=name,
#                                                                           status=side_effect_status,
#                                                                           effect=side_effect.name))
#
#
# def print_side_effect_ended(name: str, side_effect: ISideEffect) -> None:
#     """
#     Print that a side-effect duration has ended for a player.
#
#     :param str name: Name of the player.
#     :param ISideEffect side_effect: The side-effect that has ended.
#     :rtype: None
#     """
#     print('Side-effect: {effect} has ended for player: {name} \n'.format(effect=side_effect.name,
#                                                                          name=name))
#
#
# def print_iterated_side_effect_apply(name: str, side_effect: ISideEffect) -> None:
#     """
#     Print that the player passed its turn, and suffered/buffed from an iterated side-effect.
#
#     :param str name: Name of the player.
#     :param ISideEffect side_effect: The side-effect that will be applied.
#     :rtype: None
#     """
#     if side_effect.effect_type == 'buff':
#         status = 'increase'
#     else:
#         status = 'decrease'
#
#     if side_effect.attribute == 'health_points':
#         attribute = 'life'
#     elif side_effect.attribute == 'magic_points':
#         attribute = 'mana'
#     else:
#         attribute = side_effect.attribute
#     print('{name} has affected by {effect} side-effect, that will {status} player\'s {attribute} by {value} per turn. '
#           'More {turns} are left until the effect ends. \n'.format(name=name,
#                                                                    effect=side_effect.name,
#                                                                    status=status,
#                                                                    attribute=attribute,
#                                                                    value=side_effect.base,
#                                                                    turns=side_effect.duration))
#
#
# def print_player_low_mana(player: IPlayer) -> None:
#     """
#     Print that the player is running out of mana.
#
#     :param IPlayer player: Current player.
#     :rtype: None
#     """
#     print('{name} has {mana} of mana, considering healing it for casting skills. '.format(name=player.name,
#                                                                                           mana=player.mana))
#
#
# def print_heal(healer: IPlayer, foe: IPlayer, amount: int) -> None:
#     """
#     Print that the player healed himself or another one.
#
#     :param IPlayer healer: The healer.
#     :param IPlayer foe: The healed.
#     :param int amount: The amount of life healed.
#     :rtype: None
#     """
#     if healer == foe:
#         foe_name = 'itself'
#     else:
#         foe_name = foe.name
#     print('\t{name} healed {foe_name} for {amount} of health points!'.format(name=healer.name,
#                                                                            foe_name=foe_name,
#                                                                            amount=amount))
#     print('\t{foe_name} now has {life} of life'.format(foe_name=foe.name, life=foe.life))
#
#
# def print_missed(player: IPlayer, foe: IPlayer) -> None:
#     """
#     Print that the player missed the attack.
#
#     :param IPlayer player: The attacking player.
#     :param IPlayer foe: The foe suffering damage.
#     :rtype: None
#     """
#     print('\t{name} tried to attack {foe_name} but missed it.'.format(name=player.name, foe_name=foe.name))
#
#
# def print_trap_activated(player: IPlayer, side_effects: List[ISideEffect]) -> None:
#     """
#     Print that a player has fallen into a trap
#
#     :param IPlayer player: The attacking player.
#     :param ISideEffect side_effects: Side effects that will be applied.
#     :rtype: None
#     """
#     print('\t{player} has fallen into a trap, and got the following side-effects: '.format(player=player.name))
#     for side_effect in side_effects:
#         print(side_effect.name)
#
#
# def print_suffer_damage(attacker: IPlayer, foe: IPlayer, damage: int) -> None:
#     """
#     Print whenever a player inflicts damages to another players.
#
#     :param IPlayer attacker: The attacking player.
#     :param IPlayer foe: The one suffering the attack.
#     :param int damage: Amount of damage done.
#     :rtype: None
#     """
#     print('\t{name} inflicted a damage of {damage} on {foe_name}'.format(name=attacker.name,
#                                                                          damage=damage,
#                                                                          foe_name=foe.name))
#     if not foe.is_alive():
#         print(colored('\t{foe_name} it is now dead'.format(foe_name=foe.name), 'red'))
#     else:
#         print('\t{foe_name} now has {life} of life'.format(foe_name=foe.name, life=foe.life))
#
#
# def print_dice_result(name: str, result: int, kind: str, max_sides: int) -> None:
#     """
#     Print the result when a player rolls the dice.
#
#     :param str name: The name of the player who is rolling the dice.
#     :param int result: Dice result.
#     :param str kind: The purpose of rolling the dice, like attacking, skill.
#     :param int max_sides: The max sides of the dice, to detect critical attacks/skills.
#     :rtype: None
#     """
#     print('\t{name} rolled the dice and got {result}!'.format(name=name, result=result))
#     if result == max_sides:
#         print('\tIt is a critical {kind}! You will execute a massive amount of damage!'.format(kind=kind))
#
#
# def print_use_item(player_name: str, item_name: str, target_name: str) -> None:
#     """
#     Notify another players, that someone used an item.
#
#     :param str player_name: The player name that is currently using an item.
#     :param str item_name: The item name that is being used.
#     :param str target_name: The name of who is the item used on.
#     :rtype: None
#     """
#     if target_name == player_name:
#         target_name = 'himself'
#     print('\t{name} used an item: {item}, on {target}'.format(name=player_name,
#                                                               item=item_name,
#                                                               target=target_name))
#
#
# def print_player_fail_stole_item(name: str, foe_name: str) -> None:
#     """
#     Print that a player has failed in stealing an item
#
#     :param str name: Name of the player.
#     :param str foe_name: Name of the foe.
#     :rtype: None
#     """
#     print(f'\tPlayer {name} failed to steal an item from {foe_name} \n')
#
#
# def print_player_stole_item(name: str, foe_name: str, item_name: str, tier: str) -> None:
#     """
#     Print that a player has stolen an item
#
#     :param str name: Name of the player.
#     :param str foe_name: Name of the foe.
#     :param str item_name: Name of the stolen item.
#     :param str tier: tier of the item.
#     :rtype: None
#     """
#
#     print('\tPlayer {player} stole an item from {foe}! It was a {item}, of tier {tier}\n'.format(player=name,
#                                                                                                  foe=foe_name,
#                                                                                                  item=item_name,
#                                                                                                  tier=tier))
#
#
# def print_player_won(name: str) -> None:
#     """
#     Print the player that won the game.
#
#     :param str name: Name of the player.
#     :rtype: None
#     """
#     color = 'green'
#     attrs = ['bold', 'blink']
#
#     print(colored('Player {player} won the game! \n'.format(player=name), color, attrs=attrs),
#           end="")
#
#
# def print_create_new_character(number: int) -> None:
#     """
#     Print the status, that someone is currently creating one character.
#
#     :param int number: Number of the player.
#     :rtype: None
#     """
#     color = 'green'
#     attrs = ['bold', 'blink']
#
#     print(colored('Creating controlled character number: {number}... \n'.format(number=number), color, attrs=attrs),
#           end="")
#
#
# def print_event(event: str) -> None:
#     color = ''
#     attrs = ['bold']
#     if event == 'attack':
#         color = 'red'
#         print(emojis.encode(colored(':crossed_swords: ATTACK: ', color, attrs=attrs)))
#     elif event == 'skill':
#         color = 'blue'
#         print(emojis.encode(colored(':fire: SKILL: ', color, attrs=attrs)))
#     elif event == 'search':
#         color = 'yellow'
#         print(emojis.encode(colored(':eye: SEARCH: ', color, attrs=attrs)))
#     elif event == 'item':
#         color = 'green'
#         print(emojis.encode(colored(':test_tube: ITEM: ', color, attrs=attrs)))
#
#
# def print_check_item(item: IItem) -> None:
#     """
#     Print Item information that was selected by the player
#
#     :param IItem item: Item instance that will be printed.
#     :rtype: None
#     """
#     print(colored('---- Item Description --- \n', 'green'))
#     if isinstance(item, IEquipmentItem):
#         print(emojis.encode('{name}! is an equipment of {tier} tier  \n'
#                             '{description} \n'
#                             'Weight: {weight} kg \n'
#                             'Attribute: + {base} {attribute} \n'.format(name=item.name,
#                                                                         tier=item.tier,
#                                                                         description=item.description,
#                                                                         weight=item.weight,
#                                                                         base=item.base,
#                                                                         attribute=item.attribute)))
#         if len(item.side_effects) > 0:
#             print(colored('Side effects: \n', 'green'))
#             for side_effect in item.side_effects:
#                 print(
#                     '{name}: {base} {attribute} duration: {duration}, occurrence: {occurrence}\n'.format(
#                         name=side_effect.name,
#                         base='+{base}'.format(
#                             base=side_effect.base) if side_effect.effect_type == 'buff' else '-{base}'.format(
#                             base=side_effect.base),
#                         attribute=side_effect.attribute,
#                         duration=side_effect.duration,
#                         occurrence=side_effect.occurrence))
#     if isinstance(item, IRecoveryItem) or isinstance(item, IHealingItem):
#         print(emojis.encode('{name}! is an item of {tier} tier  \n'
#                             '{description} \n'
#                             'Weight: {weight} kg \n'
#                             '\n'.format(name=item.name,
#                                         tier=item.tier,
#                                         description=item.description,
#                                         weight=item.weight)))
