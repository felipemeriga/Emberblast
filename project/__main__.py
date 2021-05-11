import sys

import timg

from project.map.map import MapFactory


def run_project(args):
    print('Running project')
    obj = timg.Renderer()
    obj.load_image_from_file('./img/emberblast.png')
    obj.resize(100, 100)
    obj.render(timg.ASCIIMethod)
    # map_factory = MapFactory()
    # game_map = map_factory.create_map()



if __name__ == '__main__':
    run_project(sys.argv)
