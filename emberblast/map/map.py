import random
from math import floor
from typing import List, Dict, Optional

from .graph import Graph
from emberblast.utils import convert_number_to_letter
from emberblast.conf import get_configuration
from emberblast.item import get_random_item
from emberblast.interface import IPlayer, IItem, IMap, ISideEffect


class Map(IMap):

    def __init__(self, name: str, map_type: str, size: int) -> None:
        """
        Pick a random postion for a player in the game start.

        :param str name: The name of the map.
        :param str map_type: The type of the terrain of the map.
        :param int size: The size of the map, used to construct the graph.
        :rtype: None.
        """
        self.name = name
        self.type = map_type
        self.size = size
        self.graph = Graph(size=size)
        self.items: Dict[str, List[IItem]] = {}
        self.traps: Dict[str, List[ISideEffect]] = {}

    def define_player_initial_position_random(self, players: List[IPlayer]) -> None:
        """
        Pick a random postion for a player in the game start.

        :param List[IPlayer] players: The available positions to scan.
        :rtype: str.
        """
        selected_positions = []

        for player in players:
            position = self.pick_available_position(selected_positions)
            player.set_position(position)
            selected_positions.append(position)

    def pick_available_position(self, selected_positions: List[str]) -> str:
        """
        Function that will be called on game construction, to place players randomly in the map,
        considering that player can't start in a tile that there is already another player.

        :param List[str] selected_positions: The available positions to scan.
        :rtype: str.
        """
        while True:
            row = random.randint(0, self.size - 1)
            column = random.randint(0, self.size - 1)
            vertex_valid = self.graph.is_vertex_valid(row, column)

            position = convert_number_to_letter(row) + str(column)
            if vertex_valid and position not in selected_positions:
                return position

    def get_traps_from_position(self, position: str) -> List[ISideEffect]:
        """
        Checks if a position of the map, contains hidden traps, and return all the
        side-effects of the traps.

        :param str position: The position to check for hidden traps.
        :rtype: List[ISideEffect]
        """
        if self.traps.get(position, None):
            side_effects = self.traps.get(position)
            self.traps[position] = []
            return side_effects
        else:
            return []

    def move_player(self, player: IPlayer, destination: str) -> None:
        """
        Function to move players along the map, and check if some positions have hidden traps.

        :param IPlayer player: The player that is currently moving.
        :param str destination: The destination where player is going.
        :rtype: None
        """
        traps = self.get_traps_from_position(destination)
        # TODO - MOVE this validation to orchestrator, so we can use communicator to let players know
        if len(traps) > 0:
            for side_effect in traps:
                player.add_side_effect(side_effect)
        player.set_position(destination)

    def distribute_random_items(self) -> None:
        """
        Function to coordinate distribution of random items in the map

        The items will be placed in the half of the quantity of the walkable nodes in the map, and with the
        probabilities for each tier of item configured in the conf file, the quantity for each tier will be determined,
        and finally a random items will be picked for the respective quantities of each tier, and placed in some random
        places.

        :rtype: None
        """
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
            elif legendary_items_number > 0:
                tier = 'legendary'
                legendary_items_number = legendary_items_number - 1

            item_type = random.choice(item_type_distribution.get(tier))
            item = get_random_item(tier, item_type)
            self.add_item_to_map(key, item)

    def check_item_in_position(self, position: str) -> Optional[List[IItem]]:
        """
        Function to be used by Search action, to discover if player current position has an Item

        :param str position: A string with the current position of the player. For example: "A2" or "C4".
        :rtype: Optional[IItem]: The item if it exists or None.
        """
        items = self.items.get(position, None)
        if items is not None:
            self.items.pop(position, None)
        return items

    def add_item_to_map(self, position: str, item: IItem) -> None:
        """
        Add an item to map, this method may be called in game creation, when items are distributed randomly,
        or when a character drops an item.

        :param str position: The position of the map, like "A2" or "C4" where item will be added.
        :param IItem item: Item object that will be added.

        :rtype: None.
        """
        if self.items.get(position, None):
            self.items.get(position).append(item)
        else:
            self.items[position] = [item]

    def add_trap_to_map(self, position: str, side_effects: List[ISideEffect]) -> None:
        """
        Add a trap to map, usually thieves are the ones that are specialized on that kind of job.

        :param str position: The position of the map, like "A2" or "C4" where the trap will be added.
        :param List[ISideEffect] side_effects: Side effects list.

        :rtype: None.
        """
        if self.traps.get(position, None):
            self.traps.get(position).extend(side_effects)
        else:
            self.traps[position] = side_effects


class MapFactory:
    def create_map(self, map_size: int) -> IMap:
        """
        Factory design pattern to create a new map.

        :param int map_size: The size of the map, it will be expressed as the number of tiles of a matrix,
        For example, size = 5, the map will be based on a 5 x 5 matrix.

        :rtype: Map.
        """
        game_map = Map('test', 'wind', map_size)
        invalid_map = True

        while invalid_map:
            game_map.graph.init_graph()
            invalid_map = game_map.graph.is_graph_defective()

        return game_map
