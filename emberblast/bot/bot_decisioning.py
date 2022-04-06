import collections
import functools
import math
import random
from typing import List, Optional

from emberblast.communicator import communicator_injector
from emberblast.conf import get_configuration

from emberblast.interface import IBotDecisioning, IGame, IPlayer, IPlayingMode, ISkill, IEquipmentItem, \
    IHealingItem
from emberblast.utils.constants import EXPERIENCE_EARNED_ACTION


@communicator_injector()
class BotDecisioning(IBotDecisioning):

    def __init__(self, game: IGame) -> None:
        self.game = game
        self.current_bot: Optional[IPlayer] = None
        self.current_play_style = IPlayingMode.NEUTRAL
        self.prioritized_foes: List[IPlayer] = []
        self.possible_foe: Optional[IPlayer] = None

    def reset_attributes(self) -> None:
        self.prioritized_foes = []
        self.possible_foe = None
        self.current_play_style = IPlayingMode.NEUTRAL

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
            if foe.position in attack_range_possibilities and foe.is_hidden() is False or \
                    foe.position in skill_range_possibilities and foe.is_hidden() is False:
                possible_foe = foe
                break
        return possible_foe

    def search_on_map(self):
        found_items = self.game.game_map.check_item_in_position(self.current_bot.position)
        if found_items is not None:
            for item in found_items:
                self.current_bot.bag.add_item(item)
                self.communicator.informer.found_item(player_name=self.current_bot.name, found=True,
                                                      item_tier=item.tier,
                                                      item_name=item.name)
        else:
            self.communicator.informer.found_item(player_name=self.current_bot.name)
        return

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
        remaining_players = self.game.get_remaining_players(self.current_bot, include_hidden=False)
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

    def get_affected_players_area_skill(self, target_player: IPlayer, remaining_players: List[IPlayer],
                                        skill_affected_area):
        area_foes = [target_player]
        remaining_players.remove(target_player)
        position_possibilities = self.game.game_map.graph.get_available_nodes_in_range(target_player.position,
                                                                                       skill_affected_area)

        for player in remaining_players:
            if player.position in position_possibilities:
                area_foes.append(player)

        return area_foes

    def prepare_execute_skill(self, skill: ISkill) -> None:
        self.communicator.informer.event('skill')
        dice_result = self.game.roll_the_dice()
        foes = []
        prefix = 'attack'

        if skill.kind == 'recover':
            foes = [self.current_bot]
            prefix = 'recover'
        if skill.area > 0:
            foes = self.get_affected_players_area_skill(self.possible_foe, self.prioritized_foes,
                                                        skill.area)
            if len(foes) > 0:
                self.communicator.informer.area_damage(skill, foes)
        elif skill.area == 0 and skill.kind == 'inflict':
            foes.append(self.possible_foe)

        self.communicator.informer.dice_result(self.current_bot.name, dice_result, prefix, self.game.dice_sides)
        dice_result_normalized = dice_result / self.game.dice_sides
        skill.execute(self.current_bot, foes, dice_result_normalized)

    def decide_best_defensive_action(self) -> None:
        recovery_choices = {}
        items = self.current_bot.bag.get_usable_items()
        healing_skills = [x for x in filter(lambda skill: skill.kind == 'recover', self.current_bot.skills)]
        low_mana_level = self.current_bot.magic_points * 0.3
        low_life_level = self.current_bot.health_points * 0.3
        recover_attribute = ''
        remaining_quantity = 0

        if self.current_bot.mana <= low_mana_level and self.current_bot.job.damage_vector == 'intelligence':
            recover_attribute = 'magic_points'
            remaining_quantity = self.current_bot.magic_points - self.current_bot.mana
        elif self.current_bot.life <= low_life_level:
            recover_attribute = 'health_points'
            remaining_quantity = self.current_bot.health_points - self.current_bot.life
        elif self.current_bot.accuracy > self.current_bot.armour:
            current_accuracy = self.current_bot.get_attribute_real_value('accuracy')
            additional = (current_accuracy / 5 * 10) / 100
            result = self.game.chose_probability(additional=[additional])
            self.current_bot.set_hidden(result)
            return
        else:
            self.current_bot.set_defense_mode(True)
            return

        for item in items:
            if isinstance(item, IHealingItem):
                if item.attribute == recover_attribute:
                    closer_value = abs(remaining_quantity - item.base)
                    recovery_choices[item] = closer_value

        for skill in healing_skills:
            if skill.cost < self.current_bot.mana:
                closer_value = abs(remaining_quantity - skill.base)
                recovery_choices[skill] = closer_value

        if len(recovery_choices) < 1:
            return
        sorted_recovery_possibilities = sorted(recovery_choices.items(), key=lambda x: x[1], reverse=False)
        best_option = next(iter(sorted_recovery_possibilities))[0]

        if isinstance(best_option, IHealingItem):
            self.communicator.informer.event('item')
            self.current_bot.use_item(best_option)
            self.communicator.informer.use_item(self.current_bot.name, best_option.name, self.current_bot.name)
            self.current_bot.bag.remove_item(best_option)
        elif isinstance(best_option, ISkill):
            self.prepare_execute_skill(best_option)

    def attack(self) -> None:
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
        attack_range_possibilities.append(self.current_bot.position)

        if (self.current_bot.job.attack_type == 'melee' and self.possible_foe.position == self.current_bot.position) \
                or (
                self.current_bot.job.attack_type == 'ranged'
                and self.possible_foe.position in attack_range_possibilities):
            attack_possibilities_dict['attack'] = self.current_bot.get_attribute_real_value(
                self.current_bot.job.damage_vector, self.current_bot.job.attack_type
            )
        for skill in self.current_bot.skills:
            if skill.cost < self.current_bot.mana and skill.kind == 'inflict' \
                    and self.game.game_map.graph.is_target_in_range(self.current_bot.position,
                                                                    skill.ranged,
                                                                    self.possible_foe.position):
                attack_possibilities_dict[skill] = self.current_bot.get_attribute_real_value(
                    skill.base_attribute
                ) + skill.base

        if len(attack_possibilities_dict) < 1:
            self.current_play_style = IPlayingMode.DEFENSIVE
            return
        sorted_attack_possibilities_tuple = sorted(attack_possibilities_dict.items(), key=lambda x: x[1], reverse=True)
        best_attack = next(iter(sorted_attack_possibilities_tuple))[0]
        dice_result = self.game.roll_the_dice()

        if best_attack == 'attack':
            self.communicator.informer.event('attack')
            self.communicator.informer.dice_result(self.current_bot.name, dice_result, 'attack', self.game.dice_sides)

            targeted_defense = 'armour' if self.current_bot.job.damage_vector == 'strength' else 'magic_resist'

            damage = 0
            if self.current_bot.job.damage_vector == 'intelligence':
                damage = (self.current_bot.get_attribute_real_value(self.current_bot.job.damage_vector,
                                                                    self.current_bot.job.attack_type) / 2) + (
                                 dice_result / self.game.dice_sides) * 5
            elif self.current_bot.job.damage_vector == 'strength' and self.current_bot.job.attack_type == 'ranged':
                damage = self.current_bot.get_attribute_real_value(self.current_bot.job.damage_vector,
                                                                   self.current_bot.job.attack_type) \
                         + self.current_bot.get_attribute_real_value(
                    'accuracy') + (
                                 dice_result / self.game.dice_sides) * 5
            else:
                damage = self.current_bot.get_attribute_real_value(self.current_bot.job.damage_vector,
                                                                   self.current_bot.job.attack_type) + (
                                 dice_result / self.game.dice_sides) * 5

            damage = math.ceil(damage - self.possible_foe.get_attribute_real_value(targeted_defense))
            if damage > 0:
                self.possible_foe.suffer_damage(damage)
                self.communicator.informer.suffer_damage(self.current_bot, self.possible_foe, damage)
                experience = get_configuration(EXPERIENCE_EARNED_ACTION).get('attack', 0)
                self.current_bot.earn_xp(experience)
                self.communicator.informer.player_earned_xp(player_name=self.current_bot.name, xp=experience)

                if not self.possible_foe.is_alive():
                    experience = get_configuration(EXPERIENCE_EARNED_ACTION).get('kill', 0)
                    self.current_bot.earn_xp(experience)
                    self.communicator.informer.player_earned_xp(player_name=self.current_bot.name, xp=experience)
            else:
                self.communicator.informer.missed(self.current_bot, self.possible_foe)
            return
        elif isinstance(best_attack, ISkill):
            self.prepare_execute_skill(best_attack)
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
            self.game.game_map.move_player(self.current_bot, safest_place)
        if self.current_play_style == IPlayingMode.AGGRESSIVE:
            possible_foe = self.find_foes(possibilities)

            if possible_foe is None:
                aggressive_positions_map = self.game.game_map.graph. \
                    get_average_distances_sources_destinations_map(possibilities, remaining_players_positions)
                sorted_aggressive_positions_tuple = sorted(aggressive_positions_map.items(), key=lambda x: x[1],
                                                           reverse=False)
                best_place = next(iter(sorted_aggressive_positions_tuple))[0]
                self.game.game_map.move_player(self.current_bot, best_place)
            else:
                if self.current_bot.job.attack_type == 'melee':
                    self.game.game_map.move_player(self.current_bot, possible_foe.position)
                elif self.current_bot.job.attack_type == 'ranged':
                    attack_range = self.current_bot.get_ranged_attack_area()
                    aggressive_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
                        possible_foe.position,
                        attack_range)
                    best_position = random.choice(aggressive_possibilities)
                    self.game.game_map.move_player(self.current_bot, best_position)
                self.possible_foe = possible_foe
        if self.current_play_style == IPlayingMode.NEUTRAL:
            random_position = random.choice(possibilities)
            self.game.game_map.move_player(self.current_bot, random_position)
        self.communicator.informer.event('move')
        self.communicator.informer.moved(self.current_bot.name)

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
        low_life_level = self.current_bot.health_points * 0.3

        if self.current_bot.life > low_life_level:
            self.current_play_style = IPlayingMode.AGGRESSIVE
        elif self.current_bot.life < low_life_level and len(remaining_players) > 1:
            self.current_play_style = IPlayingMode.DEFENSIVE
        elif self.current_bot.life < low_life_level and len(remaining_players) == 1 and self.probability_of_damage(
                remaining_players[0]):
            self.current_play_style = IPlayingMode.AGGRESSIVE
        else:
            self.current_play_style = IPlayingMode.DEFENSIVE

    def decide(self, player: IPlayer) -> None:
        self.reset_attributes()
        self.current_bot = player
        self.sort_foes_by_priority()
        self.select_playing_mode()

        self.possible_foe = self.find_foes_within_damage_range()

        if self.current_play_style == IPlayingMode.AGGRESSIVE and \
                self.possible_foe is not None:
            self.attack()
            self.communicator.informer.force_loading(1)
            self.current_play_style = IPlayingMode.NEUTRAL
            self.move()
            self.communicator.informer.force_loading(1)
        elif self.current_play_style == IPlayingMode.AGGRESSIVE and \
                self.possible_foe is None:
            self.move()
            self.communicator.informer.force_loading(1)
            self.attack()
            self.communicator.informer.force_loading(1)
        else:
            self.move()
            self.communicator.informer.force_loading(1)
        if self.current_play_style == IPlayingMode.DEFENSIVE:
            self.decide_best_defensive_action()
            self.communicator.informer.force_loading(1)
        self.communicator.informer.event('search')
        self.search_on_map()
        self.communicator.informer.force_loading(1)
        self.equip_item()
