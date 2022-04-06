from abc import abstractmethod, ABC
from enum import Enum
from pathlib import Path
from typing import List, Union, Dict, Optional, Set, Callable, TypedDict


class ISideEffect(ABC):
    name: str
    effect_type: str
    attribute: str
    base: int
    duration: int
    occurrence: str


class ISkill:
    name: str
    description: str
    base: int
    cost: int
    kind: str
    level_requirement: int
    ranged: int
    area: int
    job: str
    base_attribute: str
    side_effects: List[ISideEffect]
    applies_caster_only: bool
    punishment_side_effect: List[ISideEffect]
    communicator: 'ICommunicator'

    def execute(self, player: 'IPlayer', foes: List['IPlayer'], dice_norm_result: float) -> None:
        pass


class IItem(ABC):
    name: str
    tier: str
    description: str
    weight: float


class IHealingItem(IItem):
    attribute: str
    base: int


class IRecoveryItem(IItem):
    status: str


class IEquipmentItem(IItem):
    attribute: str
    base: int
    side_effects: List[ISideEffect]
    category: str
    usage: str
    wielding: int


class IBag(ABC):
    items: List[IItem]
    weight: int

    @abstractmethod
    def add_item(self, item: IItem) -> None:
        pass

    @abstractmethod
    def remove_item(self, item: IItem) -> None:
        pass

    @abstractmethod
    def get_equipments(self) -> List[IEquipmentItem]:
        pass

    @abstractmethod
    def get_usable_items(self) -> List[IItem]:
        pass

    @abstractmethod
    def has_item_type(self, is_usable: bool = False, is_equipment: bool = False) -> bool:
        pass


class IEquipment(ABC):
    weapon: Union[None, IEquipmentItem] = None
    armour: Union[None, IEquipmentItem] = None
    boots: Union[None, IEquipmentItem] = None
    accessory: Union[None, IEquipmentItem] = None

    @abstractmethod
    def equip(self, equipment: IEquipmentItem):
        pass

    @abstractmethod
    def get_attribute_addition(self, attribute: str, usage: str = 'all') -> int:
        pass

    @abstractmethod
    def remove_equipment(self, category: str) -> None:
        pass

    @abstractmethod
    def get_previous_equipped_item(self, category: str) -> Union[None, IEquipmentItem]:
        pass

    @abstractmethod
    def is_equipped(self, equipment: IEquipmentItem) -> bool:
        pass

    @abstractmethod
    def check_and_remove(self, selected_item: IItem) -> None:
        pass

    @abstractmethod
    def remove_side_effect(self, side_effect: ISideEffect) -> None:
        pass


class IJob:
    health_points: int
    magic_points: int
    move_speed: int
    strength: int
    intelligence: int
    accuracy: int
    armour: int
    magic_resist: int
    will: int
    attack_type: str
    damage_vector: str

    @abstractmethod
    def get_name(self):
        pass


class IRace:
    health_points: int
    magic_points: int
    move_speed: int
    strength: int
    intelligence: int
    accuracy: int
    armour: int
    magic_resist: int
    will: int

    @abstractmethod
    def get_name(self):
        pass


class IPlayer(ABC):
    job: IJob
    race: IRace
    name: str
    health_points: int
    magic_points: int
    move_speed: int
    strength: int
    intelligence: int
    accuracy: int
    armour: int
    magic_resist: int
    will: int
    level: int
    experience: int
    side_effects: List[ISideEffect]
    skills: List[ISkill]
    _alive: bool
    position: str
    _hidden: bool
    _defense_mode: bool
    bag: IBag
    equipment: IEquipment
    life: int
    mana: int

    @abstractmethod
    def add_attributes(self, attributes: Union[IJob, IRace] = None) -> None:
        pass

    @abstractmethod
    def level_up(self, improvements: Union[List, Dict]):
        pass

    @abstractmethod
    def earn_xp(self, experience: int) -> None:
        pass

    @abstractmethod
    def suffer_damage(self, damage: float) -> None:
        pass

    @abstractmethod
    def spend_mana(self, quantity: int) -> None:
        pass

    @abstractmethod
    def heal(self, attribute: str, value: int) -> None:
        pass

    @abstractmethod
    def die(self) -> None:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass

    @abstractmethod
    def set_position(self, position: str) -> None:
        pass

    @abstractmethod
    def get_ranged_attack_area(self) -> int:
        pass

    @abstractmethod
    def set_hidden(self, state: bool) -> None:
        pass

    @abstractmethod
    def is_hidden(self) -> bool:
        pass

    @abstractmethod
    def reset_last_action(self) -> bool:
        pass

    @abstractmethod
    def set_defense_mode(self, state: bool) -> None:
        pass

    @abstractmethod
    def is_defending(self) -> bool:
        pass

    @abstractmethod
    def get_defense_value(self, kind: str) -> int:
        pass

    @abstractmethod
    def add_side_effect(self, new_side_effect: ISideEffect) -> None:
        pass

    @abstractmethod
    def use_item(self, item) -> None:
        pass

    @abstractmethod
    def get_attribute_real_value(self, attribute: str, usage: str = 'all') -> int:
        pass

    @abstractmethod
    def remove_side_effects(self, side_effects: List[ISideEffect]) -> None:
        pass

    @abstractmethod
    def compute_iterated_side_effects(self) -> None:
        pass

    @abstractmethod
    def compute_side_effect_duration(self) -> List[ISideEffect]:
        pass

    @abstractmethod
    def refresh_skills_list(self) -> None:
        pass


class IControlledPlayer(IPlayer):
    @abstractmethod
    def level_up(self, improvements: Union[List, Dict]) -> None:
        pass


class IBotPlayer(IPlayer):
    @abstractmethod
    def level_up(self, improvements: Union[List, Dict]) -> None:
        pass


class IEdge(ABC):
    source: str
    destination: str
    weight: float


class IVertex(ABC):
    vertex_id: str
    position: Dict
    edges: List[IEdge]
    value: int

    @abstractmethod
    def add_edge(self, edge: IEdge) -> None:
        pass


class IGraph(ABC):
    size: int
    graph_dict: Dict[str, IVertex]
    matrix: List[List]

    @abstractmethod
    def init_graph(self, fixed_matrix: List[List[int]] = None) -> None:
        pass

    @abstractmethod
    def _create_matrix_dfs_traverse(self, matrix: List[List[int]], row: int, column: int,
                                    visited: List[List[bool]]) -> None:
        pass

    @abstractmethod
    def _compute_vertical_edges(self, vertex: IVertex, row: int, column: int, matrix: List[List[int]]) -> None:
        pass

    @abstractmethod
    def _compute_horizontal_edges(self, vertex: IVertex, row: int, column: int, matrix: List[List[int]]) -> None:
        pass

    @abstractmethod
    def _compute_diagonal_edges(self, vertex: IVertex, row: int, column: int, matrix: List[List[int]]) -> None:
        pass

    @abstractmethod
    def get_list_of_nodes(self) -> List[str]:
        pass

    @abstractmethod
    def is_vertex_valid(self, row: int, column: int) -> bool:
        pass

    @abstractmethod
    def compute_recursive_range_edges(self, vertex: IVertex, reach: float, available_nodes: Set[str],
                                      origin_node: str) -> None:
        pass

    @abstractmethod
    def get_available_nodes_in_range(self, position: str, radius: int) -> List[str]:
        pass

    @abstractmethod
    def is_target_in_range(self, position: str, radius: int, target_position: str) -> bool:
        pass

    @abstractmethod
    def get_number_of_walkable_nodes(self) -> int:
        pass

    @abstractmethod
    def is_graph_defective(self) -> bool:
        pass

    @abstractmethod
    def get_walkable_nodes(self) -> Dict[str, IVertex]:
        pass

    @abstractmethod
    def fill_infinite_distance_dict(self, distances: Dict[str, float]) -> None:
        pass

    @abstractmethod
    def get_shortest_distance_between_positions(self, s1: str, s2: str) -> float:
        pass

    @abstractmethod
    def get_shortest_path(self, source_position: str) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_average_distance_source_destinations(self, source: str, positions: List[str]) -> float:
        pass

    @abstractmethod
    def get_average_distances_sources_destinations_map(self, sources: List[str],
                                                       positions: List[str]) -> Dict[str, float]:
        pass


class IMap(ABC):
    name: str
    type: str
    size: int
    graph: IGraph
    items: Dict[str, List[IItem]]

    @abstractmethod
    def define_player_initial_position_random(self, players: List[IPlayer]) -> None:
        pass

    @abstractmethod
    def pick_available_position(self, selected_positions: List[str]) -> str:
        pass

    @abstractmethod
    def distribute_random_items(self) -> None:
        pass

    @abstractmethod
    def check_item_in_position(self, position: str) -> Optional[List[IItem]]:
        pass

    @abstractmethod
    def add_item_to_map(self, position: str, item: IItem) -> None:
        pass

    @abstractmethod
    def add_trap_to_map(self, position: str, side_effects: List[ISideEffect]) -> None:
        pass

    @abstractmethod
    def get_traps_from_position(self, position: str) -> List[ISideEffect]:
        pass

    @abstractmethod
    def move_player(self, player: IPlayer, destination: str) -> None:
        pass


class ITurnStatistics(ABC):
    killer: bool
    healer: bool
    damage_caused: float
    healed_damage: float
    critical_hit: bool
    hidden: bool
    defended_damage: float
    multiple_foes_count: int
    item_found_tier: str
    tiles_moved: int


class IStatistics(ABC):
    turn_statistics: Dict[int, Dict[str, ITurnStatistics]]


class IGame(ABC):
    players: List[IPlayer]
    game_map: IMap
    turns: Dict[int, List[IPlayer]]
    dice_sides: int

    @abstractmethod
    def calculate_turn_key(self, player: IPlayer) -> float:
        pass

    @abstractmethod
    def calculate_turn_order(self) -> None:
        pass

    @abstractmethod
    def roll_the_dice(self) -> int:
        pass

    @abstractmethod
    def chose_probability(self, additional: List[float] = None) -> bool:
        pass

    @abstractmethod
    def check_another_players_in_position(self, current_player: IPlayer) -> List[IPlayer]:
        pass

    @abstractmethod
    def get_all_players(self) -> List[IPlayer]:
        pass

    @abstractmethod
    def get_all_alive_players(self) -> List[IPlayer]:
        pass

    @abstractmethod
    def get_remaining_players(self, player: IPlayer, include_hidden: bool = False) -> List[IPlayer]:
        pass


class IAction(TypedDict):
    independent: bool
    repeatable: bool
    function: Callable


class IPlayingMode(Enum):
    NEUTRAL = 0
    AGGRESSIVE = 1
    DEFENSIVE = 2


class IQuestioningSystem(ABC):

    @abstractmethod
    def ask_check_action(self, show_items: bool = False) -> Union[str, bool, list, str]:
        """
        Ask which kind of information player wants to check.

        :param bool show_items: If the player doesn't have items on its bag, this flag will help the
        communicator to remove the items question.
        :rtype: Union[str, bool, list, str].
        """
        pass

    @abstractmethod
    def ask_actions_questions(self, actions_available: List[str]) -> Union[str, bool, list, str]:
        """
        Ask which action the player is going to execute.

        :param List[str] actions_available: The actions that the player it's currently allowed to execute.
        :rtype: Union[str, bool, list, str].
        """
        pass

    @abstractmethod
    def ask_enemy_to_check(self, enemies: List[IPlayer]) -> Union[str, bool, list, IPlayer]:
        """
        Ask which enemy the player wants to know more info.

        :param List[IPlayer] enemies: The unhidden players to analyze.
        :rtype: Union[str, bool, list, IPlayer].
        """
        pass

    @abstractmethod
    def ask_enemy_to_attack(self, enemies: List[IPlayer], skill_type: str = '') -> Union[str, bool, list, IPlayer]:
        """
        Ask which enemy to attack.

        :param List[IPlayer] enemies: The possible foes.
        :param str skill_type: The type of the attack/skill.
        :rtype: Union[str, bool, list, IPlayer].
        """
        pass

    @abstractmethod
    def select_item(self, items: List[IItem]) -> Union[str, bool, list, IItem]:
        """
        Select an item to use, or even get more information about it.

        :param List[IItem] items: The available items for the player.
        :rtype: Union[str, bool, list, IItem].
        """
        pass

    @abstractmethod
    def confirm_item_selection(self) -> Union[str, bool, list, bool]:
        """
        Confirm question, to ensure that player really wants to use the selected item.

        :rtype: Union[str, bool, list, bool].
        """
        pass

    @abstractmethod
    def confirm_use_item_on_you(self) -> Union[str, bool, list, bool]:
        """
        Confirm question, to ensure that player really wants to use the selected item on himself.

        :rtype: Union[str, bool, list, bool].
        """
        pass

    @abstractmethod
    def display_equipment_choices(self, player: IPlayer) -> Union[str, bool, list, IEquipmentItem]:
        """
        Will display all the equipments that player has, for equipping one of them.

        :param IPlayer player: The current player.
        :rtype: Union[str, bool, list, IEquipmentItem].
        """
        pass

    @abstractmethod
    def ask_attributes_to_improve(self) -> Union[str, bool, list, List]:
        """
        This function is used by human controlled players to chose which attribute they want to upgrade

        :rtype: Union[str, bool, list, list].
        """
        pass

    @abstractmethod
    def ask_where_to_move(self, possibilities: List[str]) -> Union[str, bool, list, str]:
        """
        This function is used by asking the player where he wants to move.

        :param List[str] possibilities: The previously calculated possibilities of movement.
        :rtype: Union[str, bool, list, str].
        """
        pass

    @abstractmethod
    def perform_first_question(self) -> Union[str, bool, list, str]:
        """
        This function is used by asking a new game communicator.

        :rtype: Union[str, bool, list, dict].
        """
        pass

    @abstractmethod
    def perform_game_create_questions(self) -> Union[str, bool, list, dict]:
        """
        This function is used by asking a new game communicator.

        :rtype: Union[str, bool, list, dict].
        """
        pass

    @abstractmethod
    def select_skill(self, available_skills: List[ISkill]) -> Union[str, bool, list, ISkill]:
        """
        Question function, to query user for available skills to use.

        :param List[ISkill] available_skills: Skills to be chosen.
        :rtype: None
        """
        pass

    @abstractmethod
    def get_saved_game(self, normalized_files: List[Dict]) -> Union[str, bool, list, Path]:
        """
        Ask the players, which load file he wants to continue playing, the saved games comes in the normalized_files
        parameter, that it's a list of dictionaries that has the file itself, and also a normalized user friendly
        formatted name of this file.

        :param List[Dict] normalized_files: The dictionary of all saved games.
        :rtype: Union[str, bool, list, Path].
        """
        pass

    @abstractmethod
    def perform_character_creation_questions(self, existing_names: List[str]) -> Union[str, bool, list, dict]:
        """
        This function is used when creating a new character.

        :rtype: Union[str, bool, list, dict].
        """
        pass


class IInformingSystem(ABC):

    @abstractmethod
    def greetings(self) -> None:
        """
        Print game greetings.

        :rtype: None
        """
        pass

    @abstractmethod
    def new_turn(self, turn: int) -> None:
        """
        Print that a new turn started.

        :rtype: None
        """
        pass

    @abstractmethod
    def player_turn(self, name: str) -> None:
        """
        Print that the player's turn started.

        :rtype: None
        """
        pass

    @abstractmethod
    def player_earned_xp(self, player_name: str, xp: int) -> None:
        """
        Print that a player as leveled up.

        :param str player_name: The name of the player.
        :param int xp: The amount of experience earned.
        :rtype: None
        """
        pass

    @abstractmethod
    def moved(self, player_name: str) -> None:
        """
        Print that a player moved to another place.

        :param str player_name: The name of the player.
        :rtype: None
        """
        pass

    @abstractmethod
    def player_killed_enemy_earned_xp(self, player_name: str, foe: str, xp: int) -> None:
        """
        Print that a player as leveled up.

        :param str player_name: The name of the player.
        :param str foe: The name of the foe.
        :param int xp: The amount of experience earned.
        :rtype: None
        """
        pass

    @abstractmethod
    def player_level_up(self, player_name: str, level: int) -> None:
        """
        Print that a player as leveled up.

        :param str player_name: The name of the player.
        :param int level: New level.
        :rtype: None
        """
        pass

    @abstractmethod
    def player_stats(self, player: IPlayer):
        """
        Print the current playing player stats and attributes.

        :param IPlayer player: The current player.
        :rtype: None
        """
        pass

    @abstractmethod
    def enemy_status(self, enemy: IPlayer) -> None:
        """
        Print the current status and attributes of a unhidden player.

        :param IPlayer enemy: The selected enemy.
        :rtype: None
        """
        pass

    @abstractmethod
    def plain_matrix(self, matrix: List[List[int]]) -> None:
        """
        Print the matrix, that represents the map.

        :param List[List[int]] matrix: The matrix that represents the map.
        :rtype: None
        """
        pass

    @abstractmethod
    def plain_map(self, matrix: List[List[int]], size: int) -> None:
        """
        Print the plain map, without any additional info.

        :param List[List[int]] matrix: The matrix that represents the map.
        :param int size: Size of the map.
        :rtype: None
        """
        pass

    @abstractmethod
    def map_info(self, player: IPlayer, players: List[IPlayer], matrix: List[List[int]], size: int) -> None:
        """
        Print the current position of all unhidden players in the map, and all the characteristics of it.

        :param IPlayer player: The player that is currently playing.
        :param List[IPlayer] players: Another competitors.
        :param List[List[int]] matrix: The matrix that represents the map.
        :param int size: Size of the map.
        :rtype: None
        """
        pass

    @abstractmethod
    def moving_possibilities(self, player_position: str, possibilities: List[str], matrix: List[List[int]],
                             size: int) -> None:
        """
        Print all the possibilities of moving in the map, considering the player's move speed.

        :param str player_position: Original position of the player.
        :param List[str] possibilities: The possibilities of movements, previously calculated.
        :param List[List[int]] matrix: The matrix that represents the map.
        :param int size: Size of the map.
        :rtype: None
        """
        pass

    @abstractmethod
    def found_item(self, player_name: str, found: bool = False, item_tier: str = None, item_name: str = None) -> None:
        """
        Print if an item was found or not.

        :param str player_name: Player's name, whom is currently searching for an item.
        :param bool found: Whether the player has found it.
        :param str item_tier: Tier of the found item.
        :param str item_name: Item name.
        :rtype: None
        """
        pass

    @abstractmethod
    def no_foes_attack(self, player: IPlayer) -> None:
        """
        Print that there is not foe, within the attackers range.

        :param IPlayer player: The attacker.
        :rtype: None
        """
        pass

    @abstractmethod
    def no_foes_skill(self, skill_range: int, player_position: str) -> None:
        """
        Print that there is not foe, within the attackers skill range.

        :param int skill_range: The skill range.
        :param str player_position: The attacker position.
        :rtype: None
        """
        pass

    @abstractmethod
    def area_damage(self, skill: ISkill, affected_players: List[IPlayer]) -> None:
        """
        Print that some skill affects an entire area.

        :param ISkill skill: The casting skill.
        :param List[IPlayer] affected_players: The players that will be affected by the skill.
        :rtype: None
        """
        pass

    @abstractmethod
    def spent_mana(self, name: str, amount: int, skill_name: str) -> None:
        """
        Print that the player spent mana when casting a skill.

        :param str name: Name of the player.
        :param int amount: The amount spent.
        :param str skill_name: The name of the skill.
        :rtype: None
        """
        pass

    @abstractmethod
    def add_side_effect(self, name: str, side_effect: ISideEffect) -> None:
        """
        Print that the player has got a side-effect.

        :param str name: Name of the player.
        :param ISideEffect side_effect: The side-effect that will be applied.
        :rtype: None
        """
        pass

    @abstractmethod
    def side_effect_ended(self, name: str, side_effect: ISideEffect) -> None:
        """
        Print that a side-effect duration has ended for a player.

        :param str name: Name of the player.
        :param ISideEffect side_effect: The side-effect that has ended.
        :rtype: None
        """
        pass

    @abstractmethod
    def iterated_side_effect_apply(self, name: str, side_effect: ISideEffect) -> None:
        """
        Print that the player passed its turn, and suffered/buffed from an iterated side-effect.

        :param str name: Name of the player.
        :param ISideEffect side_effect: The side-effect that will be applied.
        :rtype: None
        """
        pass

    @abstractmethod
    def low_mana(self, player: IPlayer) -> None:
        """
        Print that the player is running out of mana.

        :param IPlayer player: Current player.
        :rtype: None
        """
        pass

    def heal(self, healer: IPlayer, foe: IPlayer, amount: int) -> None:
        """
        Print that the player healed himself or another one.

        :param IPlayer healer: The healer.
        :param IPlayer foe: The healed.
        :param int amount: The amount of life healed.
        :rtype: None
        """
        pass

    @abstractmethod
    def missed(self, player: IPlayer, foe: IPlayer) -> None:
        """
        Print that the player missed the attack.

        :param IPlayer player: The attacking player.
        :param IPlayer foe: The foe suffering damage.
        :rtype: None
        """
        pass

    @abstractmethod
    def trap_activated(self, player: IPlayer, side_effects: List[ISideEffect]) -> None:
        """
        Print that a player has fallen into a trap

        :param IPlayer player: The attacking player.
        :param ISideEffect side_effects: Side effects that will be applied.
        :rtype: None
        """
        pass

    @abstractmethod
    def suffer_damage(self, attacker: IPlayer, foe: IPlayer, damage: int) -> None:
        """
        Print whenever a player inflicts damages to another players.

        :param IPlayer attacker: The attacking player.
        :param IPlayer foe: The one suffering the attack.
        :param int damage: Amount of damage done.
        :rtype: None
        """
        pass

    @abstractmethod
    def dice_result(self, name: str, result: int, kind: str, max_sides: int) -> None:
        """
        Print the result when a player rolls the dice.

        :param str name: The name of the player who is rolling the dice.
        :param int result: Dice result.
        :param str kind: The purpose of rolling the dice, like attacking, skill.
        :param int max_sides: The max sides of the dice, to detect critical attacks/skills.
        :rtype: None
        """
        pass

    @abstractmethod
    def use_item(self, player_name: str, item_name: str, target_name: str) -> None:
        """
        Notify another players, that someone used an item.

        :param str player_name: The player name that is currently using an item.
        :param str item_name: The item name that is being used.
        :param str target_name: The name of who is the item used on.
        :rtype: None
        """
        pass

    @abstractmethod
    def player_fail_stole_item(self, name: str, foe_name: str) -> None:
        """
        Print that a player has failed in stealing an item

        :param str name: Name of the player.
        :param str foe_name: Name of the foe.
        :rtype: None
        """
        pass

    @abstractmethod
    def player_stole_item(self, name: str, foe_name: str, item_name: str, tier: str) -> None:
        """
        Print that a player has stolen an item

        :param str name: Name of the player.
        :param str foe_name: Name of the foe.
        :param str item_name: Name of the stolen item.
        :param str tier: tier of the item.
        :rtype: None
        """
        pass

    @abstractmethod
    def player_won(self, name: str) -> None:
        """
        Print the player that won the game.

        :param str name: Name of the player.
        :rtype: None
        """
        pass

    @abstractmethod
    def create_new_character(self, number: int) -> None:
        """
        Print the status, that someone is currently creating one character.

        :param int number: Number of the player.
        :rtype: None
        """
        pass

    @abstractmethod
    def check_item(self, item: IItem) -> None:
        """
        Print Item information that was selected by the player

        :param IItem item: Item instance that will be printed.
        :rtype: None
        """
        pass

    @abstractmethod
    def event(self, event: str) -> None:
        """
        Display that an user executed one of the available actions

        :param str event: The selected event.
        :rtype: None
        """
        pass

    @abstractmethod
    def line_separator(self) -> None:
        """
        Separate the information between the actions of two different players.
        Usually used with terminal implementations

        :rtype: None
        """
        pass

    @abstractmethod
    def force_loading(self, loading_time: int, prefix: str = '', prefix_attributes: List[str] = None) -> None:
        """
        Simulate a loading, just to give a better flow to gaming experience

        :rtype: None
        """
        pass


class ICommunicator(ABC):
    questioner: IQuestioningSystem
    informer: IInformingSystem


class IBotDecisioning(ABC):
    game: IGame
    current_bot: Union[None, IPlayer]
    current_play_style: IPlayingMode
    communicator: ICommunicator


class IGameOrchestrator:
    clear: Callable
    game: IGame
    actions: Dict[str, IAction]
    actions_left: List[str]
    turn_remaining_players: List[IPlayer]
    communicator: ICommunicator

    @abstractmethod
    def init_actions(self) -> None:
        pass

    @abstractmethod
    def execute_game(self) -> None:
        pass

    @abstractmethod
    def initialize_players_skills(self) -> None:
        pass

    @abstractmethod
    def check_iterated_side_effects(self, player: IPlayer) -> None:
        pass

    @abstractmethod
    def check_side_effect_duration(self, player: IPlayer) -> None:
        pass


class IGameFactory:
    begin_question_results: Union[Union[str, bool, list, dict], None]
    communicator: ICommunicator

    @abstractmethod
    def pre_initial_settings(self) -> IGameOrchestrator:
        pass

    @abstractmethod
    def new_game(self) -> IGameOrchestrator:
        pass

    @abstractmethod
    def init_map(self, map_size: int) -> IMap:
        pass

    @abstractmethod
    def init_players(self) -> IControlledPlayer:
        pass

    @abstractmethod
    def init_bots(self) -> List[IBotPlayer]:
        pass


class IEmberblast(ABC):
    communicator: ICommunicator

    @abstractmethod
    def run(self) -> None:
        pass
