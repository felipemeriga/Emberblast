import random
from typing import Callable

from .test import BaseTestCase
from project.map import Map, Graph
from project.utils import convert_number_to_letter
from project.message import print_plain_matrix


def mock_map() -> Callable:
    def wrapper(func):
        size = random.randint(3, 10)
        new_map = Map(name='test_map', map_type='test', size=size)
        new_map.graph.init_graph()
        setattr(func, 'mock_map', new_map)
        return func

    return wrapper


@mock_map()
class TestModuleMap(BaseTestCase):
    def test_graph_generation(self) -> None:
        size = random.randint(0, 10)
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

        print_plain_matrix(self.mock_map.graph.matrix)
        distance = self.mock_map.graph.get_shortest_path(source.vertex_id)

    def test_get_average_distance_source_destinations(self) -> None:
        walkable_nodes = self.mock_map.graph.get_walkable_nodes()
        key_list = list(walkable_nodes.keys())
        source = walkable_nodes[key_list[0]]

        destinations = random.sample([x for x in key_list if x != source.vertex_id], 3)

        print_plain_matrix(self.mock_map.graph.matrix)
        average = self.mock_map.graph.get_average_distance_source_destinations(source.vertex_id, destinations)
