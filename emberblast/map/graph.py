import math
from typing import List, Set, Dict, Tuple, Union

from emberblast.utils import generate_random_adjacent_matrix, generate_visited_default_matrix, convert_number_to_letter, \
    convert_letter_to_number, is_square_matrix
from emberblast.interface import IGraph, IVertex, IEdge


class Edge(IEdge):
    def __init__(self, source: str, destination: str, weight: float) -> None:
        """
        Constructor of Edge

        :param str source: The source Vertex(Node) of that edge.
        :param str destination: The destination Vertex(Node) of that edge.
        :param float weight: The distance between source and destination, as matrix are based in squares,
        vertical/horizontal edges, will have a weight of 1. Diagonal, will be sqrt(2) * 1.
        :rtype: None.
        """
        self.source = source
        self.destination = destination
        self.weight = weight


class Vertex(IVertex):
    def __init__(self, vertex_id: str, value: int, position: dict) -> None:
        """
        Constructor of Vertex

        :param str vertex_id: The vertex ID, for example "A2" or "F3".
        :param int value: 1 for being a valid tile, or 0 to be a tile that players can not walk on.
        :param dict position: dict representing the row and column.
        :rtype: None.
        """
        self.vertex_id = vertex_id
        self.position = position
        self.edges: List[IEdge] = []
        self.value = value

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)


class Graph(IGraph):
    def __init__(self, graph_dict: dict = None, size: int = 5) -> None:
        """
        Constructor of Graph.

        The map it's based on a squared adjacent matrix, that it's converted into a Graph, where the value of the nodes
        are randomly picked, nodes with value 1, are valid nodes are players can walk, and 0 they can't.

        The representation of the map, for the sake of clearness, will have the rows represented by alphabet letters,
        and columns by numbers, like a chess board.

        So a map of size 3, will look like this one:
            1   2   3
        A   *   0   *
        B   *   *   *
        C   *   0   *

        :param dict graph_dict: The already mounted graph, it's none, or it can be a created one, in the case player,
        is continuing a saved game.
        :param int size: base size of the matrix, for example, if size = 4, matrix will be based on 4 x 4.
        :rtype: None.
        """
        if graph_dict is None:
            graph_dict = {}
        self.size = size
        self.graph_dict: Dict[str, Vertex] = graph_dict
        self.matrix = [[]]

    def init_graph(self, fixed_matrix: List[List[int]] = None) -> None:
        """
        Simple proxy function, that calls another functions responsible to build an adjacent matrix, and transform it
        into a graph.

        :rtype: None.
        """
        if fixed_matrix is not None:
            if is_square_matrix(fixed_matrix):
                self.matrix = fixed_matrix
                self.size = len(fixed_matrix)
        else:
            self.matrix = generate_random_adjacent_matrix(self.size)

        visited = generate_visited_default_matrix(self.size)
        self._create_matrix_dfs_traverse(self.matrix, 0, 0, visited)

    def _create_matrix_dfs_traverse(self, matrix: List[List[int]], row: int, column: int,
                                    visited: List[List[bool]]) -> None:
        """
        Private recursive method to create a matrix, using DFS preorder algorithm for traversing the matrix,
        and building each of the positions of it.

        It's a squared adjacent matrix, that will be converted into a graph, that represents the map. 0 vertexes means
        invalid nodes, where players can not walk on, and 1 are the valid ones.

        Also, it computes the edges between two valid nodes(vertexes), adopting a square logic, horizontal/vertical
        edges have a weight(distance) of 1, and diagonal is weighted based in sqrt(2) * 1, which is the square diagonal
        formula.

        :param List[List[int]] matrix: The squared list, that represents the matrix.
        :param int row: The current row that is being visited by the traversal recursive function.
        :param int column: The current column that is being visited by the traversal recursive function.
        :param List[List[int]] matrix: The squared array, that represents the matrix.
        :param List[List[bool]]: squared list that represents the nodes that have already been visited.
        :rtype: None.
        """
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

    def _compute_vertical_edges(self, vertex: IVertex, row: int, column: int, matrix: List[List[int]]) -> None:
        """
        Function that receives a vertex(node), and compute all the neighbour vertical edges, looking for valid
        edges.


        :param IVertex vertex: Current vertex to be analysed.
        :param int row: Current row where vertex is.
        :param int column: Current column where vertex is.
        :param List[List[int]] matrix: The entire matrix.
        :rtype: None.
        """
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

    def _compute_horizontal_edges(self, vertex: IVertex, row: int, column: int, matrix: List[List[int]]) -> None:
        """
        Function that receives a vertex(node), and compute all the neighbour horizontal edges, looking for valid
        edges.


        :param IVertex vertex: Current vertex to be analysed.
        :param int row: Current row where vertex is.
        :param int column: Current column where vertex is.
        :param List[List[int]] matrix: The entire matrix.
        :rtype: None.
        """
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

    def _compute_diagonal_edges(self, vertex: IVertex, row: int, column: int, matrix: List[List[int]]) -> None:
        """
        Function that receives a vertex(node), and compute all the neighbour diagonal edges, looking for valid
        edges.

        Remember that diagonal edges, are weighted as sqrt(2) * 1.


        :param IVertex vertex: Current vertex to be analysed.
        :param int row: Current row where vertex is.
        :param int column: Current column where vertex is.
        :param List[List[int]] matrix: The entire matrix.
        :rtype: None.
        """
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

    def get_list_of_nodes(self) -> List[str]:
        """
        Returns a list of the keys of the dictionary

        :rtype:  List[str]
        """
        return list(self.graph_dict.keys())

    def is_vertex_valid(self, row: int, column: int) -> bool:
        """
        Returns True if vertex exists, otherwise False.

        :param int row: Row of the vertex.
        :param int column: Column of the vertex.
        :rtype:  List[str]
        """
        letter = convert_number_to_letter(row)
        vertex = self.graph_dict.get(letter + str(column))
        return True if vertex.value == 1 else False

    def compute_recursive_range_edges(self, vertex: IVertex, reach: float, available_nodes: Set[str],
                                      origin_node: str) -> None:
        """
        This function traverses the map using a dijkstra logic, trying to find all the possibilities of paths to
        walk on, within a determined reach(distance).

        This function is recursive, because it checks all the possibilities of movement starting from one vertex
        considering a base distance. For example, starting from "A1" with a distance of 3, it will recursively find
        possibilities, and for each new recursive call, the distance will be decreased by 1 (horizontal/vertical)
        possibilities, and sqrt(2) * 1 (diagonal).

        :param IVertex vertex: The current vertex to be analysed.
        :param float reach: The distance to look for possibilities.
        :param Set[str] available_nodes: The list that will be recursively incremented will be found possibilities.
        :param str origin_node: The origin node. For example, "A1".
        :rtype: None
        """
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
        """
        Get all the possibilities of nodes to walk, starting from one.
        It will get the help of compute_recursive_range_edges function, to look for
        all the possibilities.

        This function is called whenever a player wants to walk within the map, where the
        radius can be represented as the character's move speed.

        :param str position: The starting position, for example "A1".
        :param int radius: The radius(max distance) to look for possibilities.
        :rtype: List[str]
        """
        start_vertex = self.graph_dict.get(position)
        available_nodes_set = set()
        self.compute_recursive_range_edges(start_vertex, radius, available_nodes_set, position)
        available_nodes_list = list(available_nodes_set)

        if position in available_nodes_list:
            available_nodes_list.remove(position)
        return available_nodes_list

    def is_target_in_range(self, position: str, radius: int, target_position: str) -> bool:
        available_nodes = self.get_available_nodes_in_range(position, radius)
        if target_position in available_nodes:
            return True
        return False

    def get_number_of_walkable_nodes(self) -> int:
        """
        Get the number of the walkable(valid) nodes of the map.

        :rtype: int
        """
        return len([x for x in filter(lambda vertex: vertex.value == 1, list(self.graph_dict.values()))])

    def is_graph_defective(self) -> bool:
        """
        Whether the graph is defective or not. A map is considered not defective, when starting from a valid(walkable)
        node, all another walkable nodes can be reached. But in the case when a valid node, can't reach another node,
        regardless the distance, is can say that there are "islands" on the map, where players could not access another
        areas of the map.

        :rtype: Dict[str, IVertex]
        """
        walkable_nodes = self.get_walkable_nodes()
        for key in walkable_nodes.keys():
            distances = self.get_shortest_path(key)
            for value in distances.values():
                if value == math.inf:
                    return True
        return False

    def get_walkable_nodes(self) -> Dict[str, IVertex]:
        """
        Get the dictionary of only the valid nodes(vertexes).

        :rtype: Dict[str, IVertex]
        """
        return {k: v for (k, v) in self.graph_dict.items() if v.value == 1}

    def fill_infinite_distance_dict(self, distances: Dict[str, float]) -> None:
        """
        When performing Dijkstra algorithm, in a first step all the distances to possible vertexes needs to be set
        to infinite.

        :param  Dict[str, float] distances: The dictionary of the distances between source vertex and another vertexes.
        :rtype: None
        """
        for key in self.get_walkable_nodes().keys():
            distances[key] = math.inf

    def get_average_distances_sources_destinations_map(self, sources: List[str],
                                                       positions: List[str]) -> Dict[str, float]:
        averages_map = {}
        for source in sources:
            average_distance = self.get_average_distance_source_destinations(source,
                                                                             positions)
            averages_map[source] = average_distance

        return averages_map

    def get_average_distance_source_destinations(self, source: str, positions: List[str]) -> float:
        distances = self.get_shortest_path(source)
        total_distance = 0

        for position in positions:
            total_distance = total_distance + distances.get(position, 0)

        return total_distance / len(positions)

    def get_shortest_distance_between_positions(self, s1: str, s2: str) -> float:
        distances = self.get_shortest_path(s1)
        return distances.get(s2, 0)

    def get_shortest_path(self, source_position: str) -> Dict[str, float]:
        """
        Core method for Dijkstra algorithm, for getting each of the distances, and finding the shortest path to all
        the another available vertex in the map, starting from a source vertex.

        Dijkstra strategy works on presuming that you don't know all the distances to all the possible destinations,
        setting them to infinite, and start filling up them, and adding only the ones are lesser than the existing
        one.

        :param  str source_position: The source vertex to start it.
        :rtype: None
        """
        distances = {source_position: 0}
        self.fill_infinite_distance_dict(distances)
        distances[source_position] = 0
        starting_node = self.graph_dict.get(source_position)
        unsettled_nodes: List[IVertex] = [starting_node]
        settled_nodes: List[IVertex] = []

        while len(unsettled_nodes) != 0:
            current = unsettled_nodes.pop(0)

            for edge in current.edges:
                neighbour_vertex = self.graph_dict.get(edge.destination)
                self.compute_distance(current, neighbour_vertex, edge.weight, distances)
                if neighbour_vertex not in settled_nodes:
                    unsettled_nodes.append(neighbour_vertex)
            settled_nodes.append(current)
        return distances

    @staticmethod
    def compute_distance(source_vertex: IVertex, destination_vertex: IVertex, edge_weight: float,
                         distances: Dict[str, float]) -> None:
        """
        Check if the current measured edge weight it's lesser that the distance that already exists in the distances
        dictionary to the destination vertex. In the case it's smaller, it will replace the existing value.

        :param  IVertex source_vertex: The source vertex to start it.
        :param  IVertex destination_vertex: Destination vertex.
        :param  float edge_weight: The edge weight.
        :param  Dict[str, float] distances: The dictionaries of distances.
        :rtype: None
        """
        computed_distance = distances.get(source_vertex.vertex_id) + edge_weight
        if computed_distance < distances[destination_vertex.vertex_id]:
            distances[destination_vertex.vertex_id] = computed_distance
