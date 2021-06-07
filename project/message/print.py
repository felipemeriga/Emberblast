import timg
from colorama import Fore
from emojis import emojis

from project.utils import get_project_root


def print_greetings():
    obj = timg.Renderer()
    project_path = get_project_root()
    obj.load_image_from_file(str(project_path) + '/img/emberblast.png')
    obj.resize(100, 100)
    obj.render(timg.ASCIIMethod)
    print(Fore.RED + emojis.encode(':fire: Welcome to Emberblast! :fire: \n\n'))
