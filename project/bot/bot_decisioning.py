import collections
import random
from typing import Dict, List, Optional

from project.interface import IBotDecisioning, IGame, IAction, IPlayer, IPlayingMode


class BotDecisioning(IBotDecisioning):

    def __init__(self, game: IGame) -> None:
        self.game = game
        self.current_bot = None
        self.current_play_style = IPlayingMode.NEUTRAL
        self.prioritized_foes = []

    def get_remaining_players_position(self) -> List[str]:
        remaining_players = self.game.get_remaining_players(self.current_bot)
        return [x for x in map(lambda player: player.position, remaining_players)]

    def find_foes(self, movement_possibilities: List[str]) -> Optional[IPlayer]:
        possible_foe = None
        attack_range = self.current_bot.get_ranged_attack_area()
        attack_range_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
            self.current_bot.position,
            attack_range)

        for foe in self.prioritized_foes:
            if foe.position in movement_possibilities or foe.position in attack_range_possibilities:
                possible_foe = foe
                break
        return possible_foe

    def sort_foes_by_priority(self) -> None:
        remaining_players = self.game.get_remaining_players(self.current_bot)
        priorities_map = {}
        for player in remaining_players:
            distance = self.game.game_map.graph.get_shortest_distance_between_positions(self.current_bot.position,
                                                                                        player.position)
            priority = distance + player.life

            # We need to use player as the key, because players may have the same name, and priority, using objects
            # address will never fall into that case.
            priorities_map[player] = priority

        self.prioritized_foes = list(
            collections.OrderedDict(sorted(priorities_map.items(), key=lambda item: item[1])).keys())

    def attack(self) -> None:
        pass

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

        pass

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

    def decide(self, player: IPlayer, actions_left: Dict[str, IAction]) -> None:
        actions_calls = []
        self.current_bot = player
        self.sort_foes_by_priority()
        self.select_playing_mode()

        if self.current_play_style == IPlayingMode.AGGRESSIVE and \
                self.prioritized_foes[0].position == self.current_bot.position:
            self.attack()
            self.move()
        else:
            self.move()
            self.attack()

