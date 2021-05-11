import random
import emoji
import timg
from colorama import Fore
from pathlib import Path
from project.utils.constants import ROOT_DIR

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def print_greetings():
    obj = timg.Renderer()
    project_path = get_project_root()
    obj.load_image_from_file(str(project_path) + '/img/emberblast.png')
    obj.resize(100, 100)
    obj.render(timg.ASCIIMethod)
    print(Fore.RED + emoji.emojize(':fire: Welcome to Emberblast! :fire:'))

def generate_random_adjacent_matrix(size):
    return [[random.randint(0, 1) for x in range(size)] for y in range(size)]


def generate_visited_default_matrix(size):
    return [[False for x in range(size)] for x in range(size)]