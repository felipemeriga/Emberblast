from project.utils.utils import generate_random_adjacent_matrix, generate_visited_default_matrix


class Edge:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.weight = 1


class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class Graph:
    def __init__(self, graph_dict=None, size=5):
        if graph_dict is None:
            graph_dict = {}
        self.size = size
        self.graph_dict = graph_dict
        self.matrix = [[]]

    def _add_to_graph(self, vertex_id, source, destination):
        if vertex_id not in self.graph_dict:
            self.graph_dict[vertex_id] = []
        edge = Edge(source, destination)
        self.graph_dict[vertex_id].append(edge)

    def init_graph(self):
        visited = generate_visited_default_matrix(self.size)
        self.matrix = generate_random_adjacent_matrix(self.size)
        self._dfs_traverse(self.matrix, 0, 0, visited)

    def _dfs_traverse(self, matrix, row, column, visited):
        if row >= self.size or column >= self.size or visited[row][column]:
            return
        visited[row][column] = True
        if matrix[row][column] == 1 and row != column:
            self._add_to_graph(row, row, column)

        self._dfs_traverse(matrix, row + 1, column, visited)
        self._dfs_traverse(matrix, row, column + 1, visited)
