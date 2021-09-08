import collections
import functools
import math
import random
from typing import Dict, List, Optional, Union

from project.item import EquipmentItem
from project.message import print_map_info, print_dice_result, print_suffer_damage, print_missed, print_area_damage

from project.interface import IBotDecisioning, IGame, IAction, IPlayer, IPlayingMode, ISkill, IEquipmentItem, \
    ISkillAction


class BotDecisioning(IBotDecisioning):

    def __init__(self, game: IGame) -> None:
        self.game = game
        self.current_bot: Optional[IPlayer] = None
        self.current_play_style = IPlayingMode.NEUTRAL
        self.prioritized_foes = []
        self.possible_foe: Optional[IPlayer] = None

    def get_skills_average_range(self) -> int:
        self.current_bot.refresh_skills_list()
        ranges = []
        if len(self.current_bot.skills) == 0:
            return 0
        for skill in self.current_bot.skills:
            if skill.cost < self.current_bot.mana:
                ranges.append(skill.ranged)

        return math.floor(functools.reduce(lambda a, b: a + b, ranges) / len(ranges))

    def get_remaining_players_position(self) -> List[str]:
        remaining_players = self.game.get_remaining_players(self.current_bot)
        return [x for x in map(lambda player: player.position, remaining_players)]

    def find_foes_within_damage_range(self) -> Optional[IPlayer]:
        possible_foe = None
        attack_range_possibilities = [self.current_bot.position]

        attack_range = self.current_bot.get_ranged_attack_area()
        if self.current_bot.job.attack_type == 'ranged':
            attack_range_possibilities.extend(self.game.game_map.graph.get_available_nodes_in_range(
                self.current_bot.position,
                attack_range))
        skill_range = self.get_skills_average_range()
        skill_range_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
            self.current_bot.position,
            skill_range)

        for foe in self.prioritized_foes:
            if foe.position in attack_range_possibilities or \
                    foe.position in skill_range_possibilities:
                possible_foe = foe
                break
        return possible_foe

    def find_foes(self, movement_possibilities: List[str]) -> Optional[IPlayer]:
        possible_foe = None
        attack_range = self.current_bot.get_ranged_attack_area()
        attack_range_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
            self.current_bot.position,
            attack_range)
        skill_range = self.get_skills_average_range()
        skill_range_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
            self.current_bot.position,
            skill_range)

        for foe in self.prioritized_foes:
            if foe.position in movement_possibilities or \
                    foe.position in attack_range_possibilities or \
                    foe.position in skill_range_possibilities:
                possible_foe = foe
                break
        return possible_foe

    def sort_foes_by_priority(self) -> None:
        remaining_players = self.game.get_remaining_players(self.current_bot)
        priorities_map = {}
        for player in remaining_players:
            distance = self.game.game_map.graph.get_shortest_distance_between_positions(self.current_bot.position,
                                                                                        player.position)
            priority = distance + player.life / 2

            # We need to use player as the key, because players may have the same name, and priority, using objects
            # address will never fall into that case.
            priorities_map[player] = priority

        self.prioritized_foes = list(
            collections.OrderedDict(sorted(priorities_map.items(), key=lambda item: item[1])).keys())

    def attack(self, skill_action: Union[ISkillAction, IAction]) -> None:
        if self.possible_foe is None:
            self.current_play_style = IPlayingMode.DEFENSIVE
            return

            # This dictionary represents the possibilities of attack/skills that a bot can perform, where the keys
        # are the attack/skills and the values the possible damage that this one may inflict
        attack_possibilities_dict = {}
        attack_range = self.current_bot.get_ranged_attack_area()
        attack_range_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
            self.current_bot.position,
            attack_range)

        if (self.current_bot.job.attack_type == 'melee' and self.possible_foe.position == self.current_bot.position) \
                or (
                self.current_bot.job.attack_type == 'ranged'
                and self.possible_foe.position in attack_range_possibilities):
            attack_possibilities_dict['attack'] = self.current_bot.get_attribute_real_value(
                self.current_bot.job.damage_vector, self.current_bot.job.attack_type
            )
        for skill in self.current_bot.skills:
            if skill.cost < self.current_bot.mana and skill.kind == 'inflict':
                attack_possibilities_dict[skill] = self.current_bot.get_attribute_real_value(
                    skill.base_attribute
                ) + skill.base

        sorted_attack_possibilities_tuple = sorted(attack_possibilities_dict.items(), key=lambda x: x[1], reverse=True)
        best_attack = next(iter(sorted_attack_possibilities_tuple))[0]
        dice_result = self.game.roll_the_dice()

        if best_attack == 'attack':
            print_dice_result(self.current_bot.name, dice_result, 'attack', self.game.dice_sides)

            targeted_defense = 'armour' if self.current_bot.job.damage_vector == 'strength' else 'magic_resist'

            damage = math.ceil(
                self.current_bot.get_attribute_real_value(self.current_bot.job.damage_vector,
                                                          self.current_bot.job.attack_type) + (
                        dice_result / self.game.dice_sides) * 5
                - self.possible_foe.get_attribute_real_value(targeted_defense))
            if damage > 0:
                self.possible_foe.suffer_damage(damage)
                print_suffer_damage(self.current_bot, self.possible_foe, damage)
            else:
                print_missed(self.current_bot, self.possible_foe)
            return
        elif isinstance(best_attack, ISkill):
            foes = []
            if best_attack.area > 0:
                foes = skill_action.get_affected_players_area_skill(self.possible_foe, self.prioritized_foes,
                                                                    best_attack.area)
                if len(foes) > 0:
                    print_area_damage(best_attack, foes)
            else:
                foes.append(self.possible_foe)
            print_dice_result(self.current_bot.name, dice_result, 'attack', self.game.dice_sides)
            dice_result_normalized = dice_result / self.game.dice_sides
            best_attack.execute(self.current_bot, foes, dice_result_normalized)
        else:
            self.current_play_style = IPlayingMode.DEFENSIVE

    def move(self) -> None:
        remaining_players_positions = self.get_remaining_players_position()
        move_speed = self.current_bot.get_attribute_real_value('move_speed')
        possibilities = self.game.game_map.graph.get_available_nodes_in_range(self.current_bot.position, move_speed)

        if self.current_play_style == IPlayingMode.DEFENSIVE:
            safer_positions_map = self.game.game_map.graph. \
                get_average_distances_sources_destinations_map(possibilities, remaining_players_positions)

            sorted_safer_positions_tuple = sorted(safer_positions_map.items(), key=lambda x: x[1], reverse=True)
            safest_place = next(iter(sorted_safer_positions_tuple))[0]
            self.current_bot.set_position(safest_place)
        if self.current_play_style == IPlayingMode.AGGRESSIVE:
            possible_foe = self.find_foes(possibilities)

            if possible_foe is None:
                aggressive_positions_map = self.game.game_map.graph. \
                    get_average_distances_sources_destinations_map(possibilities, remaining_players_positions)
                sorted_aggressive_positions_tuple = sorted(aggressive_positions_map.items(), key=lambda x: x[1],
                                                           reverse=False)
                best_place = next(iter(sorted_aggressive_positions_tuple))[0]
                self.current_bot.set_position(best_place)
            else:
                if self.current_bot.job.attack_type == 'melee':
                    self.current_bot.set_position(possible_foe.position)
                elif self.current_bot.job.attack_type == 'ranged':
                    attack_range = self.current_bot.get_ranged_attack_area()
                    aggressive_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
                        possible_foe.position,
                        attack_range)
                    best_position = random.choice(aggressive_possibilities)
                    self.current_bot.set_position(best_position)
                self.possible_foe = possible_foe
        if self.current_play_style == IPlayingMode.NEUTRAL:
            random_position = random.choice(possibilities)
            self.current_bot.set_position(random_position)

    def probability_of_damage(self, foe: IPlayer) -> bool:
        if self.current_bot.job.intelligence > self.current_bot.job.strength:
            if self.current_bot.get_attribute_real_value('intelligence') > self.current_bot.get_attribute_real_value(
                    'magic_resist'):
                return True
        else:
            if self.current_bot.get_attribute_real_value('strength') > self.current_bot.get_attribute_real_value(
                    'armour'):
                return True
        return False

    def select_best_equipment(self, equipped: IEquipmentItem,
                              new_equipment: IEquipmentItem) -> Optional[IEquipmentItem]:
        best_choice = {
            equipped: 0,
            new_equipment: 0
        }
        if equipped.category != new_equipment.category:
            return None

        if equipped.category == 'weapon':
            if new_equipment.attribute != self.current_bot.job.damage_vector:
                best_choice[equipped] = best_choice.get(equipped, 0) + 1

        if new_equipment.base > equipped.base:
            best_choice[new_equipment] = best_choice.get(new_equipment, 0) + 1
        else:
            best_choice[equipped] = best_choice.get(equipped, 0) + 1

        if len(new_equipment.side_effects) > len(equipped.side_effects):
            best_choice[new_equipment] = best_choice.get(new_equipment, 0) + 1
        else:
            best_choice[equipped] = best_choice.get(equipped, 0) + 1

        sorted_choice_tuple = sorted(best_choice.items(), key=lambda x: x[1], reverse=True)
        return next(iter(sorted_choice_tuple))[0]

    def equip_item(self) -> None:
        equipments = self.current_bot.bag.get_equipments()

        for equipment in equipments:
            if self.current_bot.equipment.is_equipped(equipment):
                continue
            if self.current_bot.equipment.__getattribute__(equipment.category) is None:
                self.current_bot.equipment.equip(equipment)
            else:
                best_equip = self.select_best_equipment(self.current_bot.equipment.__getattribute__(equipment.category),
                                                        equipment)
                if best_equip is not None:
                    self.current_bot.equipment.equip(best_equip)

    def select_playing_mode(self) -> None:
        remaining_players = self.game.get_remaining_players(player=self.current_bot, include_hidden=True)
        low_life_level = self.current_bot.life * 0.3

        if self.current_bot.life > low_life_level:
            self.current_play_style = IPlayingMode.AGGRESSIVE
        elif self.current_bot.life < low_life_level and len(remaining_players) > 1:
            self.current_play_style = IPlayingMode.DEFENSIVE
        elif self.current_bot.life < low_life_level and len(remaining_players) == 1 and self.probability_of_damage(
                remaining_players[0]):
            self.current_play_style = IPlayingMode.AGGRESSIVE
        else:
            self.current_play_style = IPlayingMode.DEFENSIVE

    def decide(self, player: IPlayer, actions: Dict[str, IAction]) -> None:
        self.current_bot = player
        self.sort_foes_by_priority()
        self.select_playing_mode()
        skill_action = actions.get('skill')
        if skill_action is None:
            return
        # print_map_info(self.current_bot, self.prioritized_foes, self.game.game_map.graph.matrix,
        #                self.game.game_map.size)

        self.possible_foe = self.find_foes_within_damage_range()

        if self.current_play_style == IPlayingMode.AGGRESSIVE and \
                self.possible_foe is not None:
            self.attack(skill_action)
            self.current_play_style = IPlayingMode.NEUTRAL
            self.move()
        elif self.current_play_style == IPlayingMode.AGGRESSIVE and \
                self.possible_foe is None:
            self.move()
            self.attack(skill_action)
        else:
            self.move()

        if self.current_play_style == IPlayingMode.DEFENSIVE:
            pass

        search_action = actions.get('search', None)

        if search_action is not None:
            search_action.act(self.current_bot)

        self.equip_item()
