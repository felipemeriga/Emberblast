from typing import List, Tuple, Set, Dict

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

    def is_vertex_valid(self, row: int, column: int) -> bool:
        letter = convert_number_to_letter(row)
        vertex = self.graph_dict.get(letter + str(column))
        return True if vertex.value == 1 else False

    def compute_recursive_range_edges(self, vertex: Vertex, reach: float, available_nodes: Set[str], origin_node: str):
        for edge in vertex.edges:
            if reach >= edge.weight:
                if edge.destination == origin_node:
                    continue
                remaining_reach = reach - edge.weight
                reached_vertex = self.graph_dict.get(edge.destination)
                available_nodes.add(reached_vertex.vertex_id)
                if remaining_reach >= 1:
                    self.compute_recursive_range_edges(reached_vertex, remaining_reach,
                                                       available_nodes, vertex.vertex_id)
        return

    def get_available_nodes_in_range(self, position: str, radius: int) -> List[str]:
        start_vertex = self.graph_dict.get(position)
        available_nodes_set = set()
        self.compute_recursive_range_edges(start_vertex, radius, available_nodes_set, position)
        available_nodes_list = list(available_nodes_set)

        if position in available_nodes_list:
            available_nodes_list.remove(position)
        return available_nodes_list

    def get_number_of_walkable_nodes(self) -> int:
        return len([x for x in filter(lambda vertex: vertex.value == 1, list(self.graph_dict.values()))])

    def get_walkable_nodes(self) -> Dict[str, Vertex]:
        return {k: v for (k, v) in self.graph_dict.items() if v.value == 1}
