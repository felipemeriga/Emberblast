from abc import abstractmethod, ABC
from typing import List, Union, Dict, Optional, Set, Callable


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

    def execute(self, player: 'IPlayer', foes: List['IPlayer'], dice_norm_result: float) -> None:
        pass


class ISideEffect(ABC):
    name: str
    effect_type: str
    attribute: str
    base: int
    duration: int
    occurrence: str


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
    def get_attribute_addition(self, attribute: str) -> int:
        pass

    @abstractmethod
    def remove_equipment(self, category: str):
        pass

    @abstractmethod
    def is_equipped(self, equipment: IEquipmentItem) -> bool:
        pass

    @abstractmethod
    def check_and_remove(self, selected_item: IItem):
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
    attack_type: int

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
    attack_type: int

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
    def add_side_effect(self):
        pass

    @abstractmethod
    def use_item(self, item) -> None:
        pass

    @abstractmethod
    def get_attribute_real_value(self, attribute: str) -> int:
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
    def init_graph(self) -> None:
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
    def get_number_of_walkable_nodes(self) -> int:
        pass

    @abstractmethod
    def get_walkable_nodes(self) -> Dict[str, IVertex]:
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


class IGame(ABC):
    main_player: IPlayer
    bots: List[IPlayer]
    game_map: IMap
    turns: Dict[int, List[IPlayer]]
    dice_sides: int

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
