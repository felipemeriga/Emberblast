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
    ItemEvent,
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
    SkillEvent,
    SpentManaEvent,
    TrapActivatedEvent,
    TurnStartEvent,
    UseItemEvent,
    VictoryEvent,
    XPEarnedEvent,
)
from emberblast.interface.interface import IRenderer


class TextualRenderer(IRenderer):
    """Renderer that dispatches GameEvent objects to a Textual app's widgets."""

    def __init__(self, app) -> None:
        self._app = app
        self._dispatch = {
            GreetingsEvent: self._render_greetings,
            TurnStartEvent: self._render_turn_start,
            PlayerTurnEvent: self._render_player_turn,
            LineSeparatorEvent: self._render_line_separator,
            MoveEvent: self._render_move,
            DamageEvent: self._render_damage,
            HealEvent: self._render_heal,
            SkillEvent: self._render_skill,
            SpentManaEvent: self._render_spent_mana,
            ItemEvent: self._render_item,
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

    def _refresh_game_state(self, player_name: str) -> None:
        """Pull current map/player data from the orchestrator and update widgets.

        Always shows the controlled player in the HUD, regardless of whose turn it is.
        The map shows all alive players with the active player highlighted.
        """
        orch = getattr(self._app, "_orchestrator", None)
        if not orch:
            return
        try:
            game = orch.game
            all_alive = game.get_all_alive_players()

            # Find the active player (whose turn it is) for map highlighting
            active = None
            for p in all_alive:
                if p.name == player_name:
                    active = p
                    break

            if active:
                others = [p for p in all_alive if p != active]
                self._app.update_map_from_event(active, others, game.game_map.graph.matrix, game.game_map.size)

            # Always update HUD with the controlled player, not whoever's turn it is
            friendly_names = set(getattr(self._app, "_friendly_names", []))
            controlled = None
            enemies_for_hud = []
            for p in all_alive:
                if p.name in friendly_names:
                    controlled = p
                else:
                    enemies_for_hud.append(p)

            if controlled:
                self._app.update_hud(controlled)
                self._app.update_enemies(enemies_for_hud)
        except Exception:
            pass

    def _render_greetings(self, event: GreetingsEvent) -> None:
        self._app.post_combat_log("Welcome to EMBERBLAST!", "system")

    def _render_turn_start(self, event: TurnStartEvent) -> None:
        self._app.set_turn(event.turn)
        # Update combat log turn tracker so entries get [T#] prefix
        try:
            log = self._app.screen.query_one("#combat-log")
            if hasattr(log, "set_turn"):
                log.set_turn(event.turn)
        except Exception:
            pass
        self._app.post_combat_log(f"Turn {event.turn} — Embrace Yourselves!", "turn")

    def _render_player_turn(self, event: PlayerTurnEvent) -> None:
        self._app.set_active_player(event.player_name)
        self._app.post_combat_log(f"{event.player_name}'s turn!", "turn")
        # Refresh map and HUD at each player turn
        self._refresh_game_state(event.player_name)

    def _render_line_separator(self, event: LineSeparatorEvent) -> None:
        self._app.post_combat_log("---", "system")

    def _render_move(self, event: MoveEvent) -> None:
        if event.from_position and event.to_position:
            msg = f"{event.player_name} moved from {event.from_position} to {event.to_position}"
        else:
            msg = f"{event.player_name} has just moved to another position"
        self._app.post_combat_log(msg, "move")
        self._app.refresh_map()

    def _render_damage(self, event: DamageEvent) -> None:
        msg = f"{event.attacker_name} inflicted {event.damage} damage on {event.target_name}"
        self._app.post_combat_log(msg, "damage")
        if not event.target_alive:
            self._app.post_combat_log(f"{event.target_name} is now dead", "death")
        else:
            self._app.post_combat_log(f"{event.target_name} now has {event.target_life} HP", "damage")
        self._app.refresh_huds()

    def _render_heal(self, event: HealEvent) -> None:
        target = "itself" if event.healer_name == event.target_name else event.target_name
        self._app.post_combat_log(f"{event.healer_name} healed {target} for {event.amount} HP!", "heal")
        self._app.post_combat_log(f"{event.target_name} now has {event.target_life} HP", "heal")
        self._app.refresh_huds()

    def _render_skill(self, event: SkillEvent) -> None:
        self._app.post_combat_log(f"{event.caster_name} casts {event.skill_name} (cost: {event.mana_cost} MP)", "skill")

    def _render_spent_mana(self, event: SpentManaEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} casted {event.skill_name} for {event.amount} mana.", "skill")
        self._app.refresh_huds()

    def _render_item(self, event: ItemEvent) -> None:
        target = "himself" if event.target_name == event.player_name else event.target_name
        self._app.post_combat_log(f"{event.player_name} uses {event.item_name} on {target}", "item")

    def _render_use_item(self, event: UseItemEvent) -> None:
        target = "himself" if event.target_name == event.player_name else event.target_name
        self._app.post_combat_log(f"{event.player_name} used {event.item_name} on {target}", "item")

    def _render_dice_roll(self, event: DiceRollEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} rolled the dice and got {event.result}!", "dice")
        if event.is_critical:
            self._app.post_combat_log(f"Critical {event.kind}! Massive damage!", "critical")

    def _render_narration(self, event: NarrationEvent) -> None:
        self._app.post_combat_log(f'{event.player_name}: "{event.text}"', "narration")

    def _render_death(self, event: DeathEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} is now dead", "death")
        self._app.refresh_huds()
        self._app.refresh_map()

    def _render_victory(self, event: VictoryEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} won the game!", "victory")
        self._app.show_game_over(event.player_name)

    def _render_side_effect(self, event: SideEffectEvent) -> None:
        if event.effect_type == "debuff" and event.occurrence == "constant":
            status = "debuffed"
        elif event.effect_type == "debuff" and event.occurrence == "iterated":
            status = "inflicted"
        else:
            status = "buffed"
        self._app.post_combat_log(f"{event.player_name} has been {status} with {event.effect_name}.", "side_effect")
        self._app.refresh_huds()

    def _render_side_effect_ended(self, event: SideEffectEndedEvent) -> None:
        self._app.post_combat_log(f"{event.effect_name} has ended for {event.player_name}", "side_effect")
        self._app.refresh_huds()

    def _render_iterated_side_effect(self, event: IteratedSideEffectEvent) -> None:
        status = "increase" if event.effect_type == "buff" else "decrease"
        attribute = (
            "life"
            if event.attribute == "health_points"
            else ("mana" if event.attribute == "magic_points" else event.attribute)
        )
        self._app.post_combat_log(
            f"{event.player_name} affected by {event.effect_name}, "
            f"will {status} {attribute} by {event.value}/turn. "
            f"{event.turns_remaining} turns left.",
            "side_effect",
        )
        self._app.refresh_huds()

    def _render_item_found(self, event: ItemFoundEvent) -> None:
        if event.found:
            self._app.post_combat_log(f"{event.player_name} found a {event.item_tier} item! {event.item_name}", "item")
        else:
            self._app.post_combat_log(f"{event.player_name} tried to find an item, but nothing was found!", "item")

    def _render_level_up(self, event: LevelUpEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} leveled up to {event.new_level}!", "level_up")
        self._app.refresh_huds()

    def _render_xp_earned(self, event: XPEarnedEvent) -> None:
        if event.kill_target:
            self._app.post_combat_log(f"{event.player_name} earned {event.xp} XP by killing {event.kill_target}!", "xp")
        else:
            self._app.post_combat_log(f"{event.player_name} earned {event.xp} XP!", "xp")

    def _render_event_action(self, event: EventAction) -> None:
        label = event.event.upper()
        self._app.post_combat_log(f"{label}:", "action")

    def _render_low_mana(self, event: LowManaEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} has {event.mana} mana, consider healing it.", "warning")

    def _render_missed_attack(self, event: MissedAttackEvent) -> None:
        self._app.post_combat_log(f"{event.attacker_name} tried to attack {event.target_name} but missed.", "miss")

    def _render_trap_activated(self, event: TrapActivatedEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} has fallen into a trap!", "trap")
        for name in event.side_effect_names:
            self._app.post_combat_log(f"  - {name}", "trap")
        self._app.refresh_huds()

    def _render_no_foes(self, event: NoFoesEvent) -> None:
        self._app.post_combat_log(event.message, "info")

    def _render_area_damage(self, event: AreaDamageEvent) -> None:
        self._app.post_combat_log(f"{event.skill_name} is an area {event.skill_kind} skill, hitting:", "skill")
        for player in event.affected_players:
            self._app.post_combat_log(
                f"  {player.name}({player.job.get_name()}) at {player.position} with {player.life} HP",
                "damage",
            )
        self._app.refresh_huds()

    def _render_player_stole_item(self, event: PlayerStoleItemEvent) -> None:
        self._app.post_combat_log(
            f"{event.player_name} stole {event.item_name} ({event.tier}) from {event.foe_name}!",
            "item",
        )

    def _render_player_fail_stole_item(self, event: PlayerFailStoleItemEvent) -> None:
        self._app.post_combat_log(f"{event.player_name} failed to steal from {event.foe_name}", "item")

    def _render_new_character(self, event: NewCharacterEvent) -> None:
        self._app.post_combat_log(f"Creating controlled character number: {event.number}...", "system")

    def _render_map_info(self, event: MapInfoEvent) -> None:
        self._app.update_map_from_event(event.current_player, event.enemies, event.matrix, event.size)

    def _render_moving_possibilities(self, event: MovingPossibilitiesEvent) -> None:
        self._app.show_move_highlights(event.player_position, event.possibilities, event.matrix, event.size)

    def _render_player_stats(self, event: PlayerStatsEvent) -> None:
        p = event.player
        self._app.post_combat_log(
            f"{p.name} Lv.{p.level} HP:{p.life}/{p.health_points} MP:{p.mana}/{p.magic_points} "
            f"STR:{p.strength} INT:{p.intelligence} ACC:{p.accuracy} "
            f"ARM:{p.armour} RES:{p.magic_resist} SPD:{p.move_speed} WILL:{p.will}",
            "stats",
        )

    def _render_enemy_status(self, event: EnemyStatusEvent) -> None:
        e = event.enemy
        self._app.post_combat_log(
            f"{e.name} ({e.job.get_name()}) Pos:{e.position} Lv.{e.level} "
            f"HP:{e.life}/{e.health_points} MP:{e.mana}/{e.magic_points} "
            f"STR:{e.strength} INT:{e.intelligence} ACC:{e.accuracy} "
            f"ARM:{e.armour} RES:{e.magic_resist} SPD:{e.move_speed} WILL:{e.will}",
            "stats",
        )

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
        self._app.post_combat_log("\n".join(lines), "item")
