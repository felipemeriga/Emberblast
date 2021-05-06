class Edge:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def add_to_vertex(self, vertex_id):
        self.graph_dict[vertex_id] = Vertex(vertex_id)

    def append_edge_to_vertex(self, vertex_id, source, destination):
        edge = Edge(source, destination)
        self.graph_dict.get(vertex_id).append(edge)

