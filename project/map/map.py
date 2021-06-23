import random
from math import floor
from typing import List, Dict

from .graph import Graph
from project.player import Player
from project.utils import convert_number_to_letter
from ..conf import get_configuration
from ..item import Item, get_random_item


class Map:

    def __init__(self, name: str, map_type: str, size: int) -> None:
        self.name = name
        self.type = map_type
        self.size = size
        self.graph = Graph(size=size)
        self.items: Dict[str, Item] = {}

    def define_player_initial_position_random(self, players: List[Player]) -> None:
        selected_positions = []

        for player in players:
            position = self.pick_available_position(selected_positions)
            player.set_position(position)
            selected_positions.append(position)

    def pick_available_position(self, selected_positions: List[str]) -> str:
        while True:
            row = random.randint(0, self.size - 1)
            column = random.randint(0, self.size - 1)
            vertex_valid = self.graph.is_vertex_valid(row, column)

            position = convert_number_to_letter(row) + str(column)
            if vertex_valid and position not in selected_positions:
                return position

    """
    Function to coordinate distribution of random items in the map
    
    The items will be placed in the half of the quantity of the walkable nodes in the map, and with the
    probabilities for each tier of item configured in the conf file, the quantity for each tier will be determined,
    and finally a random items will be picked for the respective quantities of each tier, and placed in some random 
    places.

    :rtype: None
    """

    def distribute_random_items(self) -> None:
        walkable_nodes = self.graph.get_walkable_nodes()

        number_of_walkable_nodes = len(walkable_nodes)
        number_of_items = floor(number_of_walkable_nodes / 2)
        probabilities = get_configuration('item_probabilities')
        common_items_number = round(number_of_items * probabilities.get('common', 0.6))
        uncommon_items_number = round(number_of_items * probabilities.get('uncommon', 0.2))
        rare_items_number = round(number_of_items * probabilities.get('rare', 0.15))
        legendary_items_number = round(number_of_items * probabilities.get('legendary', 0.05))
        item_type_distribution = {'common': ['healing'] * 45 + ['equipment'] * 30 + ['recovery'] * 25,
                                  'uncommon': ['healing'] * 50 + ['equipment'] * 50,
                                  'rare': ['healing'] * 20 + ['equipment'] * 80,
                                  'legendary': ['equipment'] * 80}

        for i in range(common_items_number + uncommon_items_number + rare_items_number + legendary_items_number):
            key = random.choice(list(walkable_nodes.keys()))
            node = walkable_nodes.get(key)
            walkable_nodes.pop(key)
            tier = ''
            if common_items_number > 0:
                tier = 'common'
                common_items_number = common_items_number - 1
            elif uncommon_items_number > 0:
                tier = 'uncommon'
                uncommon_items_number = uncommon_items_number - 1
            elif rare_items_number > 0:
                tier = 'rare'
                rare_items_number = rare_items_number - 1
                choices = ['item'] * 25 + ['equipment'] * 75
                item_type = random.choice(choices)
            elif legendary_items_number > 0:
                tier = 'legendary'
                legendary_items_number = legendary_items_number - 1
                item_type = 'equipment'

            item_type = random.choice(item_type_distribution.get(tier))
            item = get_random_item(tier, item_type)
            self.items[key] = item


class MapFactory:
    def create_map(self, map_size: int) -> Map:
        game_map = Map('test', 'wind', map_size)
        game_map.graph.init_graph()
        return game_map
