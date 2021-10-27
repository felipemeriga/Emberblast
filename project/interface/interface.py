from abc import abstractmethod, ABC
from enum import Enum
from typing import List, Union, Dict, Optional, Set, Callable


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
    def _level_up(self):
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
    def add_side_effect(self, side_effect: ISideEffect) -> None:
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
    def compute_side_effect_duration(self) -> None:
        pass

    @abstractmethod
    def refresh_skills_list(self) -> None:
        pass


class IControlledPlayer(IPlayer):
    @abstractmethod
    def _level_up(self) -> None:
        pass


class IBotPlayer(IPlayer):
    @abstractmethod
    def _level_up(self) -> None:
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


class IAction:
    independent: bool
    repeatable: bool
    game: IGame

    @abstractmethod
    def act(self, player: IPlayer) -> Optional[bool]:
        pass

    @abstractmethod
    def compute_analytics(self) -> None:
        pass


class ISkillAction(IAction):

    @abstractmethod
    def get_affected_players_area_skill(self, target_player: IPlayer, remaining_players: List[IPlayer],
                                        skill_affected_area):
        pass

    @abstractmethod
    def act(self, player: IPlayer) -> Optional[bool]:
        pass


class IPlayingMode(Enum):
    NEUTRAL = 0
    AGGRESSIVE = 1
    DEFENSIVE = 2


class IBotDecisioning(ABC):
    game: IGame
    current_bot: Union[None, IPlayer]
    current_play_style: IPlayingMode


class IGameOrchestrator:
    clear: Callable
    game: IGame
    actions: Dict[str, IAction]
    actions_left: List[str]
    turn_remaining_players: List[IPlayer]

    @abstractmethod
    def init_actions(self) -> None:
        pass

    @abstractmethod
    def execute_game(self) -> None:
        pass

    @abstractmethod
    def initialize_players_skills(self) -> None:
        pass


class IGameFactory:
    begin_question_results: Union[Union[str, bool, list, dict], None]

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
