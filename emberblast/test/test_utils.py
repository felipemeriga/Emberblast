import random
from .test import BaseTestCase
from typing import Dict

from emberblast.utils import generate_random_adjacent_matrix, generate_visited_default_matrix, find_key_recursively, \
    convert_letter_to_number, convert_number_to_letter, deep_get
from emberblast.utils.name_generator import generate_name


class TestModuleUtils(BaseTestCase):
    def test_module(self):
        self.test_generate_random_adjacent_matrix()
        self.test_generate_visited_default_matrix()
        self.test_find_key_recursively()
        self.test_deep_get()
        self.test_convert_letter_to_number()
        self.test_convert_number_to_letter()
        self.test_generate_name()

    @staticmethod
    def get_mock_dict() -> Dict:
        return {
            'root': {
                'nested1': {
                    'nested2': {
                        'nested3': {
                            'nested4': {
                                'nested5': 'found'
                            }
                        }
                    }
                }
            }
        }

    def test_generate_random_adjacent_matrix(self) -> None:
        a = random.randint(1, 10)
        matrix = generate_random_adjacent_matrix(a)
        # Asserting that the generated matrix it's square and from the same input size
        self.assertEqual(len(matrix), a)
        self.assertEqual(len(matrix[0]), a)

    def test_generate_visited_default_matrix(self) -> None:
        a = random.randint(1, 10)
        matrix = generate_visited_default_matrix(a)
        # Asserting that the generated matrix it's square and from the same input size
        self.assertEqual(len(matrix), a)
        self.assertEqual(len(matrix[0]), a)

    def test_find_key_recursively(self) -> None:
        mock_dict = self.get_mock_dict()
        result = find_key_recursively(mock_dict, 'nested5')
        self.assertEqual(result, 'found')

    def test_deep_get(self) -> None:
        mock_dict = self.get_mock_dict()
        result = deep_get(mock_dict, 'root', 'nested1', 'nested2', 'nested3', 'nested4', 'nested5')
        self.assertEqual(result, 'found')

    def test_convert_letter_to_number(self) -> None:
        self.assertEqual(convert_letter_to_number('A'), 0)
        self.assertEqual(convert_letter_to_number('B'), 1)
        self.assertEqual(convert_letter_to_number('H'), 7)
        self.assertEqual(convert_letter_to_number('K'), 10)
        self.assertEqual(convert_letter_to_number('N'), 13)
        self.assertEqual(convert_letter_to_number('N'), 13)
        self.assertEqual(convert_letter_to_number('R'), 17)
        self.assertEqual(convert_letter_to_number('R'), 17)
        self.assertEqual(convert_letter_to_number('W'), 22)
        self.assertEqual(convert_letter_to_number('Y'), 24)

    def test_convert_number_to_letter(self) -> None:
        self.assertEqual(convert_number_to_letter(0), 'A')
        self.assertEqual(convert_number_to_letter(1), 'B')
        self.assertEqual(convert_number_to_letter(17), 'R')
        self.assertEqual(convert_number_to_letter(25), 'Z')

    def test_generate_name(self) -> None:
        generated_name = generate_name()
        self.assertGreater(len(generated_name), 0)
        # making sure the random generated name has a first and a last name
        self.assertGreater(len(generated_name.split(' ')), 1)
