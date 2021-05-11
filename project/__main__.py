import sys
import yaml
from project.game.game import GameFactory
from project.utils.utils import print_greetings, get_project_root


class LittleMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        super_class = superclasses[0]
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        return type.__new__(cls, clsname, superclasses, attributedict)

    def __init__(self, clsname, superclasses, attributedict):
        super_class = superclasses[0]
        a_yaml_file = open(str(get_project_root()) + '/conf.yaml')
        parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
        class_attributes = parsed_yaml_file.get('classes')
        super_class.__init__(self, 'ae')

class S:
    def __init__(self, string):
        self.test = 12


class A(S, metaclass=LittleMeta):

    def __init__(self):
        pass

def run_project(args):
    print_greetings()
    game = GameFactory()
    game.new_game()


if __name__ == '__main__':
    # run_project(sys.argv)
    a = A()



