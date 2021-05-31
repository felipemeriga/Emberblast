from .graph import Graph


class Map:

    def __init__(self, name: str, map_type: str, size: int) -> None:
        self.name = name
        self.type = map_type
        self.size = size
        self.graph = Graph(size=size)


class MapFactory:
    def create_map(self, map_size: int) -> Map:
        game_map = Map('test', 'wind', map_size)
        game_map.graph.init_graph()
        return game_map
