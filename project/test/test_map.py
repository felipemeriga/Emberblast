import random
from .test import BaseTestCase
from project.map import Map, Graph
from project.utils import convert_number_to_letter


class TestModuleMap(BaseTestCase):
    def test_module(self):
        self.test_graph_generation()
        self.test_map_attributes()

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
