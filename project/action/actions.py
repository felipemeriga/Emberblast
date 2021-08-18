"""
The plan here would be, as actions controls the game,
there will be a Singleton class called actions coordinator, that will
manage all the plays for all the players.

As the actions can be the same for each of the players, they will be considered Singletons
too.

Another thing to remember when creating the actions, is to use function generators and yield
for coordinating the move + another action per turn for each player.

Also, before this, we need to think about how it would be the difference between single player and
multiplayer, considering that it's ideal to use the same game class structure, to avoid copying similar
functionalities
"""
import math
from typing import List, Optional

from project.questions import ask_check_action, ask_enemy_to_check, ask_where_to_move, select_item, \
    confirm_item_selection, display_equipment_choices, confirm_use_item_on_you, ask_enemy_to_attack
from project.message import print_player_stats, print_enemy_status, print_map_info, print_moving_possibilities, \
    print_found_item, print_check_item, print_dice_result, print_suffer_damage, print_no_available_foes
from project.interface import IGame, IPlayer, IAction


class SingletonAction(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonAction, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Action(IAction, metaclass=SingletonAction):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        """
        Constructor of the Base Class for Actions.

        :param bool independent: If it's True, the execution of this action will not block others in the same turn.
        :param bool repeatable: If it's True, can be performed many times in a single turn.
        :param Game game: The current Game object, where the actions are going to be placed.
        :rtype: None
        """
        self.independent = independent
        self.repeatable = repeatable
        self.game = game

    def act(self, player: IPlayer) -> Optional[bool]:
        """
        Base function for executing the action, it has an Optional
        return boolean value, which means that, in the case the action
        is cancelled, it will return True

        :param player:
        :rtype: Optional[bool]
        """
        pass

    def compute_analytics(self) -> None:
        pass


class Move(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position, player.move_speed)
        print_moving_possibilities(player.position, possibilities, self.game.game_map.graph.matrix,
                                   self.game.game_map.size)
        selected_place = ask_where_to_move(possibilities)
        player.set_position(selected_place)
        return


class Defend(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)


class Hide(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        result = self.game.chose_probability(additional=[0.7])
        player.set_hidden(result)
        return


class Search(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        items = self.game.game_map.check_item_in_position(player.position)
        if items is not None:
            for item in items:
                player.bag.add_item(item)
                print_found_item(player_name=player.name, found=True, item_tier=item.tier, item_name=item.name)
        else:
            print_found_item(player_name=player.name)
        return


class Attack(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def get_attack_possibilities(self, player: IPlayer, players: List[IPlayer]) -> List[IPlayer]:
        """
        This function computes which enemies a player can attack, considering its attack style,
        ranged or melee.

        :param Player player: The player that will execute the attack action.
        :param List[Player] players: The another players playing against.
        :rtype: List[Player] players: The list of enemies to attack.
        """
        possible_foes = []
        attacker_combat_type = player.job.attack_type

        if attacker_combat_type == 'melee':
            for foe in players:
                if player.position == foe.position:
                    possible_foes.append(foe)
        elif attacker_combat_type == 'ranged':
            # TODO - implement the foes possibilities to ranged attacks
            '''
            For implementing this, considering that the map will still stay in the square matrix architecture,
            to check which foes are within the attacker reach, we just need to draw a circle from the attacker position,
            where the radius of this circle, it's the attacker's reach. Everyone inside that range, will be a possible 
            foe, the only thing that might be good to bear in mind, it's to test the scalability of the ranged attack,
            because the fact of using a circle to determinate foes, it's already a big advantage to ranged based
            players.
            '''
            position_possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position,
                                                                                           player.get_ranged_attack_area())
            for foe in players:
                if foe.position in position_possibilities:
                    possible_foes.append(foe)

        return possible_foes

    def act(self, player: IPlayer) -> Optional[bool]:
        players = self.game.get_remaining_players(player)
        possible_foes = self.get_attack_possibilities(player, players)
        if len(possible_foes) == 0:
            print_no_available_foes(player)
            return False
        enemy_to_attack = ask_enemy_to_attack(possible_foes)
        dice_result = self.game.roll_the_dice()
        print_dice_result(player.name, dice_result, 'attack', self.game.dice_sides)
        damage = math.ceil(player.strength + (dice_result / self.game.dice_sides) * 5)
        enemy_to_attack.suffer_damage(damage)
        print_suffer_damage(player, enemy_to_attack, damage)
        return


class Skill(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)


class Item(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        usable_items = player.bag.get_usable_items()
        selected_item = select_item(usable_items)
        another_players_in_position = self.game.check_another_players_in_position(player)
        if len(another_players_in_position) > 0:
            if not confirm_use_item_on_you():
                player = ask_enemy_to_check(another_players_in_position)
        if confirm_item_selection():
            player.use_item(selected_item)
            player.bag.remove_item(selected_item)
        else:
            return True


class Drop(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        selected_item = select_item(player.bag.items)
        confirm = confirm_item_selection()
        if confirm:
            player.equipment.check_and_remove(selected_item)
            player.bag.remove_item(selected_item)
            self.game.game_map.add_item_to_map(player.position, selected_item)
        return


class Equip(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        equipment = display_equipment_choices(player)
        player.equipment.equip(equipment)
        return


class Check(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        check_option = ask_check_action(show_items=True if len(player.bag.items) > 0 else False)
        if check_option == 'status':
            print_player_stats(player)
        elif check_option == 'map':
            unhidden_foes = self.game.get_remaining_players(player, include_hidden=True)
            print_map_info(player, unhidden_foes, self.game.game_map.graph.matrix, self.game.game_map.size)
        elif check_option == 'enemy':
            enemies = self.game.get_remaining_players(player, include_hidden=True)
            enemy = ask_enemy_to_check(enemies)
            print_enemy_status(enemy)
        elif check_option == 'item':
            item = select_item(player.bag.items)
            print_check_item(item)
        else:
            return


class Pass(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)
