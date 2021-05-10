import sys
from project.map.map import MapFactory


def run_project(args):
    print('Running project')
    map_factory = MapFactory()
    game_map = map_factory.create_map()



if __name__ == '__main__':
    run_project(sys.argv)
