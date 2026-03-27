from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from emberblast.events import (
    AreaDamageEvent,
    CheckItemEvent,
    DamageEvent,
    DeathEvent,
    DiceRollEvent,
    EnemyStatusEvent,
    EventAction,
    GameEvent,
    GreetingsEvent,
    HealEvent,
    ItemFoundEvent,
    IteratedSideEffectEvent,
    LevelUpEvent,
    LineSeparatorEvent,
    LowManaEvent,
    MapInfoEvent,
    MissedAttackEvent,
    MoveEvent,
    MovingPossibilitiesEvent,
    NarrationEvent,
    NewCharacterEvent,
    NoFoesEvent,
    PlayerFailStoleItemEvent,
    PlayerStatsEvent,
    PlayerStoleItemEvent,
    PlayerTurnEvent,
    SideEffectEndedEvent,
    SideEffectEvent,
    SpentManaEvent,
    TrapActivatedEvent,
    TurnStartEvent,
    UseItemEvent,
    VictoryEvent,
    XPEarnedEvent,
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
            f"\t[red]{event.attacker_name}[/red] inflicted "
            f"[bold]{event.damage}[/bold] damage on "
            f"[red]{event.target_name}[/red]"
        )
        if not event.target_alive:
            self.console.print(f"\t[bold red]{event.target_name} is now dead[/bold red]")
        else:
            self.console.print(f"\t{event.target_name} now has {event.target_life} HP")

    def _render_heal(self, event: HealEvent) -> None:
        target = "itself" if event.healer_name == event.target_name else event.target_name
        self.console.print(f"\t[green]{event.healer_name}[/green] healed {target} for [bold]{event.amount}[/bold] HP!")
        self.console.print(f"\t{event.target_name} now has {event.target_life} HP")

    def _render_spent_mana(self, event: SpentManaEvent) -> None:
        self.console.print(f"\t{event.player_name} casted [blue]{event.skill_name}[/blue] for {event.amount} mana.")

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
        attribute = (
            "life"
            if event.attribute == "health_points"
            else ("mana" if event.attribute == "magic_points" else event.attribute)
        )
        self.console.print(
            f"\t{event.player_name} affected by "
            f"[magenta]{event.effect_name}[/magenta], "
            f"will {status} {attribute} by {event.value}/turn. "
            f"{event.turns_remaining} turns left.\n"
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
            self.console.print(f"\t{event.player_name} earned {event.xp} XP by killing {event.kill_target}!\n")
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
        self.console.print(f"{event.player_name} has [blue]{event.mana}[/blue] mana, consider healing it.")

    def _render_missed_attack(self, event: MissedAttackEvent) -> None:
        self.console.print(f"\t{event.attacker_name} tried to attack {event.target_name} but missed.")

    def _render_trap_activated(self, event: TrapActivatedEvent) -> None:
        self.console.print(f"\t[red]{event.player_name} has fallen into a trap![/red]")
        for name in event.side_effect_names:
            self.console.print(f"\t  - {name}")

    def _render_no_foes(self, event: NoFoesEvent) -> None:
        self.console.print(event.message)

    def _render_area_damage(self, event: AreaDamageEvent) -> None:
        self.console.print(f"\n\t[blue]{event.skill_name}[/blue] is an area {event.skill_kind} skill, hitting:")
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
        self.console.print(f"[bold green]Creating controlled character number: {event.number}...[/bold green]\n")

    def _render_map_info(self, event: MapInfoEvent) -> None:
        player = event.current_player
        enemies = event.enemies
        matrix = event.matrix
        size = event.size

        self.console.print(f"\n[green]{player.name}[/green] is at {player.position}, with {player.life} HP")

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
            f"Lv.{p.level}  HP: {p.life}/{p.health_points}  "
            f"MP: {p.mana}/{p.magic_points}\n"
            f"STR: {p.strength}  INT: {p.intelligence}  "
            f"ACC: {p.accuracy}\n"
            f"ARM: {p.armour}  RES: {p.magic_resist}  "
            f"SPD: {p.move_speed}  WILL: {p.will}",
            title=f"[bold]{p.name}[/bold]",
            style="cyan",
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def _render_enemy_status(self, event: EnemyStatusEvent) -> None:
        e = event.enemy
        panel = Panel(
            f"Position: {e.position}  Lv.{e.level}\n"
            f"HP: {e.life}/{e.health_points}  "
            f"MP: {e.mana}/{e.magic_points}\n"
            f"STR: {e.strength}  INT: {e.intelligence}  "
            f"ACC: {e.accuracy}\n"
            f"ARM: {e.armour}  RES: {e.magic_resist}  "
            f"SPD: {e.move_speed}  WILL: {e.will}",
            title=f"[bold red]{e.name} ({e.job.get_name()})[/bold red]",
            style="red",
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def _render_check_item(self, event: CheckItemEvent) -> None:
        item = event.item
        lines = [
            f"{item.name} ({item.tier} tier)",
            item.description,
            f"Weight: {item.weight} kg",
        ]
        if hasattr(item, "base") and hasattr(item, "attribute"):
            lines.append(f"+{item.base} {item.attribute}")
        if hasattr(item, "side_effects") and item.side_effects:
            lines.append("Side effects:")
            for se in item.side_effects:
                prefix = f"+{se.base}" if se.effect_type == "buff" else f"-{se.base}"
                lines.append(f"  {se.name}: {prefix} {se.attribute} ({se.duration} turns, {se.occurrence})")
        panel = Panel(
            "\n".join(lines),
            title="[green]Item[/green]",
            style="green",
            box=box.ROUNDED,
        )
        self.console.print(panel)
