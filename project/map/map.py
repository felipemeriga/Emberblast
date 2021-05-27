from .graph import Graph


class Map:

    def __init__(self, name, map_type, size):
        self.name = name
        self.type = map_type
        self.size = size
        self.graph = Graph(size=size)


class MapFactory:
    def create_map(self):
        game_map = Map('test', 'wind', 3)
        game_map.graph.init_graph()
        return game_map
