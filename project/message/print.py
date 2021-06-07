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


def print_player_stats(player):
    print(emojis.encode(
        ':man: {name} Stats: \n\n'.format(name=player.name)))
    print(emojis.encode(
        ':bar_chart: Level: {level} \n'
        ':green_heart: Health Points: {health} \n'
        ':blue_heart: Magic Points: {magic} \n'
        ':runner: Move Speed: {move} \n'
        ':books: Intelligence: {intelligence} \n'
        ':dart: Accuracy: {accuracy} \n'
        ':punch: Strength: {attack} \n'
        ':shield: Armour: {armour} \n'
        ':cyclone: Magic Resist: {resist} \n'
        ':pray: Will: {will} \n'.format(level=player.level,
                                        health=player.health_points,
                                        magic=player.magic_points,
                                        move=player.move_speed,
                                        intelligence=player.intelligence,
                                        accuracy=player.accuracy,
                                        attack=player.strength,
                                        armour=player.armour,
                                        resist=player.magic_resist,
                                        will=player.will)))
