from typing import List, Tuple

from termcolor import colored

from project.player import Player
from project.utils import generate_random_adjacent_matrix, generate_visited_default_matrix, convert_number_to_letter


class Edge:
    def __init__(self, source: str, destination: str, weight: float) -> None:
        self.source = source
        self.destination = destination
        self.weight = weight


class Vertex:
    def __init__(self, vertex_id: str, value: int, position: dict) -> None:
        self.vertex_id = vertex_id
        self.position = position
        self.edges = []
        self.value = value

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)


class Graph:
    def __init__(self, graph_dict: dict = None, size: int = 5) -> None:
        if graph_dict is None:
            graph_dict = {}
        self.size = size
        self.graph_dict = graph_dict
        self.matrix = [[]]

    def init_graph(self) -> None:
        visited = generate_visited_default_matrix(self.size)
        self.matrix = generate_random_adjacent_matrix(self.size)
        self._create_matrix_dfs_traverse(self.matrix, 0, 0, visited)

    def _create_matrix_dfs_traverse(self, matrix: List[List[int]], row: int, column: int, visited: List[List[bool]]):
        if row >= self.size or column >= self.size or visited[row][column]:
            return
        visited[row][column] = True
        letter_row = convert_number_to_letter(row)
        vertex_id = letter_row + str(column)
        position = {
            'row': letter_row,
            'column': column
        }
        vertex = Vertex(vertex_id, matrix[row][column], position)
        if vertex.value == 1:
            self._compute_vertical_edges(vertex, row, column, matrix)
            self._compute_horizontal_edges(vertex, row, column, matrix)
            self._compute_diagonal_edges(vertex, row, column, matrix)
        self.graph_dict[vertex_id] = vertex

        self._create_matrix_dfs_traverse(matrix, row + 1, column, visited)
        self._create_matrix_dfs_traverse(matrix, row, column + 1, visited)

    def _compute_vertical_edges(self, vertex: Vertex, row: int, column: int, matrix: List[List[int]]):
        # upper edge
        if row - 1 >= 0:
            if matrix[row - 1][column] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row - 1) + str(column), 1)
                vertex.add_edge(edge)
        # lower
        if row + 1 < self.size:
            if matrix[row + 1][column] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row + 1) + str(column), 1)
                vertex.add_edge(edge)

    def _compute_horizontal_edges(self, vertex: Vertex, row: int, column: int, matrix: List[List[int]]):
        # left edge
        if column - 1 >= 0:
            if matrix[row][column - 1] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row) + str(column - 1), 1)
                vertex.add_edge(edge)
        # right edge
        if column + 1 < self.size:
            if matrix[row][column + 1] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row) + str(column + 1), 1)
                vertex.add_edge(edge)

    def _compute_diagonal_edges(self, vertex: Vertex, row: int, column: int, matrix: List[List[int]]):
        if column - 1 >= 0 and row - 1 >= 0:
            if matrix[row - 1][column - 1] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row - 1) + str(column - 1), 1.414)
                vertex.add_edge(edge)
        if column + 1 < self.size and row + 1 < self.size:
            if matrix[row + 1][column + 1] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row + 1) + str(column + 1), 1.414)
                vertex.add_edge(edge)

        if column - 1 >= 0 and row + 1 < self.size:
            if matrix[row + 1][column - 1] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row + 1) + str(column - 1), 1.414)
                vertex.add_edge(edge)

        if row - 1 >= 0 and column + 1 < self.size:
            if matrix[row - 1][column + 1] == 1:
                edge = Edge(vertex.vertex_id, convert_number_to_letter(row - 1) + str(column + 1), 1.414)
                vertex.add_edge(edge)

    def get_edges_as_array_of_tuples(self) -> List[Tuple[int, int]]:
        edges = []
        for value in self.graph_dict.values():
            for edge in value:
                edges.append((edge.source, edge.destination))
        return edges

    def get_list_of_nodes(self) -> List[int]:
        return list(self.graph_dict.keys())

    def print_map_info(self, player: Player, players: List[Player]) -> None:
        foes_positions = []
        print(colored('{name} is currently at position: {position}, '
                      'with {health_points} HP'.format(name=player.name,
                                                       position=player.position,
                                                       health_points=player.health_points),
                      'green'))

        for opponent in players:
            foes_positions.append(opponent.position)
            print(colored('Enemy {name}({job}) is currently at position: {position}, '
                          'with {health_points} HP'.format(name=opponent.name,
                                                           job=opponent.job.get_name(),
                                                           position=opponent.position,
                                                           health_points=opponent.health_points),
                          'red'))

        print(' ' * 4, end="")
        for column in range(self.size):
            print('{:4}'.format(column), end="")
        print('\n')
        for row in range(self.size):
            print('{:7}'.format(convert_number_to_letter(row)), end="")
            for column in range(self.size):
                color = 'white'
                attrs = ['bold']
                position = convert_number_to_letter(row) + str(column)

                if player.position == position:
                    color = 'green'
                    attrs.append('blink')
                elif position in foes_positions:
                    color = 'red'
                print(colored('{:4}'.format('*' if self.matrix[row][column] == 1 else ' '), color, attrs=attrs), end="")
            print('')

    def is_vertex_valid(self, row: int, column: int) -> bool:
        letter = convert_number_to_letter(row)
        vertex = self.graph_dict.get(letter + str(column))
        return True if vertex.value == 1 else False
