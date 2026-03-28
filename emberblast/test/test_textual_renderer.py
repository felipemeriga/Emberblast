from unittest.mock import MagicMock

from emberblast.events import (
    AreaDamageEvent,
    CheckItemEvent,
    DamageEvent,
    DeathEvent,
    DiceRollEvent,
    EnemyStatusEvent,
    EventAction,
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
from emberblast.test.test import BaseTestCase


class TestTextualRenderer(BaseTestCase):
    def setUp(self):
        self.app = MagicMock()
        from emberblast.tui.renderer import TextualRenderer

        self.renderer = TextualRenderer(self.app)

    def test_render_greetings_posts_combat_log(self):
        self.renderer.render(GreetingsEvent())
        self.app.post_combat_log.assert_called_once()
        args = self.app.post_combat_log.call_args
        self.assertIn("EMBERBLAST", args[0][0])

    def test_render_turn_start_sets_turn_and_posts_log(self):
        self.renderer.render(TurnStartEvent(turn=3))
        self.app.set_turn.assert_called_once_with(3)
        self.app.post_combat_log.assert_called_once()

    def test_render_player_turn_sets_active_player(self):
        self.renderer.render(PlayerTurnEvent(player_name="Hero"))
        self.app.set_active_player.assert_called_once_with("Hero")
        self.app.post_combat_log.assert_called_once()

    def test_render_line_separator_posts_log(self):
        self.renderer.render(LineSeparatorEvent())
        self.app.post_combat_log.assert_called_once()

    def test_render_move_with_positions(self):
        self.renderer.render(MoveEvent(player_name="Hero", from_position="A0", to_position="B1"))
        self.app.post_combat_log.assert_called_once()
        msg = self.app.post_combat_log.call_args[0][0]
        self.assertIn("Hero", msg)
        self.assertIn("A0", msg)
        self.assertIn("B1", msg)

    def test_render_move_without_positions(self):
        self.renderer.render(MoveEvent(player_name="Hero"))
        self.app.post_combat_log.assert_called_once()
        msg = self.app.post_combat_log.call_args[0][0]
        self.assertIn("Hero", msg)

    def test_render_damage(self):
        self.renderer.render(
            DamageEvent(attacker_name="Atk", target_name="Def", damage=50, target_alive=True, target_life=100)
        )
        self.app.post_combat_log.assert_called()
        self.app.refresh_huds.assert_called()

    def test_render_damage_target_dead(self):
        self.renderer.render(
            DamageEvent(attacker_name="Atk", target_name="Def", damage=50, target_alive=False, target_life=0)
        )
        self.app.post_combat_log.assert_called()

    def test_render_heal(self):
        self.renderer.render(HealEvent(healer_name="Heal", target_name="Hurt", amount=30, target_life=80))
        self.app.post_combat_log.assert_called()
        self.app.refresh_huds.assert_called()

    def test_render_spent_mana(self):
        self.renderer.render(SpentManaEvent(player_name="Mage", amount=20, skill_name="Fireball"))
        self.app.post_combat_log.assert_called_once()
        self.app.refresh_huds.assert_called()

    def test_render_use_item(self):
        self.renderer.render(UseItemEvent(player_name="Hero", item_name="Potion", target_name="Hero"))
        self.app.post_combat_log.assert_called_once()

    def test_render_dice_roll(self):
        self.renderer.render(DiceRollEvent(player_name="Hero", result=6, kind="attack", is_critical=False))
        self.app.post_combat_log.assert_called()

    def test_render_dice_roll_critical(self):
        self.renderer.render(DiceRollEvent(player_name="Hero", result=20, kind="attack", is_critical=True))
        calls = self.app.post_combat_log.call_args_list
        self.assertTrue(len(calls) >= 2)

    def test_render_narration(self):
        self.renderer.render(NarrationEvent(player_name="Hero", text="I shall prevail!"))
        self.app.post_combat_log.assert_called_once()

    def test_render_death(self):
        self.renderer.render(DeathEvent(player_name="Villain"))
        self.app.post_combat_log.assert_called_once()
        self.app.refresh_huds.assert_called()

    def test_render_victory_shows_game_over(self):
        self.renderer.render(VictoryEvent(player_name="Hero"))
        self.app.show_game_over.assert_called_once_with("Hero")

    def test_render_side_effect_debuff_constant(self):
        self.renderer.render(
            SideEffectEvent(player_name="Hero", effect_name="Poison", effect_type="debuff", occurrence="constant")
        )
        self.app.post_combat_log.assert_called_once()
        self.assertIn("debuffed", self.app.post_combat_log.call_args[0][0])

    def test_render_side_effect_debuff_iterated(self):
        self.renderer.render(
            SideEffectEvent(player_name="Hero", effect_name="Burn", effect_type="debuff", occurrence="iterated")
        )
        self.assertIn("inflicted", self.app.post_combat_log.call_args[0][0])

    def test_render_side_effect_buff(self):
        self.renderer.render(
            SideEffectEvent(player_name="Hero", effect_name="Shield", effect_type="buff", occurrence="constant")
        )
        self.assertIn("buffed", self.app.post_combat_log.call_args[0][0])

    def test_render_side_effect_ended(self):
        self.renderer.render(SideEffectEndedEvent(player_name="Hero", effect_name="Poison"))
        self.app.post_combat_log.assert_called_once()

    def test_render_iterated_side_effect(self):
        self.renderer.render(
            IteratedSideEffectEvent(
                player_name="Hero",
                effect_name="Burn",
                effect_type="debuff",
                attribute="health_points",
                value=5,
                turns_remaining=3,
            )
        )
        self.app.post_combat_log.assert_called_once()
        msg = self.app.post_combat_log.call_args[0][0]
        self.assertIn("life", msg)

    def test_render_item_found_success(self):
        self.renderer.render(ItemFoundEvent(player_name="Hero", found=True, item_name="Sword", item_tier="gold"))
        self.app.post_combat_log.assert_called_once()

    def test_render_item_found_failure(self):
        self.renderer.render(ItemFoundEvent(player_name="Hero", found=False))
        self.app.post_combat_log.assert_called_once()

    def test_render_level_up(self):
        self.renderer.render(LevelUpEvent(player_name="Hero", new_level=5))
        self.app.post_combat_log.assert_called_once()
        self.app.refresh_huds.assert_called()

    def test_render_xp_earned_with_kill(self):
        self.renderer.render(XPEarnedEvent(player_name="Hero", xp=100, kill_target="Villain"))
        msg = self.app.post_combat_log.call_args[0][0]
        self.assertIn("Villain", msg)

    def test_render_xp_earned_no_kill(self):
        self.renderer.render(XPEarnedEvent(player_name="Hero", xp=50))
        self.app.post_combat_log.assert_called_once()

    def test_render_event_action(self):
        self.renderer.render(EventAction(event="attack"))
        self.app.post_combat_log.assert_called_once()

    def test_render_low_mana(self):
        self.renderer.render(LowManaEvent(player_name="Mage", mana=5))
        self.app.post_combat_log.assert_called_once()

    def test_render_missed_attack(self):
        self.renderer.render(MissedAttackEvent(attacker_name="Hero", target_name="Foe"))
        self.app.post_combat_log.assert_called_once()

    def test_render_trap_activated(self):
        self.renderer.render(TrapActivatedEvent(player_name="Hero", side_effect_names=["Poison", "Burn"]))
        calls = self.app.post_combat_log.call_args_list
        self.assertTrue(len(calls) >= 2)

    def test_render_no_foes(self):
        self.renderer.render(NoFoesEvent(message="No enemies nearby"))
        self.app.post_combat_log.assert_called_once()

    def test_render_area_damage(self):
        player = MagicMock()
        player.name = "Target"
        player.job.get_name.return_value = "Warrior"
        player.position = "A0"
        player.life = 100
        self.renderer.render(AreaDamageEvent(skill_name="Blizzard", skill_kind="magic", affected_players=[player]))
        self.app.post_combat_log.assert_called()

    def test_render_player_stole_item(self):
        self.renderer.render(
            PlayerStoleItemEvent(player_name="Thief", foe_name="Victim", item_name="Ring", tier="silver")
        )
        self.app.post_combat_log.assert_called_once()

    def test_render_player_fail_stole_item(self):
        self.renderer.render(PlayerFailStoleItemEvent(player_name="Thief", foe_name="Victim"))
        self.app.post_combat_log.assert_called_once()

    def test_render_new_character(self):
        self.renderer.render(NewCharacterEvent(number=1))
        self.app.post_combat_log.assert_called_once()

    def test_render_map_info_calls_update_map(self):
        self.renderer.render(
            MapInfoEvent(current_player="p", enemies=["e"], matrix=[[1]], size=1)
        )
        self.app.update_map_from_event.assert_called_once_with("p", ["e"], [[1]], 1)

    def test_render_moving_possibilities(self):
        self.renderer.render(
            MovingPossibilitiesEvent(player_position="A0", possibilities=["A1", "B0"], matrix=[[1]], size=1)
        )
        self.app.show_move_highlights.assert_called_once_with("A0", ["A1", "B0"], [[1]], 1)

    def test_render_player_stats(self):
        player = MagicMock()
        player.name = "Hero"
        player.level = 5
        player.life = 100
        player.health_points = 120
        player.mana = 50
        player.magic_points = 60
        player.strength = 10
        player.intelligence = 8
        player.accuracy = 7
        player.armour = 5
        player.magic_resist = 4
        player.move_speed = 3
        player.will = 6
        self.renderer.render(PlayerStatsEvent(player=player))
        self.app.post_combat_log.assert_called_once()

    def test_render_enemy_status(self):
        enemy = MagicMock()
        enemy.name = "Foe"
        enemy.job.get_name.return_value = "Mage"
        enemy.position = "B2"
        enemy.level = 3
        enemy.life = 80
        enemy.health_points = 100
        enemy.mana = 40
        enemy.magic_points = 50
        enemy.strength = 8
        enemy.intelligence = 12
        enemy.accuracy = 6
        enemy.armour = 3
        enemy.magic_resist = 7
        enemy.move_speed = 4
        enemy.will = 5
        self.renderer.render(EnemyStatusEvent(enemy=enemy))
        self.app.post_combat_log.assert_called_once()

    def test_render_check_item(self):
        item = MagicMock()
        item.name = "Sword"
        item.tier = "gold"
        item.description = "A sharp sword"
        item.weight = 2.5
        self.renderer.render(CheckItemEvent(item=item))
        self.app.post_combat_log.assert_called_once()

    def test_render_skill_event(self):
        self.renderer.render(SkillEvent(caster_name="Mage", skill_name="Fireball", mana_cost=20))
        self.app.post_combat_log.assert_called_once()

    def test_render_item_event(self):
        self.renderer.render(ItemEvent(player_name="Hero", item_name="Potion", target_name="Hero"))
        self.app.post_combat_log.assert_called_once()

    def test_unknown_event_does_not_crash(self):
        from emberblast.events.events import GameEvent

        self.renderer.render(GameEvent())  # base event, not in dispatch

    def test_all_event_types_in_dispatch(self):
        """Verify that every concrete event type has a handler."""
        expected_types = {
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
        }
        self.assertEqual(expected_types, set(self.renderer._dispatch.keys()))
