import math
import random
from typing import Callable

from .test import BaseTestCase
from emberblast.map import Map, Graph
from emberblast.utils import convert_number_to_letter


def mock_defective_map() -> Callable:
    def wrapper(func):
        size = random.randint(3, 10)
        matrix = [[1, 1, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]
        defective_new_map = Map(name='test_map', map_type='test', size=size)
        defective_new_map.graph.init_graph(matrix)
        setattr(func, 'mock_defective_map', defective_new_map)
        return func

    return wrapper


def mock_map() -> Callable:
    def wrapper(func):
        size = random.randint(3, 10)
        new_map = Map(name='test_map', map_type='test', size=size)
        new_map.graph.init_graph()
        setattr(func, 'mock_map', new_map)
        return func

    return wrapper


@mock_map()
@mock_defective_map()
class TestModuleMap(BaseTestCase):
    def test_graph_generation(self) -> None:
        size = random.randint(1, 10)
        new_graph = Graph(size=size)
        new_graph.init_graph()

        self.assertEqual(len(new_graph.matrix), size)
        self.assertEqual(len(new_graph.matrix[0]), size)

        for i in range(0, size):
            for j in range(0, size):
                current_row = convert_number_to_letter(i)
                current_column = j
                position = current_row + str(current_column)
                self.assertIn(position, new_graph.graph_dict)
                map_value = new_graph.graph_dict.get(position)
                self.assertEqual(current_row, map_value.position.get('row'))
                self.assertEqual(current_column, map_value.position.get('column'))
                self.assertEqual(position, map_value.vertex_id)

    def test_map_attributes(self) -> None:
        size = random.randint(0, 10)
        new_map = Map(name='test_map', map_type='test', size=size)

    def test_get_shortest_path(self) -> None:
        walkable_nodes = self.mock_map.graph.get_walkable_nodes()
        key_list = list(walkable_nodes.keys())
        source = walkable_nodes[key_list[0]]

        distance = self.mock_map.graph.get_shortest_path(source.vertex_id)

    def test_infinite_shortest_path(self) -> None:
        walkable_nodes = self.mock_defective_map.graph.get_walkable_nodes()
        source = walkable_nodes['A0']

        distances = self.mock_defective_map.graph.get_shortest_path(source.vertex_id)
        for value in distances.values():
            if value is math.inf:
                return
        else:
            self.fail('As this is a defective map, at least one of the distances should be infinite. ')

    def test_defective_map(self) -> None:
        if not self.mock_defective_map.graph.is_graph_defective():
            self.fail(
                'A defective map was used in the validation, the validation should return that this map is defective. ')

    def test_get_average_distance_source_destinations(self) -> None:
        walkable_nodes = self.mock_map.graph.get_walkable_nodes()
        key_list = list(walkable_nodes.keys())
        source = walkable_nodes[key_list[0]]

        destinations = random.sample([x for x in key_list if x != source.vertex_id], 3)

        average = self.mock_map.graph.get_average_distance_source_destinations(source.vertex_id, destinations)
