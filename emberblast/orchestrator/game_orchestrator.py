import asyncio
import math
import random
from os import system
from typing import List, Optional

from emberblast.bot import BotDecisioning
from emberblast.communicator import communicator_injector, improve_attributes_automatically
from emberblast.conf import get_configuration
from emberblast.events import (
    AreaDamageEvent,
    CheckItemEvent,
    DamageEvent,
    DiceRollEvent,
    EnemyStatusEvent,
    EventAction,
    ItemFoundEvent,
    IteratedSideEffectEvent,
    LevelUpEvent,
    LineSeparatorEvent,
    LowManaEvent,
    MapInfoEvent,
    MissedAttackEvent,
    MoveEvent,
    MovingPossibilitiesEvent,
    NoFoesEvent,
    PlayerStatsEvent,
    PlayerTurnEvent,
    SideEffectEndedEvent,
    TurnStartEvent,
    UseItemEvent,
    VictoryEvent,
    XPEarnedEvent,
)
from emberblast.interface import IAction, IControlledPlayer, IEquipmentItem, IGame, IGameOrchestrator, IPlayer
from emberblast.skill import get_player_available_skills
from emberblast.utils import PASS_ACTION_NAME
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
        self.clear = lambda: system("clear")
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

        self.actions["move"]: IAction = {"independent": True, "repeatable": False, "function": self.move}
        self.actions["defend"]: IAction = {"independent": False, "repeatable": False, "function": self.defend}
        self.actions["hide"]: IAction = {"independent": False, "repeatable": False, "function": self.hide}
        self.actions["search"]: IAction = {"independent": True, "repeatable": False, "function": self.search}
        self.actions["attack"]: IAction = {"independent": False, "repeatable": False, "function": self.attack}
        self.actions["skill"]: IAction = {"independent": False, "repeatable": False, "function": self.skill}
        self.actions["item"]: IAction = {"independent": False, "repeatable": False, "function": self.item}
        self.actions["equip"]: IAction = {"independent": True, "repeatable": True, "function": self.equip}
        self.actions["drop"]: IAction = {"independent": True, "repeatable": True, "function": self.drop}
        self.actions["check"]: IAction = {"independent": True, "repeatable": True, "function": self.check}
        self.actions["pass"]: IAction = {"independent": True, "repeatable": False, "function": self.pass_turn}

    async def execute_game(self) -> None:
        """
        This method should be implement by Styles of Games that Inherits from this superclass.

        :rtype: None.
        """
        raise NotImplementedError("Game::to_string() should be implemented!")

    def initialize_players_skills(self) -> None:
        """
        Each Job/Race grants player specific skills, that can be revealed under some level conditions
        this method basically refresh all the skills for all the players, matching the available skills in the
        configuration file, with players' characteristics.

        :rtype: None.
        """
        for player in self.game.get_all_players():
            player.refresh_skills_list()

    async def check_player_level_up(self, player: IPlayer) -> None:
        if player.experience >= 100:
            player.experience = player.experience - 100
            if isinstance(player, IControlledPlayer):
                attributes = await self.communicator.questioner.ask_attributes_to_improve()
            else:
                attributes = improve_attributes_automatically(player.job.get_name(), player.race.get_name())
            player.level_up(attributes)
            self.communicator.informer.render(LevelUpEvent(player_name=player.name, new_level=player.level))

    async def move(self, player: IPlayer) -> Optional[bool]:
        pass

    async def defend(self, player: IPlayer) -> Optional[bool]:
        pass

    async def hide(self, player: IPlayer) -> Optional[bool]:
        pass

    async def search(self, player: IPlayer) -> Optional[bool]:
        pass

    async def attack(self, player: IPlayer) -> Optional[bool]:
        pass

    async def skill(self, player: IPlayer) -> Optional[bool]:
        pass

    async def item(self, player: IPlayer) -> Optional[bool]:
        pass

    async def drop(self, player: IPlayer) -> Optional[bool]:
        pass

    async def equip(self, player: IPlayer) -> Optional[bool]:
        pass

    async def check(self, player: IPlayer) -> Optional[bool]:
        pass

    async def pass_turn(self, player: IPlayer) -> Optional[bool]:
        pass

    def check_iterated_side_effects(self, player: IPlayer) -> None:
        iterated_side_effects = [x for x in filter(lambda effect: effect.occurrence == "iterated", player.side_effects)]

        for side_effect in iterated_side_effects:
            self.communicator.informer.render(EventAction(event="side-effect"))
            self.communicator.informer.render(
                IteratedSideEffectEvent(
                    player_name=player.name,
                    effect_name=side_effect.name,
                    effect_type=side_effect.effect_type,
                    attribute=side_effect.attribute,
                    value=side_effect.base,
                    turns_remaining=side_effect.duration,
                )
            )
        player.compute_iterated_side_effects()

        if iterated_side_effects and isinstance(self, DeathMatchOrchestrator):
            turn = self.bot_controller._current_turn
            effects_desc = ", ".join(
                f"{e.name} ({e.effect_type} {e.attribute} by {e.base})" for e in iterated_side_effects
            )
            self._record_bot_memory(player.name, turn, f"Side effects applied: {effects_desc}")

    def check_side_effect_duration(self, player: IPlayer) -> None:
        ended_side_effects = player.compute_side_effect_duration()
        if len(ended_side_effects) > 0:
            for side_effect in ended_side_effects:
                self.communicator.informer.render(
                    SideEffectEndedEvent(player_name=player.name, effect_name=side_effect.name)
                )
            if isinstance(self, DeathMatchOrchestrator):
                turn = self.bot_controller._current_turn
                names = ", ".join(e.name for e in ended_side_effects)
                self._record_bot_memory(player.name, turn, f"Side effects ended: {names}")


class DeathMatchOrchestrator(GameOrchestrator):
    def __init__(self, game: IGame) -> None:
        """
        Constructor of the DeathMatchOrchestrator.

        :param IGame game: The created game to be executed.
        :rtype: None.
        """
        super().__init__(game)

    def _record_bot_memory(self, player_name: str, turn: int, description: str) -> None:
        """
        Record a game event into a bot's memory so the LLM has context
        about what happened to or around the bot.

        :param str player_name: The name of the bot to record memory for.
        :param int turn: The current turn number.
        :param str description: A description of the event.
        :rtype: None.
        """
        memory = self.bot_controller._get_memory(player_name)
        memory.add(turn, description)

    async def execute_game(self) -> None:
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
            self.communicator.informer.render(LineSeparatorEvent())
            await asyncio.sleep(3)

            for turn in turn_list:
                self.clear()
                self.bot_controller.set_current_turn(turn)
                self.communicator.informer.render(TurnStartEvent(turn=turn))

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
                    self.communicator.informer.render(LineSeparatorEvent())
                    self.communicator.informer.render(PlayerTurnEvent(player_name=player.name))
                    # Resetting player's last action, If he was defending or hidden, this will be reset for a new turn
                    player.reset_last_action()
                    if isinstance(player, IControlledPlayer):
                        await self.controlled_decisioning(player)
                    else:
                        await asyncio.sleep(random.randint(2, 4))
                        await self.bot_decisioning(player)
                    self.turn_remaining_players.remove(player)

                alive_players = self.game.get_all_alive_players()
                if len(alive_players) < 2:
                    self.clear()
                    self.communicator.informer.render(VictoryEvent(player_name=alive_players[0].name))
                    break

                self.game.calculate_turn_order()
                turn_list.append(turn + 1)
        except Exception as err:
            print(err)

    async def bot_decisioning(self, player: IPlayer) -> None:
        """
        Function that controls bot decisions over a IA.

        :param IPlayer player: The bot that is currently playing.
        :rtype: None.
        """
        self.check_iterated_side_effects(player)
        try:
            await self.bot_controller.decide(player)

        except Exception as err:
            print(err)
            print("System shutdown with unexpected error")

        self.check_side_effect_duration(player)
        await self.check_player_level_up(player)

        turn = self.bot_controller._current_turn
        self._record_bot_memory(
            player.name,
            turn,
            f"Completed turn (HP: {player.life}, MP: {player.mana})",
        )

    def hide_invalid_actions(self, player: IPlayer) -> List[str]:
        """
        Hide the actions that are invalid in the player context, for example, if the player doesn't have items
        in his bag, there is no point to show the items options.
        Additionally, another example is a player that hasn't learnt any skills, there is no point in showing skills.

        :param IPlayer player: The player that is currently playing.
        :rtype: List[str].
        """
        valid_actions = self.actions_left.copy()
        if "skill" in valid_actions:
            if len(player.skills) == 0:
                valid_actions.remove("skill")
        if "item" in valid_actions:
            if not player.bag.has_item_type(is_usable=True):
                valid_actions.remove("item")
        if not player.bag.has_item_type(is_equipment=True):
            valid_actions.remove("equip")
        if len(player.bag.items) < 1:
            valid_actions.remove("drop")

        return valid_actions

    async def controlled_decisioning(self, player: IControlledPlayer) -> None:
        """
        The function for controlled players to decide which actions they are going to execute each turn.

        :param IControlledPlayer player: The player that is currently playing.
        :rtype: None.
        """
        self.actions_left = list(self.actions.keys())
        self.check_iterated_side_effects(player)

        while len(self.actions_left) > 2:
            chosen_action_string = await self.communicator.questioner.ask_actions_questions(
                self.hide_invalid_actions(player)
            )
            action = self.actions[chosen_action_string]
            action_function = action["function"]
            if await action_function(player) is None:
                self.compute_player_decisions(action, chosen_action_string)
        else:
            self.check_side_effect_duration(player)
            await self.check_player_level_up(player)

    def compute_player_decisions(self, action: IAction, action_string: str) -> None:
        """
        Compute each actions are still available to be execute, after one was already executed.

        :param IAction action: The action that was selected by the player.
        :param str action_string: The selected action string key.
        :rtype: None.
        """
        if action_string == PASS_ACTION_NAME:
            self.actions_left.clear()
        elif action["repeatable"]:
            return
        elif action["independent"]:
            self.actions_left.remove(action_string)
        else:
            for key, value in self.actions.items():
                if not value["independent"]:
                    self.actions_left.remove(key)

    async def move(self, player: IPlayer) -> Optional[bool]:
        move_speed = player.get_attribute_real_value("move_speed")
        possibilities = self.game.game_map.graph.get_available_nodes_in_range(player.position, move_speed)
        self.communicator.informer.render(
            MovingPossibilitiesEvent(
                player_position=player.position,
                possibilities=possibilities,
                matrix=self.game.game_map.graph.matrix,
                size=self.game.game_map.size,
            )
        )
        selected_place = await self.communicator.questioner.ask_where_to_move(possibilities)
        self.game.game_map.move_player(player, selected_place)
        self.communicator.informer.render(EventAction(event="move"))
        self.communicator.informer.render(MoveEvent(player_name=player.name))
        return

    async def defend(self, player: IPlayer) -> Optional[bool]:
        player.set_defense_mode(True)
        return

    async def hide(self, player: IPlayer) -> Optional[bool]:
        current_accuracy = player.get_attribute_real_value("accuracy")
        additional = (current_accuracy / 5 * 10) / 100

        result = self.game.chose_probability(additional=[additional])
        player.set_hidden(result)
        return

    async def search(self, player: IPlayer) -> Optional[bool]:
        self.communicator.informer.render(EventAction(event="search"))
        items = self.game.game_map.check_item_in_position(player.position)
        await asyncio.sleep(2)
        if items is not None:
            for item in items:
                player.bag.add_item(item)
                self.communicator.informer.render(
                    ItemFoundEvent(player_name=player.name, found=True, item_tier=item.tier, item_name=item.name)
                )
            turn = self.bot_controller._current_turn
            item_names = ", ".join(i.name for i in items)
            self._record_bot_memory(player.name, turn, f"Found items: {item_names}")
        else:
            self.communicator.informer.render(ItemFoundEvent(player_name=player.name, found=False))
        return

    def calculate_damage(self, player: IPlayer, foe: IPlayer, dice_result: int) -> int:
        targeted_defense = "armour" if player.job.damage_vector == "strength" else "magic_resist"
        damage = 0
        if player.job.damage_vector == "intelligence":
            damage = (player.get_attribute_real_value(player.job.damage_vector, player.job.attack_type) / 2) + (
                dice_result / self.game.dice_sides
            ) * 5
        elif player.job.damage_vector == "strength" and player.job.attack_type == "ranged":
            damage = (
                player.get_attribute_real_value(player.job.damage_vector, player.job.attack_type)
                + player.get_attribute_real_value("accuracy") / 2
                + (dice_result / self.game.dice_sides) * 5
            )
        else:
            damage = (
                player.get_attribute_real_value(player.job.damage_vector, player.job.attack_type)
                + (dice_result / self.game.dice_sides) * 5
            )

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
            ranged_attack_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
                player.position, attack_range
            )
            ranged_attack_possibilities.append(player.position)
            for foe in players:
                if foe.position in ranged_attack_possibilities:
                    possible_foes.append(foe)

        return possible_foes

    async def attack(self, player: IPlayer) -> Optional[bool]:
        players = self.game.get_remaining_players(player)
        attack_range = player.get_ranged_attack_area()
        possible_foes = self.get_attack_possibilities(attack_range, player, players)
        if len(possible_foes) == 0:
            self.communicator.informer.render(
                NoFoesEvent(
                    message=f"No foes in range! For melee, foes must be at {player.position}. "
                    f"For ranged, within range {player.get_ranged_attack_area()}"
                )
            )
            return False
        enemy_to_attack = await self.communicator.questioner.ask_enemy_to_attack(possible_foes)
        if enemy_to_attack is None:
            return False
        await asyncio.sleep(2)
        self.communicator.informer.render(EventAction(event="attack"))
        dice_result = self.game.roll_the_dice()
        self.communicator.informer.render(
            DiceRollEvent(
                player_name=player.name,
                result=dice_result,
                kind="attack",
                is_critical=(dice_result == self.game.dice_sides),
            )
        )

        damage = self.calculate_damage(player, enemy_to_attack, dice_result)
        await self.check_player_level_up(player)
        turn = self.bot_controller._current_turn
        if damage > 0:
            enemy_to_attack.suffer_damage(damage)
            self.communicator.informer.render(
                DamageEvent(
                    attacker_name=player.name,
                    target_name=enemy_to_attack.name,
                    damage=damage,
                    target_alive=enemy_to_attack.is_alive(),
                    target_life=enemy_to_attack.life,
                )
            )
            experience = get_configuration(EXPERIENCE_EARNED_ACTION).get("attack", 0)

            player.earn_xp(experience)
            self.communicator.informer.render(XPEarnedEvent(player_name=player.name, xp=experience))

            self._record_bot_memory(player.name, turn, f"Attacked {enemy_to_attack.name} for {damage} damage")
            self._record_bot_memory(
                enemy_to_attack.name,
                turn,
                f"Took {damage} damage from {player.name} (HP: {enemy_to_attack.life})",
            )

            if not enemy_to_attack.is_alive():
                experience = get_configuration(EXPERIENCE_EARNED_ACTION).get("kill", 0)
                player.earn_xp(experience)
                self.communicator.informer.render(XPEarnedEvent(player_name=player.name, xp=experience))
                self._record_bot_memory(player.name, turn, f"Killed {enemy_to_attack.name}")
                self._record_bot_memory(enemy_to_attack.name, turn, f"Was killed by {player.name}")
        else:
            self.communicator.informer.render(
                MissedAttackEvent(attacker_name=player.name, target_name=enemy_to_attack.name)
            )
            self._record_bot_memory(player.name, turn, f"Missed attack on {enemy_to_attack.name}")
        return

    def get_affected_players_area_skill(
        self, target_player: IPlayer, remaining_players: List[IPlayer], skill_affected_area
    ):
        area_foes = [target_player]
        remaining_players.remove(target_player)
        position_possibilities = self.game.game_map.graph.get_available_nodes_in_range(
            target_player.position, skill_affected_area
        )
        position_possibilities.append(target_player.position)

        for player in remaining_players:
            if player.position in position_possibilities:
                area_foes.append(player)

        return area_foes

    async def skill(self, player: IPlayer) -> Optional[bool]:
        foes = []
        possible_foes = []

        # Warn the current player that he is running out of mana, and should consider healing it.
        if player.mana <= 5:
            self.communicator.informer.render(LowManaEvent(player_name=player.name, mana=player.mana))

        available_skills = get_player_available_skills(player)
        selected_skill = await self.communicator.questioner.select_skill(available_skills)
        remaining_players = self.game.get_remaining_players(player)
        if selected_skill is None:
            return False
        if selected_skill.kind == "recover" or selected_skill.kind == "buff":
            possible_foes = [player]
        if selected_skill.kind == "trap":
            self.game.game_map.add_trap_to_map(player.position, selected_skill.side_effects)
            return
        if not selected_skill.applies_caster_only:
            possible_foes.extend(self.get_attack_possibilities(selected_skill.ranged, player, remaining_players))
        if len(possible_foes) == 0:
            self.communicator.informer.render(
                NoFoesEvent(
                    message=(
                        f"No foes in range for this skill "
                        f"(range: {selected_skill.ranged}, your position: {player.position})"
                    )
                )
            )
            return False
        enemy_to_attack = await self.communicator.questioner.ask_enemy_to_attack(possible_foes, selected_skill.kind)
        if enemy_to_attack is None:
            return False
        if selected_skill.area > 0:
            foes = self.get_affected_players_area_skill(enemy_to_attack, remaining_players, selected_skill.area)
            if len(foes) > 0:
                self.communicator.informer.render(
                    AreaDamageEvent(
                        skill_name=selected_skill.name, skill_kind=selected_skill.kind, affected_players=foes
                    )
                )
        else:
            foes.append(enemy_to_attack)
        await asyncio.sleep(2)
        self.communicator.informer.render(EventAction(event="skill"))
        dice_result = self.game.roll_the_dice()
        self.communicator.informer.render(
            DiceRollEvent(
                player_name=player.name,
                result=dice_result,
                kind="skill",
                is_critical=(dice_result == self.game.dice_sides),
            )
        )
        dice_result_normalized = dice_result / self.game.dice_sides
        selected_skill.execute(player, foes, dice_result_normalized)

        turn = self.bot_controller._current_turn
        foe_names = ", ".join(f.name for f in foes)
        self._record_bot_memory(
            player.name,
            turn,
            f"Used skill {selected_skill.name} ({selected_skill.kind}) on {foe_names}",
        )
        for foe in foes:
            if foe.name != player.name:
                self._record_bot_memory(
                    foe.name,
                    turn,
                    f"Hit by {player.name}'s skill {selected_skill.name} ({selected_skill.kind})",
                )
        return

    async def item(self, player: IPlayer) -> Optional[bool]:
        using_player = player.name
        usable_items = player.bag.get_usable_items()
        selected_item = await self.communicator.questioner.select_item(usable_items)
        if selected_item is None:
            return False
        another_players_in_position = self.game.check_another_players_in_position(player)
        if len(another_players_in_position) > 0:
            if not await self.communicator.questioner.confirm_use_item_on_you():
                player = await self.communicator.questioner.ask_enemy_to_attack(another_players_in_position)
        if await self.communicator.questioner.confirm_item_selection():
            await asyncio.sleep(2)
            self.communicator.informer.render(EventAction(event="item"))
            target_player = player.name
            player.use_item(selected_item)
            self.communicator.informer.render(
                UseItemEvent(player_name=using_player, item_name=selected_item.name, target_name=target_player)
            )
            player.bag.remove_item(selected_item)
            turn = self.bot_controller._current_turn
            self._record_bot_memory(
                using_player,
                turn,
                f"Used item {selected_item.name} on {target_player}",
            )
        else:
            return True

    async def drop(self, player: IPlayer) -> Optional[bool]:
        selected_item = await self.communicator.questioner.select_item(player.bag.items)
        if selected_item is None:
            return False
        confirm = await self.communicator.questioner.confirm_item_selection()
        if confirm:
            if isinstance(selected_item, IEquipmentItem):
                player.remove_side_effects(selected_item.side_effects)
                player.equipment.check_and_remove(selected_item)
            player.bag.remove_item(selected_item)
            self.game.game_map.add_item_to_map(player.position, selected_item)
        return

    async def equip(self, player: IPlayer) -> Optional[bool]:
        equipment_item = await self.communicator.questioner.display_equipment_choices(player)
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

    async def check(self, player: IPlayer) -> Optional[bool]:
        check_option = await self.communicator.questioner.ask_check_action(
            show_items=True if len(player.bag.items) > 0 else False
        )
        if check_option == "status":
            self.communicator.informer.render(PlayerStatsEvent(player=player))
        elif check_option == "map":
            unhidden_foes = self.game.get_remaining_players(player, include_hidden=False)
            self.communicator.informer.render(
                MapInfoEvent(
                    current_player=player,
                    enemies=unhidden_foes,
                    matrix=self.game.game_map.graph.matrix,
                    size=self.game.game_map.size,
                )
            )
        elif check_option == "enemy":
            enemies = self.game.get_remaining_players(player, include_hidden=False)
            enemy = await self.communicator.questioner.ask_enemy_to_check(enemies)
            self.communicator.informer.render(EnemyStatusEvent(enemy=enemy))
        elif check_option == "item":
            item = await self.communicator.questioner.select_item(player.bag.items)
            self.communicator.informer.render(CheckItemEvent(item=item))
        else:
            return
