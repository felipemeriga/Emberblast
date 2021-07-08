from typing import List, Set, Dict

from project.utils import generate_random_adjacent_matrix, generate_visited_default_matrix, convert_number_to_letter


class Edge:
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


class Vertex:
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
        self.edges = []
        self.value = value

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)


class Graph:
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

    def init_graph(self) -> None:
        """
        Simple proxy function, that calls another functions responsible to build an adjacent matrix, and transform it
        into a graph.

        :rtype: None.
        """
        visited = generate_visited_default_matrix(self.size)
        self.matrix = generate_random_adjacent_matrix(self.size)
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

    def _compute_vertical_edges(self, vertex: Vertex, row: int, column: int, matrix: List[List[int]]) -> None:
        """
        Function that receives a vertex(node), and compute all the neighbour vertical edges, looking for valid
        edges.


        :param Vertex vertex: Current vertex to be analysed.
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

    def _compute_horizontal_edges(self, vertex: Vertex, row: int, column: int, matrix: List[List[int]]) -> None:
        """
        Function that receives a vertex(node), and compute all the neighbour horizontal edges, looking for valid
        edges.


        :param Vertex vertex: Current vertex to be analysed.
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

    def _compute_diagonal_edges(self, vertex: Vertex, row: int, column: int, matrix: List[List[int]]) -> None:
        """
        Function that receives a vertex(node), and compute all the neighbour diagonal edges, looking for valid
        edges.

        Remember that diagonal edges, are weighted as sqrt(2) * 1.


        :param Vertex vertex: Current vertex to be analysed.
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

    def compute_recursive_range_edges(self, vertex: Vertex, reach: float, available_nodes: Set[str],
                                      origin_node: str) -> None:
        """
        This function traverses the map using a dijkstra logic, trying to find all the possibilities of paths to
        walk on, within a determined reach(distance).

        This function is recursive, because it checks all the possibilities of movement starting from one vertex
        considering a base distance. For example, starting from "A1" with a distance of 3, it will recursively find
        possibilities, and for each new recursive call, the distance will be decreased by 1 (horizontal/vertical)
        possibilities, and sqrt(2) * 1 (diagonal).

        :param Vertex vertex: The current vertex to be analysed.
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

    def get_number_of_walkable_nodes(self) -> int:
        """
        Get the number of the walkable(valid) nodes of the map.

        :rtype: int
        """
        return len([x for x in filter(lambda vertex: vertex.value == 1, list(self.graph_dict.values()))])

    def get_walkable_nodes(self) -> Dict[str, Vertex]:
        """
        Get the dictionary of only the valid nodes(vertexes).

        :rtype: int
        """
        return {k: v for (k, v) in self.graph_dict.items() if v.value == 1}
