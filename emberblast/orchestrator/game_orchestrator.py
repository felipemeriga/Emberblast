import math
import random
from os import system
from typing import List, Optional

from colorama import Fore

from emberblast.conf import get_configuration
from emberblast.communicator import improve_attributes_automatically, communicator_injector
from emberblast.skill import get_player_available_skills
from emberblast.utils import PASS_ACTION_NAME
from emberblast.interface import IGame, IControlledPlayer, IPlayer, IAction, IGameOrchestrator, IEquipmentItem
from emberblast.bot import BotDecisioning
from emberblast.utils.constants import EXPERIENCE_EARNED_ACTION


@communicator_injector()
class GameOrchestrator(IGameOrchestrator):

    def __init__(self, game: IGame) -> None:
        """
        Constructor of the Game Orchestrator, which is the Class that receives a Game object,
        and command and coordinate the actions, and the execution of the game based on turns.

        :param IGame game: The created game to be executed.
        :rtype: None.
        """
        self.clear = lambda: system('clear')
        self.game = game
        self.actions = {}
        self.init_actions()
        self.bot_controller = BotDecisioning(game)
        """
        The actions left, it's an array of the available actions of a player on a turn,
        for each player and each turn, this array is modified.
        """
        self.actions_left: List[str] = []
        """
        The turn remaining players manages how many players are left for playing a turn, this variable
        it's very important for saved games, because it helps the game to be continued exactly from the 
        player that was playing when the game was saved.
        """
        self.turn_remaining_players: List[IPlayer] = []

    def init_actions(self) -> None:
        """
        Init the actions available in the game, each of the actions of the game, are represented by Singleton clases
        that coordinates and implements the execution of that action.

        :rtype: None.
        """

        self.actions['move']: IAction = {'independent': True, 'repeatable': False, 'function': self.move}
        self.actions['defend']: IAction = {'independent': False, 'repeatable': False, 'function': self.defend}
        self.actions['hide']: IAction = {'independent': False, 'repeatable': False, 'function': self.hide}
        self.actions['search']: IAction = {'independent': True, 'repeatable': False, 'function': self.search}
        self.actions['attack']: IAction = {'independent': False, 'repeatable': False, 'function': self.attack}
        self.actions['skill']: IAction = {'independent': False, 'repeatable': False, 'function': self.skill}
        self.actions['item']: IAction = {'independent': False, 'repeatable': False, 'function': self.item}
        self.actions['equip']: IAction = {'independent': True, 'repeatable': True, 'function': self.equip}
        self.actions['drop']: IAction = {'independent': True, 'repeatable': True, 'function': self.drop}
        self.actions['check']: IAction = {'independent': True, 'repeatable': True, 'function': self.check}
        self.actions['pass']: IAction = {'independent': True, 'repeatable': False, 'function': self.pass_turn}

    def execute_game(self) -> None:
        """
        This method should be implement by Styles of Games that Inherits from this superclass.

        :rtype: None.
        """
        raise NotImplementedError('Game::to_string() should be implemented!')

    def initialize_players_skills(self) -> None:
        """
        Each Job/Race grants player specific skills, that can be revealed under some level conditions
        this method basically refresh all the skills for all the players, matching the available skills in the
        configuration file, with players' characteristics.

        :rtype: None.
        """
        for player in self.game.get_all_players():
            player.refresh_skills_list()

    def check_player_level_up(self, player: IPlayer) -> None:
        if player.experience >= 100:
            player.experience = player.experience - 100
            if isinstance(player, IControlledPlayer):
                attributes = self.communicator.questioner.ask_attributes_to_improve()
            else:
                attributes = improve_attributes_automatically(player.job.get_name(), player.race.get_name())
            player.level_up(attributes)
            self.communicator.informer.player_level_up(player.name, player.level)

    def move(self, player: IPlayer) -> Optional[bool]:
        pass

    def defend(self, player: IPlayer) -> Optional[bool]:
        pass

    def hide(self, player: IPlayer) -> Optional[bool]:
        pass

    def search(self, player: IPlayer) -> Optional[bool]:
        pass

    def attack(self, player: IPlayer) -> Optional[bool]:
        pass

    def skill(self, player: IPlayer) -> Optional[bool]:
        pass

    def item(self, player: IPlayer) -> Optional[bool]:
        pass

    def drop(self, player: IPlayer) -> Optional[bool]:
        pass

    def equip(self, player: IPlayer) -> Optional[bool]:
        pass

    def check(self, player: IPlayer) -> Optional[bool]:
        pass

    def pass_turn(self, player: IPlayer) -> Optional[bool]:
        pass

    def check_iterated_side_effects(self, player: IPlayer) -> None:
        iterated_side_effects = [x for x in
                                 filter(lambda effect: effect.occurrence == 'iterated', player.side_effects)]

        for side_effect in iterated_side_effects:
            self.communicator.informer.event('side-effect')
            self.communicator.informer.iterated_side_effect_apply(player.name, side_effect)
        player.compute_iterated_side_effects()

    def check_side_effect_duration(self, player: IPlayer) -> None:
        ended_side_effects = player.compute_side_effect_duration()
        if len(ended_side_effects) > 0:
            for side_effect in ended_side_effects:
                self.communicator.informer.side_effect_ended(player.name, side_effect)


class DeathMatchOrchestrator(GameOrchestrator):

    def __init__(self, game: IGame) -> None:
        """
        Constructor of the DeathMatchOrchestrator.

        :param IGame game: The created game to be executed.
        :rtype: None.
        """
        super().__init__(game)

    def execute_game(self) -> None:
        """
        The implementation of the superclass method,which is the one for executing each of the calculated turns of
        the game. It's the same method to start a newly created game or a continue.

        :rtype: None.
        """
        try:
            self.initialize_players_skills()
            # Getting only the last element of the list, because in the case it's a saved game, it will take the last
            # player turn, and continue from there, if it's a new game, it will only game the first turn, which is the
            # first and the only element of the turns dictionary.
            turn_list = [list(self.game.turns.copy().keys())[-1]]
            self.clear()
            self.communicator.informer.line_separator()
            self.communicator.informer.force_loading(3, 'Starting game', ['bold'])

            for turn in turn_list:
                self.clear()
                self.communicator.informer.new_turn(turn)

                if not len(self.turn_remaining_players) > 0:
                    # Making a copy of the dict, because dicts are mutable, and without a copy, would alter
                    # the attribute from Game class.
                    # Additionally, the remaining players attributes allow the game to be continued from the player
                    # that was playing when the game was saved.
                    self.turn_remaining_players = self.game.turns.get(turn).copy()

                while len(self.turn_remaining_players) > 0:
                    player = self.turn_remaining_players[0]
                    if not player.is_alive():
                        self.turn_remaining_players.remove(player)
                        continue
                    self.communicator.informer.line_separator()
                    self.communicator.informer.player_turn(player.name)
                    # Resetting player's last action, If he was defending or hidden, this will be reset for a new turn
                    player.reset_last_action()
                    if isinstance(player, IControlledPlayer):
                        self.controlled_decisioning(player)
                    else:
                        self.communicator.informer.force_loading(random.randint(2, 4))
                        self.bot_decisioning(player)
                    self.turn_remaining_players.remove(player)

                alive_players = self.game.get_all_alive_players()
                if len(alive_players) < 2:
                    self.clear()
                    self.communicator.informer.player_won(alive_players[0].name)
                    break

                self.game.calculate_turn_order()
                turn_list.append(turn + 1)
        except Exception as err:
            print(err)

    def bot_decisioning(self, player: IPlayer) -> None:
        """
        Function that controls bot decisions over a IA.

        :param IPlayer player: The bot that is currently playing.
        :rtype: None.
        """
        self.check_iterated_side_effects(player)
        try:
            self.bot_controller.decide(player)

        except Exception as err:
            print(err)
            print(Fore.RED + 'System shutdown with unexpected error')

        self.check_side_effect_duration(player)
        self.check_player_level_up(player)

    def hide_invalid_actions(self, player: IPlayer) -> List[str]:
        """
        Hide the actions that are invalid in the player context, for example, if the player doesn't have items
        in his bag, there is no point to show the items options.
        Additionally, another example is a player that hasn't learnt any skills, there is no point in showing skills.

        :param IPlayer player: The player that is currently playing.
        :rtype: List[str].
        """
        valid_actions = self.actions_left.copy()
        if 'skill' in valid_actions:
            if len(player.skills) == 0:
                valid_actions.remove('skill')
        if 'item' in valid_actions:
            if not player.bag.has_item_type(is_usable=True):
                valid_actions.remove('item')
        if not player.bag.has_item_type(is_equipment=True):
            valid_actions.remove('equip')
        if len(player.bag.items) < 1:
            valid_actions.remove('drop')

        return valid_actions

    def controlled_decisioning(self, player: IControlledPlayer) -> None:
        """
        The function for controlled players to decide which actions they are going to execute each turn.

        :param IControlledPlayer player: The player that is currently playing.
        :rtype: None.
        """
        self.actions_left = list(self.actions.keys())
        self.check_iterated_side_effects(player)

        while len(self.actions_left) > 2:
            chosen_action_string = self.communicator.questioner.ask_actions_questions(
                self.hide_invalid_actions(player))
            action = self.actions[chosen_action_string]
            action_function = action['function']
            if action_function(player) is None:
                self.compute_player_decisions(action, chosen_action_string)
        else:
            self.check_side_effect_duration(player)
            self.check_player_level_up(player)

    def compute_player_decisions(self, action: IAction, action_string: str) -> None:
        """
        Compute each actions are still available to be execute, after one was already executed.

        :param IAction action: The action that was selected by the player.
        :param str action_string: The selected action string key.
        :rtype: None.
        """
        if action_string == PASS_ACTION_NAME:
            self.actions_left.clear()
        elif action['repeatable']:
            return
        elif action['independent']:
            self.actions_left.remove(action_string)
        else:
            for key, value in self.actions.items():
                if not value['independent']:
                    self.actions_left.remove(key)

    def move(self, player: IPlayer) -> Optional[bool]:
        move_speed = player.get_attribute_real_value('move_speed')
        possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position, move_speed)
        self.communicator.informer.moving_possibilities(player.position, possibilities, self.game.game_map.graph.matrix,
                                                        self.game.game_map.size)
        selected_place = self.communicator.questioner.ask_where_to_move(possibilities)
        self.game.game_map.move_player(player, selected_place)
        self.communicator.informer.event('move')
        self.communicator.informer.moved(player.name)
        return

    def defend(self, player: IPlayer) -> Optional[bool]:
        player.set_defense_mode(True)
        return

    def hide(self, player: IPlayer) -> Optional[bool]:
        current_accuracy = player.get_attribute_real_value('accuracy')
        additional = (current_accuracy / 5 * 10) / 100

        result = self.game.chose_probability(additional=[additional])
        player.set_hidden(result)
        return

    def search(self, player: IPlayer) -> Optional[bool]:
        self.communicator.informer.event('search')
        items = self.game.game_map.check_item_in_position(player.position)
        self.communicator.informer.force_loading(2)
        if items is not None:
            for item in items:
                player.bag.add_item(item)
                self.communicator.informer.found_item(player_name=player.name, found=True, item_tier=item.tier,
                                                      item_name=item.name)
        else:
            self.communicator.informer.found_item(player_name=player.name)
        return

    def calculate_damage(self, player: IPlayer, foe: IPlayer, dice_result: int) -> int:
        targeted_defense = 'armour' if player.job.damage_vector == 'strength' else 'magic_resist'
        damage = 0
        if player.job.damage_vector == 'intelligence':
            damage = (player.get_attribute_real_value(player.job.damage_vector, player.job.attack_type) / 2) + (
                    dice_result / self.game.dice_sides) * 5
        elif player.job.damage_vector == 'strength' and player.job.attack_type == 'ranged':
            damage = player.get_attribute_real_value(player.job.damage_vector,
                                                     player.job.attack_type) + player.get_attribute_real_value(
                'accuracy') / 2 + (
                             dice_result / self.game.dice_sides) * 5
        else:
            damage = player.get_attribute_real_value(player.job.damage_vector, player.job.attack_type) + (
                    dice_result / self.game.dice_sides) * 5

        return math.ceil(damage - foe.get_attribute_real_value(targeted_defense))

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
            ranged_attack_possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position,
                                                                                                attack_range)
            ranged_attack_possibilities.append(player.position)
            for foe in players:
                if foe.position in ranged_attack_possibilities:
                    possible_foes.append(foe)

        return possible_foes

    def attack(self, player: IPlayer) -> Optional[bool]:
        players = self.game.get_remaining_players(player)
        attack_range = player.get_ranged_attack_area()
        possible_foes = self.get_attack_possibilities(attack_range, player, players)
        if len(possible_foes) == 0:
            self.communicator.informer.no_foes_attack(player)
            return False
        enemy_to_attack = self.communicator.questioner.ask_enemy_to_attack(possible_foes)
        if enemy_to_attack is None:
            return False
        self.communicator.informer.force_loading(2)
        self.communicator.informer.event('attack')
        dice_result = self.game.roll_the_dice()
        self.communicator.informer.dice_result(player.name, dice_result, 'attack', self.game.dice_sides)

        damage = self.calculate_damage(player, enemy_to_attack, dice_result)
        self.check_player_level_up(player)
        if damage > 0:
            enemy_to_attack.suffer_damage(damage)
            self.communicator.informer.suffer_damage(player, enemy_to_attack, damage)
            experience = get_configuration(EXPERIENCE_EARNED_ACTION).get('attack', 0)

            player.earn_xp(experience)
            self.communicator.informer.player_earned_xp(player_name=player.name, xp=experience)

            if not enemy_to_attack.is_alive():
                experience = get_configuration(EXPERIENCE_EARNED_ACTION).get('kill', 0)
                player.earn_xp(experience)
                self.communicator.informer.player_killed_enemy_earned_xp(player_name=player.name, xp=experience)
        else:
            self.communicator.informer.missed(player, enemy_to_attack)
        return

    def get_affected_players_area_skill(self, target_player: IPlayer, remaining_players: List[IPlayer],
                                        skill_affected_area):
        area_foes = [target_player]
        remaining_players.remove(target_player)
        position_possibilities = self.game.game_map.graph.get_available_nodes_in_range(target_player.position,
                                                                                       skill_affected_area)
        position_possibilities.append(target_player.position)

        for player in remaining_players:
            if player.position in position_possibilities:
                area_foes.append(player)

        return area_foes

    def skill(self, player: IPlayer) -> Optional[bool]:
        foes = []
        possible_foes = []

        # Warn the current player that he is running out of mana, and should consider healing it.
        if player.mana <= 5:
            self.communicator.informer.low_mana(player)

        available_skills = get_player_available_skills(player)
        selected_skill = self.communicator.questioner.select_skill(available_skills)
        remaining_players = self.game.get_remaining_players(player)
        if selected_skill is None:
            return False
        if selected_skill.kind == 'recover' or selected_skill.kind == 'buff':
            possible_foes = [player]
        if selected_skill.kind == 'trap':
            self.game.game_map.add_trap_to_map(player.position, selected_skill.side_effects)
            return
        if not selected_skill.applies_caster_only:
            possible_foes.extend(self.get_attack_possibilities(selected_skill.ranged, player, remaining_players))
        if len(possible_foes) == 0:
            self.communicator.informer.no_foes_skill(selected_skill.ranged, player.position)
            return False
        enemy_to_attack = self.communicator.questioner.ask_enemy_to_attack(possible_foes,
                                                                           selected_skill.kind)
        if enemy_to_attack is None:
            return False
        if selected_skill.area > 0:
            foes = self.get_affected_players_area_skill(enemy_to_attack, remaining_players, selected_skill.area)
            if len(foes) > 0:
                self.communicator.informer.area_damage(selected_skill, foes)
        else:
            foes.append(enemy_to_attack)
        self.communicator.informer.force_loading(2)
        self.communicator.informer.event('skill')
        dice_result = self.game.roll_the_dice()
        self.communicator.informer.dice_result(player.name, dice_result, 'skill', self.game.dice_sides)
        dice_result_normalized = dice_result / self.game.dice_sides
        selected_skill.execute(player, foes, dice_result_normalized)
        return

    def item(self, player: IPlayer) -> Optional[bool]:
        using_player = player.name
        usable_items = player.bag.get_usable_items()
        selected_item = self.communicator.questioner.select_item(usable_items)
        if selected_item is None:
            return False
        another_players_in_position = self.game.check_another_players_in_position(player)
        if len(another_players_in_position) > 0:
            if not self.communicator.questioner.confirm_use_item_on_you():
                player = self.communicator.questioner.ask_enemy_to_attack(another_players_in_position)
        if self.communicator.questioner.confirm_item_selection():
            self.communicator.informer.force_loading(2)
            self.communicator.informer.event('item')
            target_player = player.name
            player.use_item(selected_item)
            self.communicator.informer.use_item(using_player, selected_item.name, target_player)
            player.bag.remove_item(selected_item)
        else:
            return True

    def drop(self, player: IPlayer) -> Optional[bool]:
        selected_item = self.communicator.questioner.select_item(player.bag.items)
        if selected_item is None:
            return False
        confirm = self.communicator.questioner.confirm_item_selection()
        if confirm:
            if isinstance(selected_item, IEquipmentItem):
                player.remove_side_effects(selected_item.side_effects)
                player.equipment.check_and_remove(selected_item)
            player.bag.remove_item(selected_item)
            self.game.game_map.add_item_to_map(player.position, selected_item)
        return

    def equip(self, player: IPlayer) -> Optional[bool]:
        equipment_item = self.communicator.questioner.display_equipment_choices(player)
        if equipment_item is None:
            return False
        if player.equipment.is_equipped(equipment_item):
            return False
        previous_equipment = player.equipment.get_previous_equipped_item(equipment_item.category)
        if previous_equipment is not None:
            player.remove_side_effects(previous_equipment.side_effects)
        player.equipment.equip(equipment_item)
        player.side_effects.extend(equipment_item.side_effects)
        return

    def check(self, player: IPlayer) -> Optional[bool]:
        check_option = self.communicator.questioner.ask_check_action(
            show_items=True if len(player.bag.items) > 0 else False)
        if check_option == 'status':
            self.communicator.informer.player_stats(player)
        elif check_option == 'map':
            unhidden_foes = self.game.get_remaining_players(player, include_hidden=False)
            self.communicator.informer.map_info(player, unhidden_foes, self.game.game_map.graph.matrix,
                                                self.game.game_map.size)
        elif check_option == 'enemy':
            enemies = self.game.get_remaining_players(player, include_hidden=False)
            enemy = self.communicator.questioner.ask_enemy_to_check(enemies)
            self.communicator.informer.enemy_status(enemy)
        elif check_option == 'item':
            item = self.communicator.questioner.select_item(player.bag.items)
            self.communicator.informer.check_item(item)
        else:
            return
