import random
from typing import List

from .graph import Graph
from ..player import Player
from ..utils import convert_number_to_letter


class Map:

    def __init__(self, name: str, map_type: str, size: int) -> None:
        self.name = name
        self.type = map_type
        self.size = size
        self.graph = Graph(size=size)

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


class MapFactory:
    def create_map(self, map_size: int) -> Map:
        game_map = Map('test', 'wind', map_size)
        game_map.graph.init_graph()
        return game_map
