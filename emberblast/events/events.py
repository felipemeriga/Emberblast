from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class GameEvent:
    """Base class for all game events."""

    pass


@dataclass
class GreetingsEvent(GameEvent):
    pass


@dataclass
class TurnStartEvent(GameEvent):
    turn: int


@dataclass
class PlayerTurnEvent(GameEvent):
    player_name: str


@dataclass
class LineSeparatorEvent(GameEvent):
    pass


@dataclass
class MoveEvent(GameEvent):
    player_name: str
    from_position: Optional[str] = None
    to_position: Optional[str] = None


@dataclass
class DamageEvent(GameEvent):
    attacker_name: str
    target_name: str
    damage: int
    target_alive: bool
    target_life: int


@dataclass
class HealEvent(GameEvent):
    healer_name: str
    target_name: str
    amount: int
    target_life: int


@dataclass
class SkillEvent(GameEvent):
    caster_name: str
    skill_name: str
    mana_cost: int


@dataclass
class SpentManaEvent(GameEvent):
    player_name: str
    amount: int
    skill_name: str


@dataclass
class ItemEvent(GameEvent):
    player_name: str
    item_name: str
    target_name: str


@dataclass
class UseItemEvent(GameEvent):
    player_name: str
    item_name: str
    target_name: str


@dataclass
class DiceRollEvent(GameEvent):
    player_name: str
    result: int
    kind: str
    is_critical: bool


@dataclass
class NarrationEvent(GameEvent):
    player_name: str
    text: str


@dataclass
class DeathEvent(GameEvent):
    player_name: str


@dataclass
class VictoryEvent(GameEvent):
    player_name: str


@dataclass
class SideEffectEvent(GameEvent):
    player_name: str
    effect_name: str
    effect_type: str
    occurrence: str


@dataclass
class SideEffectEndedEvent(GameEvent):
    player_name: str
    effect_name: str


@dataclass
class IteratedSideEffectEvent(GameEvent):
    player_name: str
    effect_name: str
    effect_type: str
    attribute: str
    value: int
    turns_remaining: int


@dataclass
class ItemFoundEvent(GameEvent):
    player_name: str
    found: bool
    item_name: Optional[str] = None
    item_tier: Optional[str] = None


@dataclass
class LevelUpEvent(GameEvent):
    player_name: str
    new_level: int


@dataclass
class XPEarnedEvent(GameEvent):
    player_name: str
    xp: int
    kill_target: Optional[str] = None


@dataclass
class EventAction(GameEvent):
    event: str


@dataclass
class LowManaEvent(GameEvent):
    player_name: str
    mana: int


@dataclass
class MissedAttackEvent(GameEvent):
    attacker_name: str
    target_name: str


@dataclass
class TrapActivatedEvent(GameEvent):
    player_name: str
    side_effect_names: List[str] = field(default_factory=list)


@dataclass
class NoFoesEvent(GameEvent):
    message: str


@dataclass
class AreaDamageEvent(GameEvent):
    skill_name: str
    skill_kind: str
    affected_players: List[Any] = field(default_factory=list)


@dataclass
class PlayerStoleItemEvent(GameEvent):
    player_name: str
    foe_name: str
    item_name: str
    tier: str


@dataclass
class PlayerFailStoleItemEvent(GameEvent):
    player_name: str
    foe_name: str


@dataclass
class NewCharacterEvent(GameEvent):
    number: int


@dataclass
class MapInfoEvent(GameEvent):
    current_player: Any
    enemies: List[Any]
    matrix: List[List[int]]
    size: int


@dataclass
class MovingPossibilitiesEvent(GameEvent):
    player_position: str
    possibilities: List[str]
    matrix: List[List[int]]
    size: int


@dataclass
class PlayerStatsEvent(GameEvent):
    player: Any


@dataclass
class EnemyStatusEvent(GameEvent):
    enemy: Any


@dataclass
class CheckItemEvent(GameEvent):
    item: Any
