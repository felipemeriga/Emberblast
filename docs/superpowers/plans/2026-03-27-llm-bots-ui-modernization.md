# LLM-Powered Bots & UI Modernization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace deterministic bot AI with OpenAI LLM-powered decisions (personality + narration), modernize terminal output with Rich, introduce typed game events with renderer pattern, and migrate tooling to uv.

**Architecture:** Direct replacement of bot decision logic in `BotDecisioning.decide()` with OpenAI calls. Game engine emits typed `GameEvent` dataclasses, consumed by a `RichCLIRenderer` (replacing `InformerCMD`). The `ICommunicator` pattern is preserved — `communicator.informer` becomes the renderer. uv replaces pip/setuptools.

**Tech Stack:** Python 3.10+, OpenAI API (gpt-4o-mini), Rich (terminal UI), uv (package management), InquirerPy (interactive prompts), unittest (testing)

**Code Standards:** Atomic commits per task using conventional commits. Never commit to main directly — create a feature branch. Never add Co-Authored-By. Run `ruff check --fix && ruff format` after changes. Push after every commit.

---

## File Structure

### New Files
- `emberblast/events/__init__.py` — exports all event classes
- `emberblast/events/events.py` — typed GameEvent dataclasses
- `emberblast/renderer/__init__.py` — exports renderer
- `emberblast/renderer/rich_cli.py` — RichCLIRenderer implementation
- `emberblast/bot/llm_client.py` — OpenAI API wrapper, game state serializer, personality prompts
- `emberblast/bot/memory.py` — per-bot turn memory
- `emberblast/test/test_events.py` — event creation tests
- `emberblast/test/test_llm_client.py` — LLM client tests (mocked)
- `emberblast/test/test_memory.py` — memory system tests
- `emberblast/test/test_rich_renderer.py` — renderer tests
- `pyproject.toml` — replaces setup.cfg/setup.py
- `.python-version` — Python version pin

### Modified Files
- `emberblast/interface/interface.py` — add IRenderer, GameEvent base
- `emberblast/communicator/communicator.py` — wire RichCLIRenderer as informer
- `emberblast/communicator/communicator_cmd.py` — swap InformerCMD for RichCLIRenderer
- `emberblast/bot/bot_decisioning.py` — replace decide() with LLM flow + fallback
- `emberblast/orchestrator/game_orchestrator.py` — emit events instead of calling informer directly
- `emberblast/__main__.py` — API key check, remove pip helper

### Removed Files
- `emberblast/communicator/informer_cmd.py` — replaced by RichCLIRenderer
- `setup.cfg` — replaced by pyproject.toml
- `setup.py` — replaced by pyproject.toml

---

## Task 1: Create feature branch and migrate to uv

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Remove: `setup.cfg`
- Remove: `setup.py`
- Modify: `emberblast/__main__.py`

- [ ] **Step 1: Create feature branch**

```bash
git checkout -b feat/llm-bots-ui-modernization
```

- [ ] **Step 2: Create `.python-version`**

Create `.python-version`:
```
3.10
```

- [ ] **Step 3: Create `pyproject.toml`**

Migrate all metadata from `setup.cfg`. Add `openai` and `rich` as new deps. Remove `colorama`, `termcolor`, `emojis`, `timg`. Keep `InquirerPy`. Add `ruff` as dev dependency.

```toml
[project]
name = "Emberblast"
version = "0.0.2"
description = "Medieval Turn based RPG"
readme = "README.md"
license = {text = "MIT"}
authors = [{name = "Felipe Meriga", email = "felipe.meriga@gmail.com"}]
requires-python = ">=3.10"
dependencies = [
    "InquirerPy>=0.2.0",
    "PyYAML>=5.4.1",
    "Cerberus>=1.3.4",
    "numpy>=1.21.1",
    "sqlparse>=0.4.1",
    "cloudpickle>=1.6.0",
    "rich>=13.0.0",
    "openai>=1.0.0",
]

[project.urls]
Homepage = "https://github.com/felipemeriga/Emberblast"
"Bug Tracker" = "https://github.com/felipemeriga/Emberblast/issues"

[project.scripts]
emberblast = "emberblast.__main__:run_project"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I"]
```

- [ ] **Step 4: Remove `setup.cfg` and `setup.py`**

Delete both files.

- [ ] **Step 5: Remove pip helper from `__main__.py`**

In `emberblast/__main__.py`, remove the import of `Fore` from colorama (line 2) since it will be replaced later. Keep `run_project()` function as the entry point but remove any pip-specific logic. The file currently imports `from colorama import Fore` — remove that import and replace the `Fore.RED` usage in the except block with a plain string for now (Rich will handle it in a later task).

Replace:
```python
from colorama import Fore
```
With nothing (remove the import).

Replace:
```python
print(Fore.RED + 'System shutdown with unexpected error')
```
With:
```python
print('System shutdown with unexpected error')
```

- [ ] **Step 6: Install dependencies with uv**

```bash
uv sync
```

- [ ] **Step 7: Run existing tests**

```bash
uv run python -m pytest emberblast/test/ -v 2>/dev/null || uv run python -m unittest discover -s emberblast/test -v
```

Verify tests still pass with the new setup.

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml .python-version emberblast/__main__.py
git rm setup.cfg setup.py
git commit -m "feat: migrate from setuptools to uv with pyproject.toml"
git push -u origin feat/llm-bots-ui-modernization
```

---

## Task 2: Create typed game events

**Files:**
- Create: `emberblast/events/__init__.py`
- Create: `emberblast/events/events.py`
- Create: `emberblast/test/test_events.py`

- [ ] **Step 1: Write the test file**

Create `emberblast/test/test_events.py`:

```python
from emberblast.test.test import BaseTestCase
from emberblast.events import (
    GameEvent, TurnStartEvent, PlayerTurnEvent, MoveEvent, DamageEvent,
    HealEvent, SkillEvent, ItemEvent, DiceRollEvent, NarrationEvent,
    DeathEvent, VictoryEvent, SideEffectEvent, SideEffectEndedEvent,
    IteratedSideEffectEvent, ItemFoundEvent, LevelUpEvent, XPEarnedEvent,
    LineSeparatorEvent, EventAction, LowManaEvent, MissedAttackEvent,
    TrapActivatedEvent, NoFoesEvent, AreaDamageEvent, PlayerStoleItemEvent,
    PlayerFailStoleItemEvent, SpentManaEvent, NewCharacterEvent,
    GreetingsEvent, MovingPossibilitiesEvent, MapInfoEvent, PlayerStatsEvent,
    EnemyStatusEvent, CheckItemEvent, UseItemEvent,
)


class TestGameEvents(BaseTestCase):

    def test_turn_start_event(self):
        event = TurnStartEvent(turn=5)
        self.assertEqual(event.turn, 5)
        self.assertIsInstance(event, GameEvent)

    def test_damage_event(self):
        event = DamageEvent(
            attacker_name="Grukk",
            target_name="Elara",
            damage=15,
            target_alive=True,
            target_life=35,
        )
        self.assertEqual(event.attacker_name, "Grukk")
        self.assertEqual(event.damage, 15)
        self.assertTrue(event.target_alive)

    def test_narration_event(self):
        event = NarrationEvent(
            player_name="Grukk",
            text="You cannot hide from me!",
        )
        self.assertEqual(event.player_name, "Grukk")
        self.assertEqual(event.text, "You cannot hide from me!")

    def test_move_event(self):
        event = MoveEvent(player_name="Grukk")
        self.assertEqual(event.player_name, "Grukk")

    def test_heal_event(self):
        event = HealEvent(
            healer_name="Priest",
            target_name="Grukk",
            amount=20,
            target_life=65,
        )
        self.assertEqual(event.amount, 20)

    def test_victory_event(self):
        event = VictoryEvent(player_name="Grukk")
        self.assertEqual(event.player_name, "Grukk")

    def test_item_found_event_with_item(self):
        event = ItemFoundEvent(
            player_name="Grukk",
            found=True,
            item_name="Healing Potion",
            item_tier="common",
        )
        self.assertTrue(event.found)
        self.assertEqual(event.item_name, "Healing Potion")

    def test_item_found_event_without_item(self):
        event = ItemFoundEvent(player_name="Grukk", found=False)
        self.assertFalse(event.found)
        self.assertIsNone(event.item_name)

    def test_xp_earned_with_kill(self):
        event = XPEarnedEvent(player_name="Grukk", xp=60, kill_target="Elara")
        self.assertEqual(event.kill_target, "Elara")

    def test_xp_earned_without_kill(self):
        event = XPEarnedEvent(player_name="Grukk", xp=30)
        self.assertIsNone(event.kill_target)

    def test_event_action(self):
        event = EventAction(event="attack")
        self.assertEqual(event.event, "attack")

    def test_dice_roll_event(self):
        event = DiceRollEvent(
            player_name="Grukk", result=20, kind="attack", is_critical=True
        )
        self.assertTrue(event.is_critical)

    def test_side_effect_event(self):
        event = SideEffectEvent(
            player_name="Grukk",
            effect_name="Poison",
            effect_type="debuff",
            occurrence="iterated",
        )
        self.assertEqual(event.effect_type, "debuff")

    def test_level_up_event(self):
        event = LevelUpEvent(player_name="Grukk", new_level=4)
        self.assertEqual(event.new_level, 4)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run python -m unittest emberblast.test.test_events -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'emberblast.events'`

- [ ] **Step 3: Create `emberblast/events/events.py`**

```python
from dataclasses import dataclass, field
from typing import List, Optional, Any


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
```

- [ ] **Step 4: Create `emberblast/events/__init__.py`**

```python
from .events import (
    GameEvent,
    GreetingsEvent,
    TurnStartEvent,
    PlayerTurnEvent,
    LineSeparatorEvent,
    MoveEvent,
    DamageEvent,
    HealEvent,
    SkillEvent,
    SpentManaEvent,
    ItemEvent,
    UseItemEvent,
    DiceRollEvent,
    NarrationEvent,
    DeathEvent,
    VictoryEvent,
    SideEffectEvent,
    SideEffectEndedEvent,
    IteratedSideEffectEvent,
    ItemFoundEvent,
    LevelUpEvent,
    XPEarnedEvent,
    EventAction,
    LowManaEvent,
    MissedAttackEvent,
    TrapActivatedEvent,
    NoFoesEvent,
    AreaDamageEvent,
    PlayerStoleItemEvent,
    PlayerFailStoleItemEvent,
    NewCharacterEvent,
    MapInfoEvent,
    MovingPossibilitiesEvent,
    PlayerStatsEvent,
    EnemyStatusEvent,
    CheckItemEvent,
)

__all__ = [
    "GameEvent",
    "GreetingsEvent",
    "TurnStartEvent",
    "PlayerTurnEvent",
    "LineSeparatorEvent",
    "MoveEvent",
    "DamageEvent",
    "HealEvent",
    "SkillEvent",
    "SpentManaEvent",
    "ItemEvent",
    "UseItemEvent",
    "DiceRollEvent",
    "NarrationEvent",
    "DeathEvent",
    "VictoryEvent",
    "SideEffectEvent",
    "SideEffectEndedEvent",
    "IteratedSideEffectEvent",
    "ItemFoundEvent",
    "LevelUpEvent",
    "XPEarnedEvent",
    "EventAction",
    "LowManaEvent",
    "MissedAttackEvent",
    "TrapActivatedEvent",
    "NoFoesEvent",
    "AreaDamageEvent",
    "PlayerStoleItemEvent",
    "PlayerFailStoleItemEvent",
    "NewCharacterEvent",
    "MapInfoEvent",
    "MovingPossibilitiesEvent",
    "PlayerStatsEvent",
    "EnemyStatusEvent",
    "CheckItemEvent",
]
```

- [ ] **Step 5: Run tests**

```bash
uv run python -m unittest emberblast.test.test_events -v
```

Expected: All tests PASS.

- [ ] **Step 6: Lint and commit**

```bash
uv run ruff check --fix emberblast/events/ emberblast/test/test_events.py && uv run ruff format emberblast/events/ emberblast/test/test_events.py
git add emberblast/events/ emberblast/test/test_events.py
git commit -m "feat: add typed game event dataclasses"
git push
```

---

## Task 3: Create RichCLIRenderer

**Files:**
- Create: `emberblast/renderer/__init__.py`
- Create: `emberblast/renderer/rich_cli.py`
- Create: `emberblast/test/test_rich_renderer.py`
- Modify: `emberblast/interface/interface.py`

- [ ] **Step 1: Write the test file**

Create `emberblast/test/test_rich_renderer.py`:

```python
from io import StringIO
from unittest.mock import patch

from emberblast.test.test import BaseTestCase
from emberblast.renderer.rich_cli import RichCLIRenderer
from emberblast.events import (
    TurnStartEvent,
    PlayerTurnEvent,
    MoveEvent,
    DamageEvent,
    NarrationEvent,
    VictoryEvent,
    DiceRollEvent,
    LevelUpEvent,
    XPEarnedEvent,
    LineSeparatorEvent,
    EventAction,
    ItemFoundEvent,
    DeathEvent,
    HealEvent,
    SpentManaEvent,
    SideEffectEvent,
    SideEffectEndedEvent,
    LowManaEvent,
    MissedAttackEvent,
)


class TestRichCLIRenderer(BaseTestCase):

    def setUp(self):
        self.renderer = RichCLIRenderer()

    def test_render_turn_start(self):
        event = TurnStartEvent(turn=3)
        # Should not raise
        self.renderer.render(event)

    def test_render_damage_event(self):
        event = DamageEvent(
            attacker_name="Grukk",
            target_name="Elara",
            damage=15,
            target_alive=True,
            target_life=35,
        )
        self.renderer.render(event)

    def test_render_narration_event(self):
        event = NarrationEvent(
            player_name="Grukk",
            text="You cannot hide!",
        )
        self.renderer.render(event)

    def test_render_victory_event(self):
        event = VictoryEvent(player_name="Grukk")
        self.renderer.render(event)

    def test_render_move_event(self):
        event = MoveEvent(player_name="Grukk")
        self.renderer.render(event)

    def test_render_heal_event(self):
        event = HealEvent(
            healer_name="Priest",
            target_name="Grukk",
            amount=20,
            target_life=65,
        )
        self.renderer.render(event)

    def test_render_dice_roll_event(self):
        event = DiceRollEvent(
            player_name="Grukk", result=20, kind="attack", is_critical=True
        )
        self.renderer.render(event)

    def test_render_level_up_event(self):
        event = LevelUpEvent(player_name="Grukk", new_level=4)
        self.renderer.render(event)

    def test_render_xp_earned_event(self):
        event = XPEarnedEvent(player_name="Grukk", xp=30)
        self.renderer.render(event)

    def test_render_unknown_event_does_not_crash(self):
        from emberblast.events import GameEvent
        event = GameEvent()
        # Unknown events should be silently ignored
        self.renderer.render(event)

    def test_render_item_found(self):
        event = ItemFoundEvent(
            player_name="Grukk", found=True, item_name="Sword", item_tier="rare"
        )
        self.renderer.render(event)

    def test_render_item_not_found(self):
        event = ItemFoundEvent(player_name="Grukk", found=False)
        self.renderer.render(event)

    def test_render_death_event(self):
        event = DeathEvent(player_name="Elara")
        self.renderer.render(event)

    def test_render_missed_attack(self):
        event = MissedAttackEvent(attacker_name="Grukk", target_name="Elara")
        self.renderer.render(event)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run python -m unittest emberblast.test.test_rich_renderer -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'emberblast.renderer'`

- [ ] **Step 3: Add `IRenderer` to interface**

In `emberblast/interface/interface.py`, add after the `IInformingSystem` class (after line 1036):

```python
class IRenderer(ABC):
    @abstractmethod
    def render(self, event: 'GameEvent') -> None:
        pass
```

Also add `IRenderer` to the imports in `emberblast/interface/__init__.py`.

- [ ] **Step 4: Create `emberblast/renderer/rich_cli.py`**

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from emberblast.events import (
    GameEvent,
    GreetingsEvent,
    TurnStartEvent,
    PlayerTurnEvent,
    LineSeparatorEvent,
    MoveEvent,
    DamageEvent,
    HealEvent,
    SpentManaEvent,
    UseItemEvent,
    DiceRollEvent,
    NarrationEvent,
    DeathEvent,
    VictoryEvent,
    SideEffectEvent,
    SideEffectEndedEvent,
    IteratedSideEffectEvent,
    ItemFoundEvent,
    LevelUpEvent,
    XPEarnedEvent,
    EventAction,
    LowManaEvent,
    MissedAttackEvent,
    TrapActivatedEvent,
    NoFoesEvent,
    AreaDamageEvent,
    PlayerStoleItemEvent,
    PlayerFailStoleItemEvent,
    NewCharacterEvent,
    MapInfoEvent,
    MovingPossibilitiesEvent,
    PlayerStatsEvent,
    EnemyStatusEvent,
    CheckItemEvent,
)
from emberblast.utils import convert_number_to_letter


class RichCLIRenderer:

    def __init__(self):
        self.console = Console()
        self._dispatch = {
            GreetingsEvent: self._render_greetings,
            TurnStartEvent: self._render_turn_start,
            PlayerTurnEvent: self._render_player_turn,
            LineSeparatorEvent: self._render_line_separator,
            MoveEvent: self._render_move,
            DamageEvent: self._render_damage,
            HealEvent: self._render_heal,
            SpentManaEvent: self._render_spent_mana,
            UseItemEvent: self._render_use_item,
            DiceRollEvent: self._render_dice_roll,
            NarrationEvent: self._render_narration,
            DeathEvent: self._render_death,
            VictoryEvent: self._render_victory,
            SideEffectEvent: self._render_side_effect,
            SideEffectEndedEvent: self._render_side_effect_ended,
            IteratedSideEffectEvent: self._render_iterated_side_effect,
            ItemFoundEvent: self._render_item_found,
            LevelUpEvent: self._render_level_up,
            XPEarnedEvent: self._render_xp_earned,
            EventAction: self._render_event_action,
            LowManaEvent: self._render_low_mana,
            MissedAttackEvent: self._render_missed_attack,
            TrapActivatedEvent: self._render_trap_activated,
            NoFoesEvent: self._render_no_foes,
            AreaDamageEvent: self._render_area_damage,
            PlayerStoleItemEvent: self._render_player_stole_item,
            PlayerFailStoleItemEvent: self._render_player_fail_stole_item,
            NewCharacterEvent: self._render_new_character,
            MapInfoEvent: self._render_map_info,
            MovingPossibilitiesEvent: self._render_moving_possibilities,
            PlayerStatsEvent: self._render_player_stats,
            EnemyStatusEvent: self._render_enemy_status,
            CheckItemEvent: self._render_check_item,
        }

    def render(self, event: GameEvent) -> None:
        handler = self._dispatch.get(type(event))
        if handler:
            handler(event)

    def _render_greetings(self, event: GreetingsEvent) -> None:
        title = Text("EMBERBLAST", style="bold red")
        panel = Panel(title, title="Welcome", style="red", box=box.DOUBLE)
        self.console.print(panel)

    def _render_turn_start(self, event: TurnStartEvent) -> None:
        panel = Panel(
            f"Turn {event.turn} — Embrace Yourselves!",
            style="bold green",
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def _render_player_turn(self, event: PlayerTurnEvent) -> None:
        self.console.print(f"\n[bold cyan]{event.player_name}[/bold cyan] Time!\n")

    def _render_line_separator(self, event: LineSeparatorEvent) -> None:
        self.console.rule()

    def _render_move(self, event: MoveEvent) -> None:
        self.console.print(f"\t{event.player_name} has just moved to another position\n")

    def _render_damage(self, event: DamageEvent) -> None:
        self.console.print(
            f"\t[red]{event.attacker_name}[/red] inflicted [bold]{event.damage}[/bold] damage on [red]{event.target_name}[/red]"
        )
        if not event.target_alive:
            self.console.print(f"\t[bold red]{event.target_name} is now dead[/bold red]")
        else:
            self.console.print(f"\t{event.target_name} now has {event.target_life} HP")

    def _render_heal(self, event: HealEvent) -> None:
        target = "itself" if event.healer_name == event.target_name else event.target_name
        self.console.print(
            f"\t[green]{event.healer_name}[/green] healed {target} for [bold]{event.amount}[/bold] HP!"
        )
        self.console.print(f"\t{event.target_name} now has {event.target_life} HP")

    def _render_spent_mana(self, event: SpentManaEvent) -> None:
        self.console.print(
            f"\t{event.player_name} casted [blue]{event.skill_name}[/blue] for {event.amount} mana."
        )

    def _render_use_item(self, event: UseItemEvent) -> None:
        target = "himself" if event.target_name == event.player_name else event.target_name
        self.console.print(f"\t{event.player_name} used [green]{event.item_name}[/green] on {target}")

    def _render_dice_roll(self, event: DiceRollEvent) -> None:
        self.console.print(f"\t{event.player_name} rolled the dice and got [bold]{event.result}[/bold]!")
        if event.is_critical:
            self.console.print(f"\t[bold yellow]Critical {event.kind}! Massive damage![/bold yellow]")

    def _render_narration(self, event: NarrationEvent) -> None:
        panel = Panel(
            f'[italic]"{event.text}"[/italic]',
            title=f"[bold]{event.player_name}[/bold]",
            style="dim",
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def _render_death(self, event: DeathEvent) -> None:
        self.console.print(f"\t[bold red]{event.player_name} is now dead[/bold red]")

    def _render_victory(self, event: VictoryEvent) -> None:
        panel = Panel(
            f"[bold green]{event.player_name} won the game![/bold green]",
            style="bold green",
            box=box.DOUBLE,
        )
        self.console.print(panel)

    def _render_side_effect(self, event: SideEffectEvent) -> None:
        if event.effect_type == "debuff" and event.occurrence == "constant":
            status = "debuffed"
        elif event.effect_type == "debuff" and event.occurrence == "iterated":
            status = "inflicted"
        else:
            status = "buffed"
        self.console.print(f"\t{event.player_name} has been {status} with [magenta]{event.effect_name}[/magenta].")

    def _render_side_effect_ended(self, event: SideEffectEndedEvent) -> None:
        self.console.print(f"\t{event.effect_name} has ended for {event.player_name}\n")

    def _render_iterated_side_effect(self, event: IteratedSideEffectEvent) -> None:
        status = "increase" if event.effect_type == "buff" else "decrease"
        attribute = "life" if event.attribute == "health_points" else ("mana" if event.attribute == "magic_points" else event.attribute)
        self.console.print(
            f"\t{event.player_name} affected by [magenta]{event.effect_name}[/magenta], "
            f"will {status} {attribute} by {event.value}/turn. {event.turns_remaining} turns left.\n"
        )

    def _render_item_found(self, event: ItemFoundEvent) -> None:
        if event.found:
            self.console.print(
                f"\t{event.player_name} found a [yellow]{event.item_tier}[/yellow] item! {event.item_name}\n"
            )
        else:
            self.console.print(f"\t{event.player_name} tried to find an item, but nothing was found!\n")

    def _render_level_up(self, event: LevelUpEvent) -> None:
        self.console.print(f"\t[bold yellow]{event.player_name} leveled up to {event.new_level}![/bold yellow]\n")

    def _render_xp_earned(self, event: XPEarnedEvent) -> None:
        if event.kill_target:
            self.console.print(
                f"\t{event.player_name} earned {event.xp} XP by killing {event.kill_target}!\n"
            )
        else:
            self.console.print(f"\t{event.player_name} earned {event.xp} XP!\n")

    def _render_event_action(self, event: EventAction) -> None:
        action_styles = {
            "attack": ("ATTACK", "bold red"),
            "skill": ("SKILL", "bold blue"),
            "search": ("SEARCH", "bold yellow"),
            "item": ("ITEM", "bold green"),
            "move": ("MOVE", "bold cyan"),
            "side-effect": ("SIDE-EFFECT", "bold magenta"),
        }
        label, style = action_styles.get(event.event, (event.event.upper(), "bold"))
        self.console.print(f"[{style}]{label}:[/{style}]")

    def _render_low_mana(self, event: LowManaEvent) -> None:
        self.console.print(
            f"{event.player_name} has [blue]{event.mana}[/blue] mana, consider healing it."
        )

    def _render_missed_attack(self, event: MissedAttackEvent) -> None:
        self.console.print(f"\t{event.attacker_name} tried to attack {event.target_name} but missed.")

    def _render_trap_activated(self, event: TrapActivatedEvent) -> None:
        self.console.print(f"\t[red]{event.player_name} has fallen into a trap![/red]")
        for name in event.side_effect_names:
            self.console.print(f"\t  - {name}")

    def _render_no_foes(self, event: NoFoesEvent) -> None:
        self.console.print(event.message)

    def _render_area_damage(self, event: AreaDamageEvent) -> None:
        self.console.print(
            f"\n\t[blue]{event.skill_name}[/blue] is an area {event.skill_kind} skill, hitting:"
        )
        for player in event.affected_players:
            self.console.print(
                f"\t  [red]{player.name}({player.job.get_name()})[/red] at {player.position} with {player.life} HP"
            )
        self.console.print()

    def _render_player_stole_item(self, event: PlayerStoleItemEvent) -> None:
        self.console.print(
            f"\t{event.player_name} stole [green]{event.item_name}[/green] ({event.tier}) from {event.foe_name}!\n"
        )

    def _render_player_fail_stole_item(self, event: PlayerFailStoleItemEvent) -> None:
        self.console.print(f"\t{event.player_name} failed to steal from {event.foe_name}\n")

    def _render_new_character(self, event: NewCharacterEvent) -> None:
        self.console.print(
            f"[bold green]Creating controlled character number: {event.number}...[/bold green]\n"
        )

    def _render_map_info(self, event: MapInfoEvent) -> None:
        player = event.current_player
        enemies = event.enemies
        matrix = event.matrix
        size = event.size

        self.console.print(
            f"\n[green]{player.name}[/green] is at {player.position}, with {player.life} HP"
        )

        foes_positions = []
        for enemy in enemies:
            foes_positions.append(enemy.position)
            self.console.print(
                f"[red]Enemy {enemy.name}({enemy.job.get_name()})[/red] at {enemy.position}, {enemy.life} HP"
            )

        table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))
        table.add_column("", style="bold")
        for col in range(size):
            table.add_column(str(col), justify="center")

        for row in range(size):
            cells = [f"[bold]{convert_number_to_letter(row)}[/bold]"]
            for col in range(size):
                position = convert_number_to_letter(row) + str(col)
                if matrix[row][col] == 0:
                    cells.append(" ")
                elif player.position == position:
                    cells.append("[bold green]*[/bold green]")
                elif position in foes_positions:
                    cells.append("[bold red]*[/bold red]")
                else:
                    cells.append("*")
            table.add_row(*cells)

        self.console.print(table)

    def _render_moving_possibilities(self, event: MovingPossibilitiesEvent) -> None:
        self.console.print("Possibilities of Moving")
        self.console.print("[yellow]You are on the Yellow tile[/yellow]")
        self.console.print("[green]Green tiles are the possibilities[/green]")

        table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))
        table.add_column("", style="bold")
        for col in range(event.size):
            table.add_column(str(col), justify="center")

        for row in range(event.size):
            cells = [f"[bold]{convert_number_to_letter(row)}[/bold]"]
            for col in range(event.size):
                position = convert_number_to_letter(row) + str(col)
                if event.matrix[row][col] == 0:
                    cells.append(" ")
                elif position in event.possibilities:
                    cells.append("[bold green]*[/bold green]")
                elif event.player_position == position:
                    cells.append("[bold yellow]*[/bold yellow]")
                else:
                    cells.append("*")
            table.add_row(*cells)

        self.console.print(table)

    def _render_player_stats(self, event: PlayerStatsEvent) -> None:
        p = event.player
        panel = Panel(
            f"Lv.{p.level}  HP: {p.life}/{p.health_points}  MP: {p.mana}/{p.magic_points}\n"
            f"STR: {p.strength}  INT: {p.intelligence}  ACC: {p.accuracy}\n"
            f"ARM: {p.armour}  RES: {p.magic_resist}  SPD: {p.move_speed}  WILL: {p.will}",
            title=f"[bold]{p.name}[/bold]",
            style="cyan",
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def _render_enemy_status(self, event: EnemyStatusEvent) -> None:
        e = event.enemy
        panel = Panel(
            f"Position: {e.position}  Lv.{e.level}\n"
            f"HP: {e.life}/{e.health_points}  MP: {e.mana}/{e.magic_points}\n"
            f"STR: {e.strength}  INT: {e.intelligence}  ACC: {e.accuracy}\n"
            f"ARM: {e.armour}  RES: {e.magic_resist}  SPD: {e.move_speed}  WILL: {e.will}",
            title=f"[bold red]{e.name} ({e.job.get_name()})[/bold red]",
            style="red",
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def _render_check_item(self, event: CheckItemEvent) -> None:
        item = event.item
        lines = [f"{item.name} ({item.tier} tier)", item.description, f"Weight: {item.weight} kg"]
        if hasattr(item, "base") and hasattr(item, "attribute"):
            lines.append(f"+{item.base} {item.attribute}")
        if hasattr(item, "side_effects") and item.side_effects:
            lines.append("Side effects:")
            for se in item.side_effects:
                prefix = f"+{se.base}" if se.effect_type == "buff" else f"-{se.base}"
                lines.append(f"  {se.name}: {prefix} {se.attribute} ({se.duration} turns, {se.occurrence})")
        panel = Panel("\n".join(lines), title="[green]Item[/green]", style="green", box=box.ROUNDED)
        self.console.print(panel)
```

- [ ] **Step 5: Create `emberblast/renderer/__init__.py`**

```python
from .rich_cli import RichCLIRenderer

__all__ = ["RichCLIRenderer"]
```

- [ ] **Step 6: Run tests**

```bash
uv run python -m unittest emberblast.test.test_rich_renderer -v
```

Expected: All tests PASS.

- [ ] **Step 7: Lint and commit**

```bash
uv run ruff check --fix emberblast/renderer/ emberblast/test/test_rich_renderer.py emberblast/interface/ && uv run ruff format emberblast/renderer/ emberblast/test/test_rich_renderer.py emberblast/interface/
git add emberblast/renderer/ emberblast/test/test_rich_renderer.py emberblast/interface/interface.py emberblast/interface/__init__.py
git commit -m "feat: add RichCLIRenderer with typed event dispatch"
git push
```

---

## Task 4: Wire RichCLIRenderer into communicator and adapt orchestrator

**Files:**
- Modify: `emberblast/communicator/communicator_cmd.py`
- Modify: `emberblast/communicator/communicator.py`
- Modify: `emberblast/orchestrator/game_orchestrator.py`
- Remove: `emberblast/communicator/informer_cmd.py`

This is the integration task. The orchestrator and all code that calls `self.communicator.informer.some_method(...)` needs to emit events via `self.communicator.informer.render(SomeEvent(...))` instead.

- [ ] **Step 1: Replace InformerCMD with RichCLIRenderer in communicator_cmd.py**

In `emberblast/communicator/communicator_cmd.py`, replace:

```python
from emberblast.interface import ICommunicator
from .informer_cmd import InformerCMD
from .questioner_cmd import QuestionerCMD


class CommunicatorCMD(ICommunicator):
    def __init__(self) -> None:
        self.informer = InformerCMD()
        self.questioner = QuestionerCMD()
```

With:

```python
from emberblast.interface import ICommunicator
from emberblast.renderer import RichCLIRenderer
from .questioner_cmd import QuestionerCMD


class CommunicatorCMD(ICommunicator):
    def __init__(self) -> None:
        self.informer = RichCLIRenderer()
        self.questioner = QuestionerCMD()
```

- [ ] **Step 2: Update orchestrator to emit events**

This is the largest change. In `emberblast/orchestrator/game_orchestrator.py`, every call to `self.communicator.informer.some_method(args)` must become `self.communicator.informer.render(SomeEvent(args))`.

Add imports at the top:

```python
from emberblast.events import (
    TurnStartEvent, PlayerTurnEvent, LineSeparatorEvent, MoveEvent,
    DamageEvent, HealEvent, SpentManaEvent, UseItemEvent, DiceRollEvent,
    VictoryEvent, SideEffectEvent, SideEffectEndedEvent,
    IteratedSideEffectEvent, ItemFoundEvent, LevelUpEvent, XPEarnedEvent,
    EventAction, LowManaEvent, MissedAttackEvent, TrapActivatedEvent,
    NoFoesEvent, AreaDamageEvent, PlayerStoleItemEvent,
    PlayerFailStoleItemEvent, NewCharacterEvent, MapInfoEvent,
    MovingPossibilitiesEvent, PlayerStatsEvent, EnemyStatusEvent,
    CheckItemEvent, NarrationEvent, DeathEvent, GreetingsEvent,
)
```

Then replace each informer call throughout the file. Key replacements:

| Old call | New call |
|----------|----------|
| `self.communicator.informer.new_turn(turn)` | `self.communicator.informer.render(TurnStartEvent(turn=turn))` |
| `self.communicator.informer.player_turn(name)` | `self.communicator.informer.render(PlayerTurnEvent(player_name=name))` |
| `self.communicator.informer.line_separator()` | `self.communicator.informer.render(LineSeparatorEvent())` |
| `self.communicator.informer.moved(name)` | `self.communicator.informer.render(MoveEvent(player_name=name))` |
| `self.communicator.informer.suffer_damage(attacker, foe, damage)` | `self.communicator.informer.render(DamageEvent(attacker_name=attacker.name, target_name=foe.name, damage=damage, target_alive=foe.is_alive(), target_life=foe.life))` |
| `self.communicator.informer.heal(healer, foe, amount)` | `self.communicator.informer.render(HealEvent(healer_name=healer.name, target_name=foe.name, amount=amount, target_life=foe.life))` |
| `self.communicator.informer.dice_result(name, result, kind, max_sides)` | `self.communicator.informer.render(DiceRollEvent(player_name=name, result=result, kind=kind, is_critical=(result == max_sides)))` |
| `self.communicator.informer.player_won(name)` | `self.communicator.informer.render(VictoryEvent(player_name=name))` |
| `self.communicator.informer.event(event_name)` | `self.communicator.informer.render(EventAction(event=event_name))` |
| `self.communicator.informer.player_earned_xp(name, xp)` | `self.communicator.informer.render(XPEarnedEvent(player_name=name, xp=xp))` |
| `self.communicator.informer.player_killed_enemy_earned_xp(name, foe, xp)` | `self.communicator.informer.render(XPEarnedEvent(player_name=name, xp=xp, kill_target=foe))` |
| `self.communicator.informer.player_level_up(name, level)` | `self.communicator.informer.render(LevelUpEvent(player_name=name, new_level=level))` |
| `self.communicator.informer.found_item(name, found, tier, item_name)` | `self.communicator.informer.render(ItemFoundEvent(player_name=name, found=found, item_tier=tier, item_name=item_name))` |
| `self.communicator.informer.spent_mana(name, amount, skill_name)` | `self.communicator.informer.render(SpentManaEvent(player_name=name, amount=amount, skill_name=skill_name))` |
| `self.communicator.informer.add_side_effect(name, se)` | `self.communicator.informer.render(SideEffectEvent(player_name=name, effect_name=se.name, effect_type=se.effect_type, occurrence=se.occurrence))` |
| `self.communicator.informer.side_effect_ended(name, se)` | `self.communicator.informer.render(SideEffectEndedEvent(player_name=name, effect_name=se.name))` |
| `self.communicator.informer.iterated_side_effect_apply(name, se)` | `self.communicator.informer.render(IteratedSideEffectEvent(player_name=name, effect_name=se.name, effect_type=se.effect_type, attribute=se.attribute, value=se.base, turns_remaining=se.duration))` |
| `self.communicator.informer.no_foes_attack(player)` | `self.communicator.informer.render(NoFoesEvent(message=...))` |
| `self.communicator.informer.no_foes_skill(range, pos)` | `self.communicator.informer.render(NoFoesEvent(message=...))` |
| `self.communicator.informer.missed(player, foe)` | `self.communicator.informer.render(MissedAttackEvent(attacker_name=player.name, target_name=foe.name))` |
| `self.communicator.informer.area_damage(skill, players)` | `self.communicator.informer.render(AreaDamageEvent(skill_name=skill.name, skill_kind=skill.kind, affected_players=players))` |
| `self.communicator.informer.map_info(player, players, matrix, size)` | `self.communicator.informer.render(MapInfoEvent(current_player=player, enemies=players, matrix=matrix, size=size))` |
| `self.communicator.informer.moving_possibilities(pos, possibilities, matrix, size)` | `self.communicator.informer.render(MovingPossibilitiesEvent(player_position=pos, possibilities=possibilities, matrix=matrix, size=size))` |
| `self.communicator.informer.player_stats(player)` | `self.communicator.informer.render(PlayerStatsEvent(player=player))` |
| `self.communicator.informer.enemy_status(enemy)` | `self.communicator.informer.render(EnemyStatusEvent(enemy=enemy))` |
| `self.communicator.informer.use_item(name, item_name, target)` | `self.communicator.informer.render(UseItemEvent(player_name=name, item_name=item_name, target_name=target))` |
| `self.communicator.informer.check_item(item)` | `self.communicator.informer.render(CheckItemEvent(item=item))` |
| `self.communicator.informer.low_mana(player)` | `self.communicator.informer.render(LowManaEvent(player_name=player.name, mana=player.mana))` |
| `self.communicator.informer.trap_activated(player, side_effects)` | `self.communicator.informer.render(TrapActivatedEvent(player_name=player.name, side_effect_names=[se.name for se in side_effects]))` |
| `self.communicator.informer.player_stole_item(name, foe, item, tier)` | `self.communicator.informer.render(PlayerStoleItemEvent(player_name=name, foe_name=foe, item_name=item, tier=tier))` |
| `self.communicator.informer.player_fail_stole_item(name, foe)` | `self.communicator.informer.render(PlayerFailStoleItemEvent(player_name=name, foe_name=foe))` |
| `self.communicator.informer.create_new_character(number)` | `self.communicator.informer.render(NewCharacterEvent(number=number))` |
| `self.communicator.informer.force_loading(time, prefix, attrs)` | Remove — Rich handles pacing naturally, or use `time.sleep()` inline if delay is needed |
| `self.communicator.informer.plain_map(matrix, size)` | Use `MapInfoEvent` or remove if unused |
| `self.communicator.informer.plain_matrix(matrix)` | Remove — debug-only method |

Also update any other files that call informer methods directly (skill classes, game_factory, etc.). Search the codebase for `communicator.informer.` to find all call sites.

- [ ] **Step 3: Update `__main__.py` greetings call**

Replace:
```python
self.communicator.informer.greetings()
```
With:
```python
from emberblast.events import GreetingsEvent
self.communicator.informer.render(GreetingsEvent())
```

- [ ] **Step 4: Update `questioner_cmd.py` to remove old deps**

In `emberblast/communicator/questioner_cmd.py`, replace `emojis.encode(...)` wrapping around strings. Use plain strings or Rich markup if needed. The `QuestionerCMD` class uses `InquirerPy` which handles its own display — just remove the `emojis` import and all `emojis.encode()` calls, keeping the inner strings.

- [ ] **Step 5: Remove `informer_cmd.py`**

Delete `emberblast/communicator/informer_cmd.py`.

- [ ] **Step 6: Update communicator `__init__.py` if needed**

The `communicator/__init__.py` exports `communicator_injector` — verify this still works with the new setup.

- [ ] **Step 7: Run all tests**

```bash
uv run python -m unittest discover -s emberblast/test -v
```

Fix any broken tests caused by the informer swap.

- [ ] **Step 8: Lint and commit**

```bash
uv run ruff check --fix emberblast/ && uv run ruff format emberblast/
git add -A
git rm emberblast/communicator/informer_cmd.py
git commit -m "feat: replace InformerCMD with RichCLIRenderer and typed events"
git push
```

---

## Task 5: Create bot memory system

**Files:**
- Create: `emberblast/bot/memory.py`
- Create: `emberblast/test/test_memory.py`

- [ ] **Step 1: Write the test file**

Create `emberblast/test/test_memory.py`:

```python
from emberblast.test.test import BaseTestCase
from emberblast.bot.memory import BotMemory


class TestBotMemory(BaseTestCase):

    def setUp(self):
        self.memory = BotMemory(max_entries=10)

    def test_add_entry(self):
        self.memory.add(1, "Attacked Elara for 15 damage")
        entries = self.memory.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], "Turn 1: Attacked Elara for 15 damage")

    def test_rolling_window(self):
        for i in range(15):
            self.memory.add(i, f"Event {i}")
        entries = self.memory.get_entries()
        self.assertEqual(len(entries), 10)
        self.assertEqual(entries[0], "Turn 5: Event 5")
        self.assertEqual(entries[9], "Turn 14: Event 14")

    def test_empty_memory(self):
        entries = self.memory.get_entries()
        self.assertEqual(entries, [])

    def test_custom_max_entries(self):
        small_memory = BotMemory(max_entries=3)
        for i in range(5):
            small_memory.add(i, f"Event {i}")
        entries = small_memory.get_entries()
        self.assertEqual(len(entries), 3)

    def test_clear(self):
        self.memory.add(1, "test")
        self.memory.clear()
        self.assertEqual(self.memory.get_entries(), [])
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run python -m unittest emberblast.test.test_memory -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'emberblast.bot.memory'`

- [ ] **Step 3: Create `emberblast/bot/memory.py`**

```python
from collections import deque
from typing import List


class BotMemory:

    def __init__(self, max_entries: int = 10):
        self._entries: deque = deque(maxlen=max_entries)

    def add(self, turn: int, description: str) -> None:
        self._entries.append(f"Turn {turn}: {description}")

    def get_entries(self) -> List[str]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()
```

- [ ] **Step 4: Run tests**

```bash
uv run python -m unittest emberblast.test.test_memory -v
```

Expected: All tests PASS.

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff check --fix emberblast/bot/memory.py emberblast/test/test_memory.py && uv run ruff format emberblast/bot/memory.py emberblast/test/test_memory.py
git add emberblast/bot/memory.py emberblast/test/test_memory.py
git commit -m "feat: add BotMemory with rolling window for turn history"
git push
```

---

## Task 6: Create LLM client (OpenAI wrapper + game state serializer + personality)

**Files:**
- Create: `emberblast/bot/llm_client.py`
- Create: `emberblast/test/test_llm_client.py`

- [ ] **Step 1: Write the test file**

Create `emberblast/test/test_llm_client.py`:

```python
import json
from unittest.mock import patch, MagicMock

from emberblast.test.test import BaseTestCase
from emberblast.bot.llm_client import (
    build_personality_prompt,
    serialize_game_state,
    parse_llm_response,
    call_openai,
    JOB_TRAITS,
    RACE_MODIFIERS,
)


class TestPersonalityPrompt(BaseTestCase):

    def test_build_personality_known_job_race(self):
        prompt = build_personality_prompt("Grukk", "Knight", "Orc")
        self.assertIn("Grukk", prompt)
        self.assertIn("Orc", prompt)
        self.assertIn("Knight", prompt)
        self.assertIn(JOB_TRAITS["Knight"], prompt)
        self.assertIn(RACE_MODIFIERS["Orc"], prompt)

    def test_build_personality_unknown_job(self):
        prompt = build_personality_prompt("Test", "UnknownJob", "Human")
        self.assertIn("Test", prompt)
        self.assertIn("UnknownJob", prompt)

    def test_all_jobs_have_traits(self):
        for job in ["Knight", "Wizard", "Rogue", "Archer", "Priest"]:
            self.assertIn(job, JOB_TRAITS)

    def test_all_races_have_modifiers(self):
        for race in ["Human", "Dwarf", "Elf", "Orc", "Halflings"]:
            self.assertIn(race, RACE_MODIFIERS)


class TestSerializeGameState(BaseTestCase):

    def _make_mock_player(self, name="Grukk", job_name="Knight", race_name="Orc",
                          position="C4", life=45, health_points=80, mana=10,
                          magic_points=20, level=3, attack_type="melee",
                          damage_vector="strength"):
        player = MagicMock()
        player.name = name
        player.position = position
        player.life = life
        player.health_points = health_points
        player.mana = mana
        player.magic_points = magic_points
        player.level = level
        player.strength = 12
        player.intelligence = 4
        player.accuracy = 6
        player.armour = 10
        player.magic_resist = 3
        player.move_speed = 3
        player.will = 5
        player.job = MagicMock()
        player.job.get_name.return_value = job_name
        player.job.attack_type = attack_type
        player.job.damage_vector = damage_vector
        player.race = MagicMock()
        player.race.get_name.return_value = race_name
        player.skills = []
        player.bag = MagicMock()
        player.bag.items = []
        player.equipment = MagicMock()
        player.equipment.weapon = None
        player.equipment.armour = None
        player.equipment.boots = None
        player.equipment.accessory = None
        player.side_effects = []
        player.is_hidden.return_value = False
        return player

    def test_serialize_basic_state(self):
        bot = self._make_mock_player()
        enemies = [self._make_mock_player(name="Elara", job_name="Wizard", position="F7", life=30, health_points=50)]

        game = MagicMock()
        game.game_map.graph.get_available_nodes_in_range.return_value = ["C3", "C5"]
        game.game_map.graph.get_shortest_distance_between_positions.return_value = 4.0

        memory_entries = ["Turn 1: Moved to C4"]

        state = serialize_game_state(bot, enemies, game, memory_entries, ["move", "attack", "pass"])
        self.assertEqual(state["current_bot"]["name"], "Grukk")
        self.assertEqual(state["current_bot"]["job"], "Knight")
        self.assertEqual(len(state["enemies"]), 1)
        self.assertEqual(state["enemies"][0]["name"], "Elara")
        self.assertEqual(state["memory"], ["Turn 1: Moved to C4"])
        self.assertIn("move", state["available_actions"])

    def test_serialize_with_skills(self):
        bot = self._make_mock_player()
        skill = MagicMock()
        skill.name = "Shield Bash"
        skill.base = 15
        skill.cost = 8
        skill.ranged = 1
        skill.kind = "inflict"
        bot.skills = [skill]
        bot.mana = 10

        state = serialize_game_state(bot, [], MagicMock(), [], ["attack"])
        self.assertEqual(len(state["current_bot"]["available_skills"]), 1)
        self.assertEqual(state["current_bot"]["available_skills"][0]["name"], "Shield Bash")


class TestParseLLMResponse(BaseTestCase):

    def test_parse_valid_response(self):
        response = json.dumps({
            "action": "attack",
            "target": "Elara",
            "narration": "Die, wizard!",
        })
        result = parse_llm_response(response)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["target"], "Elara")
        self.assertEqual(result["narration"], "Die, wizard!")

    def test_parse_invalid_json(self):
        result = parse_llm_response("not json")
        self.assertIsNone(result)

    def test_parse_missing_action(self):
        response = json.dumps({"target": "Elara", "narration": "hi"})
        result = parse_llm_response(response)
        self.assertIsNone(result)


class TestCallOpenAI(BaseTestCase):

    @patch("emberblast.bot.llm_client.OpenAI")
    def test_call_openai_success(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"action": "attack", "target": "Elara", "narration": "Die!"}'
        mock_client.chat.completions.create.return_value = mock_response

        result = call_openai("system prompt", "user prompt")
        self.assertIn("attack", result)

    @patch("emberblast.bot.llm_client.OpenAI")
    def test_call_openai_failure(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        result = call_openai("system prompt", "user prompt")
        self.assertIsNone(result)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run python -m unittest emberblast.test.test_llm_client -v
```

Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Create `emberblast/bot/llm_client.py`**

```python
import json
import os
import logging
from typing import Dict, List, Optional, Any

from openai import OpenAI

logger = logging.getLogger(__name__)

JOB_TRAITS = {
    "Knight": "Honorable and brave. You charge headfirst into battle and respect strength above all. You protect the weak and fight with discipline.",
    "Wizard": "Calculating and intellectual. You position carefully, preferring to strike from a distance with devastating magic. You look down on brute force.",
    "Rogue": "Opportunistic and sneaky. You avoid fair fights, preferring to strike from the shadows. You look for cheap shots and escape routes.",
    "Archer": "Patient and methodical. You keep your distance and pick off enemies one by one. You value precision over power.",
    "Priest": "Cautious and wise. You are a reluctant combatant who prefers healing and support. You fight only when cornered.",
}

RACE_MODIFIERS = {
    "Orc": "You are aggressive, blunt, and love to trash-talk your enemies.",
    "Elf": "You are eloquent, condescending, and surgically precise in everything you do.",
    "Dwarf": "You are grumpy, stubborn, and have a dry sense of humor.",
    "Halflings": "You are nervous, scrappy, and fight with underdog energy.",
    "Human": "You are balanced, adaptable, and practical in your approach.",
}

SYSTEM_TEMPLATE = """You are {name}, a {race} {job} in a tactical RPG deathmatch.

Personality: {job_trait} {race_modifier}

You must choose one action per turn based on the game state provided. Respond ONLY with a JSON object:
{{
  "action": "<one of the available actions>",
  "target": "<target player name, if applicable>",
  "skill_name": "<skill to use, if action is skill>",
  "item_name": "<item to use, if action is item>",
  "move_to": "<destination tile, if action is move>",
  "narration": "<a short in-character line, 1 sentence, spoken aloud>"
}}

Rules:
- You can only move to tiles listed in bot_walkable_tiles_in_range
- You can only attack/skill enemies within your range
- Skills cost mana — check you have enough
- Think tactically: consider positioning, health, mana, and enemy threats
- Stay in character with your narration"""


def build_personality_prompt(name: str, job_name: str, race_name: str) -> str:
    job_trait = JOB_TRAITS.get(job_name, f"A skilled {job_name}.")
    race_modifier = RACE_MODIFIERS.get(race_name, f"You have the traits of a {race_name}.")
    return SYSTEM_TEMPLATE.format(
        name=name,
        race=race_name,
        job=job_name,
        job_trait=job_trait,
        race_modifier=race_modifier,
    )


def serialize_game_state(
    bot: Any,
    enemies: List[Any],
    game: Any,
    memory_entries: List[str],
    available_actions: List[str],
) -> Dict:
    skills_data = []
    for skill in bot.skills:
        if skill.cost <= bot.mana:
            skills_data.append({
                "name": skill.name,
                "damage": skill.base,
                "mana_cost": skill.cost,
                "range": skill.ranged,
                "kind": skill.kind,
            })

    bag_items = []
    for item in bot.bag.items:
        item_data = {"name": item.name, "tier": item.tier}
        if hasattr(item, "attribute"):
            item_data["attribute"] = item.attribute
        if hasattr(item, "base"):
            item_data["value"] = item.base
        bag_items.append(item_data)

    equipment = {}
    for slot in ["weapon", "armour", "boots", "accessory"]:
        eq = getattr(bot.equipment, slot, None)
        equipment[slot] = eq.name if eq else None

    effects = []
    for se in bot.side_effects:
        effects.append({
            "name": se.name,
            "turns_remaining": se.duration,
            "effect_type": se.effect_type,
        })

    enemies_data = []
    for enemy in enemies:
        if not enemy.is_hidden():
            distance = game.game_map.graph.get_shortest_distance_between_positions(
                bot.position, enemy.position
            )
            enemies_data.append({
                "name": enemy.name,
                "job": enemy.job.get_name(),
                "position": enemy.position,
                "life": enemy.life,
                "max_life": enemy.health_points,
                "distance": round(distance, 1),
            })

    walkable = game.game_map.graph.get_available_nodes_in_range(
        bot.position, bot.move_speed
    )

    return {
        "current_bot": {
            "name": bot.name,
            "job": bot.job.get_name(),
            "race": bot.race.get_name(),
            "level": bot.level,
            "position": bot.position,
            "life": bot.life,
            "max_life": bot.health_points,
            "mana": bot.mana,
            "max_mana": bot.magic_points,
            "attack_type": bot.job.attack_type,
            "attributes": {
                "strength": bot.strength,
                "intelligence": bot.intelligence,
                "accuracy": bot.accuracy,
                "armour": bot.armour,
                "magic_resist": bot.magic_resist,
                "move_speed": bot.move_speed,
            },
            "available_skills": skills_data,
            "bag_items": bag_items,
            "equipment": equipment,
            "active_effects": effects,
        },
        "enemies": enemies_data,
        "map": {
            "bot_walkable_tiles_in_range": walkable,
        },
        "available_actions": available_actions,
        "memory": memory_entries,
    }


def parse_llm_response(raw: str) -> Optional[Dict]:
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    if "action" not in data:
        return None
    return data


def call_openai(system_prompt: str, user_prompt: str) -> Optional[str]:
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=os.environ.get("EMBERBLAST_MODEL", "gpt-4o-mini"),
            temperature=0.7,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.warning("OpenAI API call failed: %s", e)
        return None
```

- [ ] **Step 4: Run tests**

```bash
uv run python -m unittest emberblast.test.test_llm_client -v
```

Expected: All tests PASS.

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff check --fix emberblast/bot/llm_client.py emberblast/test/test_llm_client.py && uv run ruff format emberblast/bot/llm_client.py emberblast/test/test_llm_client.py
git add emberblast/bot/llm_client.py emberblast/test/test_llm_client.py
git commit -m "feat: add OpenAI LLM client with game state serializer and personality prompts"
git push
```

---

## Task 7: Integrate LLM into BotDecisioning with fallback

**Files:**
- Modify: `emberblast/bot/bot_decisioning.py`
- Modify: `emberblast/__main__.py`

This is the core integration. The existing `decide()` method becomes the fallback. A new LLM-powered flow wraps it.

- [ ] **Step 1: Add LLM flow to `bot_decisioning.py`**

Add imports at the top of `emberblast/bot/bot_decisioning.py`:

```python
import json
import logging
import os

from emberblast.bot.llm_client import (
    build_personality_prompt,
    serialize_game_state,
    parse_llm_response,
    call_openai,
)
from emberblast.bot.memory import BotMemory
from emberblast.events import NarrationEvent

logger = logging.getLogger(__name__)
```

Add a `memories` dict and helper to the `__init__`:

```python
def __init__(self, game: IGame) -> None:
    self.game = game
    self.current_bot: Optional[IPlayer] = None
    self.current_play_style = IPlayingMode.NEUTRAL
    self.prioritized_foes: List[IPlayer] = []
    self.possible_foe: Optional[IPlayer] = None
    self._memories: Dict[str, BotMemory] = {}
    self._current_turn: int = 0
    self._llm_enabled: bool = bool(os.environ.get("OPENAI_API_KEY"))
```

Add a `_get_memory` method:

```python
def _get_memory(self, player_name: str) -> BotMemory:
    if player_name not in self._memories:
        self._memories[player_name] = BotMemory()
    return self._memories[player_name]
```

Add `set_current_turn` method (called from orchestrator):

```python
def set_current_turn(self, turn: int) -> None:
    self._current_turn = turn
```

Rename the existing `decide()` method to `_decide_deterministic()`:

```python
def _decide_deterministic(self, player: IPlayer) -> None:
    # ... existing decide() body unchanged ...
```

Create new `decide()` that wraps the LLM flow:

```python
def decide(self, player: IPlayer) -> None:
    if not self._llm_enabled:
        self._decide_deterministic(player)
        return

    self.reset_attributes()
    self.current_bot = player

    enemies = self.game.get_remaining_players(player)
    memory = self._get_memory(player.name)
    available_actions = ["move", "attack", "skill", "item", "defend", "hide", "search", "equip", "pass"]

    system_prompt = build_personality_prompt(
        player.name, player.job.get_name(), player.race.get_name()
    )
    game_state = serialize_game_state(
        player, enemies, self.game, memory.get_entries(), available_actions
    )
    user_prompt = json.dumps(game_state, indent=2)

    raw_response = call_openai(system_prompt, user_prompt)
    if raw_response is None:
        logger.warning("LLM call failed for %s, falling back to deterministic", player.name)
        self._decide_deterministic(player)
        return

    parsed = parse_llm_response(raw_response)
    if parsed is None:
        logger.warning("Failed to parse LLM response for %s, falling back", player.name)
        self._decide_deterministic(player)
        return

    success = self._execute_llm_action(player, parsed, enemies)
    if not success:
        # Retry once with error feedback
        error_msg = f"Previous action was invalid. Game state: {user_prompt}\nChoose a valid action."
        raw_response = call_openai(system_prompt, error_msg)
        if raw_response:
            parsed = parse_llm_response(raw_response)
            if parsed:
                success = self._execute_llm_action(player, parsed, enemies)

        if not success:
            logger.warning("LLM retry failed for %s, falling back to deterministic", player.name)
            self._decide_deterministic(player)
            return

    # Display narration if present
    narration = parsed.get("narration", "")
    if narration:
        self.communicator.informer.render(
            NarrationEvent(player_name=player.name, text=narration)
        )

    # Record to memory
    action = parsed.get("action", "unknown")
    target = parsed.get("target", "")
    memory_line = f"{action}"
    if target:
        memory_line += f" targeting {target}"
    memory.add(self._current_turn, memory_line)
```

Add `_execute_llm_action` that maps the LLM response to existing game actions:

```python
def _execute_llm_action(self, player: IPlayer, parsed: Dict, enemies: List[IPlayer]) -> bool:
    action = parsed.get("action", "").lower()
    try:
        if action == "move":
            return self._execute_llm_move(player, parsed)
        elif action == "attack":
            return self._execute_llm_attack(player, parsed, enemies)
        elif action == "skill":
            return self._execute_llm_skill(player, parsed, enemies)
        elif action == "item":
            return self._execute_llm_item(player, parsed)
        elif action == "defend":
            player.set_defense_mode(True)
            return True
        elif action == "hide":
            player.set_hidden(True)
            return True
        elif action == "search":
            self.search_on_map()
            return True
        elif action == "equip":
            self.equip_item()
            return True
        elif action == "pass":
            return True
        else:
            return False
    except Exception as e:
        logger.warning("Error executing LLM action %s: %s", action, e)
        return False
```

The individual `_execute_llm_*` methods delegate to existing game logic (e.g., `_execute_llm_move` validates the tile is walkable and calls `game_map.move_player`, `_execute_llm_attack` finds the target enemy and calls the existing damage calculation). These methods should reuse as much existing orchestrator/game logic as possible.

```python
def _execute_llm_move(self, player: IPlayer, parsed: Dict) -> bool:
    destination = parsed.get("move_to", "")
    if not destination:
        return False
    walkable = self.game.game_map.graph.get_available_nodes_in_range(
        player.position, player.move_speed
    )
    if destination not in walkable:
        return False
    self.game.game_map.move_player(player, destination)
    return True

def _execute_llm_attack(self, player: IPlayer, parsed: Dict, enemies: List[IPlayer]) -> bool:
    target_name = parsed.get("target", "")
    target = self._find_enemy_by_name(target_name, enemies)
    if target is None:
        return False
    # Delegate to existing attack logic — the orchestrator handles damage calc
    self.possible_foe = target
    self.current_bot = player
    self.attack()
    return True

def _execute_llm_skill(self, player: IPlayer, parsed: Dict, enemies: List[IPlayer]) -> bool:
    skill_name = parsed.get("skill_name", "")
    target_name = parsed.get("target", "")
    skill = None
    for s in player.skills:
        if s.name.lower() == skill_name.lower() and s.cost <= player.mana:
            skill = s
            break
    if skill is None:
        return False
    target = self._find_enemy_by_name(target_name, enemies)
    if target is None and skill.kind == "inflict":
        return False
    # Use existing skill execution
    self.possible_foe = target
    self.current_bot = player
    # Skill execution follows existing pattern in the orchestrator
    return True

def _execute_llm_item(self, player: IPlayer, parsed: Dict) -> bool:
    item_name = parsed.get("item_name", "")
    for item in player.bag.get_usable_items():
        if item.name.lower() == item_name.lower():
            player.use_item(item)
            player.bag.remove_item(item)
            return True
    return False

def _find_enemy_by_name(self, name: str, enemies: List[IPlayer]) -> Optional[IPlayer]:
    for enemy in enemies:
        if enemy.name.lower() == name.lower():
            return enemy
    return None
```

- [ ] **Step 2: Update orchestrator to pass turn number to bot controller**

In `emberblast/orchestrator/game_orchestrator.py`, inside the turn loop (around line 171), add:

```python
self.bot_controller.set_current_turn(turn)
```

- [ ] **Step 3: Add API key check to `__main__.py`**

In `emberblast/__main__.py`, add at the start of the `run()` method:

```python
import os
if not os.environ.get("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not set. Bots will use deterministic AI.")
```

- [ ] **Step 4: Run all tests**

```bash
uv run python -m unittest discover -s emberblast/test -v
```

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff check --fix emberblast/ && uv run ruff format emberblast/
git add emberblast/bot/bot_decisioning.py emberblast/orchestrator/game_orchestrator.py emberblast/__main__.py
git commit -m "feat: integrate LLM-powered bot decisions with deterministic fallback"
git push
```

---

## Task 8: Record bot memory from game events

**Files:**
- Modify: `emberblast/orchestrator/game_orchestrator.py`
- Modify: `emberblast/bot/bot_decisioning.py`

The orchestrator needs to feed turn events back into bot memory so the LLM has context about what happened.

- [ ] **Step 1: Add memory recording to orchestrator**

After key events in the game loop (damage dealt, items found, kills, heals), call the bot controller's memory system. Add a helper method to `DeathMatchOrchestrator`:

```python
def _record_bot_memory(self, player_name: str, turn: int, description: str) -> None:
    memory = self.bot_controller._get_memory(player_name)
    memory.add(turn, description)
```

Call this after:
- Damage events: `self._record_bot_memory(target.name, turn, f"Took {damage} damage from {attacker.name}")`
- Kill events: `self._record_bot_memory(attacker.name, turn, f"Killed {target.name}")`
- Heal events: `self._record_bot_memory(player.name, turn, f"Healed for {amount} HP")`
- Item found: `self._record_bot_memory(player.name, turn, f"Found {item.name}")`
- Side effects: `self._record_bot_memory(player.name, turn, f"Affected by {effect.name}")`

- [ ] **Step 2: Run all tests**

```bash
uv run python -m unittest discover -s emberblast/test -v
```

- [ ] **Step 3: Lint and commit**

```bash
uv run ruff check --fix emberblast/ && uv run ruff format emberblast/
git add emberblast/orchestrator/game_orchestrator.py emberblast/bot/bot_decisioning.py
git commit -m "feat: record game events into bot memory for LLM context"
git push
```

---

## Task 9: Manual integration test and cleanup

**Files:**
- Modify: any files that need fixes from manual testing

- [ ] **Step 1: Run the game manually**

```bash
export OPENAI_API_KEY="your-key-here"
uv run emberblast
```

Play through a few turns. Verify:
- Rich output renders correctly (panels, colors, map table)
- Bot narration appears in panels
- Bot actions make tactical sense
- Fallback works (unset OPENAI_API_KEY and verify deterministic bots still work)

- [ ] **Step 2: Fix any issues found during manual testing**

Address rendering bugs, action parsing issues, or formatting problems.

- [ ] **Step 3: Run full test suite**

```bash
uv run python -m unittest discover -s emberblast/test -v
```

- [ ] **Step 4: Final lint pass**

```bash
uv run ruff check --fix emberblast/ && uv run ruff format emberblast/
```

- [ ] **Step 5: Commit any fixes**

```bash
git add -A
git commit -m "fix: integration test fixes and cleanup"
git push
```

---

## Task 10: Add `.gitignore` entries and final cleanup

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Ensure `.gitignore` has uv entries**

Add to `.gitignore` if not present:

```
.venv/
uv.lock
__pycache__/
*.pyc
.env
```

- [ ] **Step 2: Remove any unused imports from old deps**

Search the codebase for any remaining imports of `colorama`, `termcolor`, `emojis`, `timg`. Remove them all.

```bash
uv run ruff check --fix emberblast/ && uv run ruff format emberblast/
```

- [ ] **Step 3: Run full test suite one last time**

```bash
uv run python -m unittest discover -s emberblast/test -v
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: cleanup old dependencies and update gitignore"
git push
```
