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
    confirm_item_selection, display_equipment_choices, confirm_use_item_on_you, ask_enemy_to_attack, select_skill
from project.message import print_player_stats, print_enemy_status, print_map_info, print_moving_possibilities, \
    print_found_item, print_check_item, print_dice_result, print_suffer_damage, print_no_foes_attack, \
    print_no_foes_skill, print_area_damage, print_missed, print_player_low_mana
from project.interface import IGame, IPlayer, IAction
from project.skill import get_player_available_skills


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

    def get_attack_possibilities(self, attack_range: int, player: IPlayer, players: List[IPlayer]) -> List[IPlayer]:
        """
        This function computes which enemies a player can attack, considering its attack style,
        ranged or melee.

        :param int attack_range: The range of skill/attack, zero means melee attack/skill.
        :param Player player: The player that will execute the attack action.
        :param List[Player] players: The another players playing against.
        :rtype: List[Player] players: The list of enemies to attack.
        """
        possible_foes = []

        if attack_range == 0:
            for foe in players:
                if player.position == foe.position:
                    possible_foes.append(foe)
        elif attack_range > 0:
            position_possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position,
                                                                                           attack_range)
            for foe in players:
                if foe.position in position_possibilities:
                    possible_foes.append(foe)

        return possible_foes

    def compute_analytics(self) -> None:
        pass


class Move(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        move_speed = player.get_attribute_real_value('move_speed')
        possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position, move_speed)
        print_moving_possibilities(player.position, possibilities, self.game.game_map.graph.matrix,
                                   self.game.game_map.size)
        selected_place = ask_where_to_move(possibilities)
        player.set_position(selected_place)
        return


class Defend(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        player.set_defense_mode(True)
        return


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

    def act(self, player: IPlayer) -> Optional[bool]:
        players = self.game.get_remaining_players(player)
        attack_range = player.get_ranged_attack_area()
        possible_foes = self.get_attack_possibilities(attack_range, player, players)
        if len(possible_foes) == 0:
            print_no_foes_attack(player)
            return False
        enemy_to_attack = ask_enemy_to_attack(possible_foes)
        if enemy_to_attack is None:
            return False
        dice_result = self.game.roll_the_dice()
        print_dice_result(player.name, dice_result, 'attack', self.game.dice_sides)
        damage = math.ceil(player.get_attribute_real_value('strength', player.job.attack_type) + (
                dice_result / self.game.dice_sides) * 5
                           - enemy_to_attack.get_attribute_real_value('armour'))
        if damage > 0:
            enemy_to_attack.suffer_damage(damage)
            print_suffer_damage(player, enemy_to_attack, damage)
        else:
            print_missed(player, enemy_to_attack)
        return


class Skill(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def get_affected_players_area_skill(self, target_player: IPlayer, remaining_players: List[IPlayer],
                                        skill_affected_area):
        area_foes = [target_player]
        remaining_players.remove(target_player)
        position_possibilities = self.game.game_map.graph.get_available_nodes_in_range(target_player.position,
                                                                                       skill_affected_area)

        for player in remaining_players:
            if player.position in position_possibilities:
                area_foes.append(player)

        return area_foes

    def act(self, player: IPlayer) -> Optional[bool]:
        foes = []
        possible_foes = []

        # Warn the current player that he is running out of mana, and should consider healing it.
        if player.mana <= 5:
            print_player_low_mana(player)

        available_skills = get_player_available_skills(player)
        selected_skill = select_skill(available_skills)
        remaining_players = self.game.get_remaining_players(player)
        if selected_skill is None:
            return False
        if selected_skill.kind == 'recover':
            possible_foes = [player]
        possible_foes.extend(self.get_attack_possibilities(selected_skill.ranged, player, remaining_players))
        if len(possible_foes) == 0:
            print_no_foes_skill(selected_skill.ranged, player.position)
            return False
        enemy_to_attack = ask_enemy_to_attack(possible_foes)
        if enemy_to_attack is None:
            return False
        if selected_skill.area > 0:
            foes = self.get_affected_players_area_skill(enemy_to_attack, remaining_players, selected_skill.area)
            if len(foes) > 0:
                print_area_damage(selected_skill, foes)
        else:
            foes.append(enemy_to_attack)
        dice_result = self.game.roll_the_dice()
        print_dice_result(player.name, dice_result, 'skill', self.game.dice_sides)
        dice_result_normalized = dice_result / self.game.dice_sides
        selected_skill.execute(player, foes, dice_result_normalized)
        return


class Item(Action):
    def __init__(self, independent: bool, repeatable: bool, game: IGame) -> None:
        super().__init__(independent, repeatable, game)

    def act(self, player: IPlayer) -> Optional[bool]:
        usable_items = player.bag.get_usable_items()
        selected_item = select_item(usable_items)
        if selected_item is None:
            return False
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
