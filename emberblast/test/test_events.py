from emberblast.events import (
    DamageEvent,
    DiceRollEvent,
    EventAction,
    GameEvent,
    HealEvent,
    ItemFoundEvent,
    LevelUpEvent,
    MoveEvent,
    NarrationEvent,
    SideEffectEvent,
    TurnStartEvent,
    VictoryEvent,
    XPEarnedEvent,
)
from emberblast.test.test import BaseTestCase


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
        event = DiceRollEvent(player_name="Grukk", result=20, kind="attack", is_critical=True)
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
