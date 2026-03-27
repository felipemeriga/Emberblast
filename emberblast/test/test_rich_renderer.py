from emberblast.events import (
    DamageEvent,
    DeathEvent,
    DiceRollEvent,
    GameEvent,
    HealEvent,
    ItemFoundEvent,
    LevelUpEvent,
    MissedAttackEvent,
    MoveEvent,
    NarrationEvent,
    TurnStartEvent,
    VictoryEvent,
    XPEarnedEvent,
)
from emberblast.renderer.rich_cli import RichCLIRenderer
from emberblast.test.test import BaseTestCase


class TestRichCLIRenderer(BaseTestCase):
    def setUp(self):
        self.renderer = RichCLIRenderer()

    def test_render_turn_start(self):
        event = TurnStartEvent(turn=3)
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
        event = DiceRollEvent(player_name="Grukk", result=20, kind="attack", is_critical=True)
        self.renderer.render(event)

    def test_render_level_up_event(self):
        event = LevelUpEvent(player_name="Grukk", new_level=4)
        self.renderer.render(event)

    def test_render_xp_earned_event(self):
        event = XPEarnedEvent(player_name="Grukk", xp=30)
        self.renderer.render(event)

    def test_render_unknown_event_does_not_crash(self):
        event = GameEvent()
        self.renderer.render(event)

    def test_render_item_found(self):
        event = ItemFoundEvent(player_name="Grukk", found=True, item_name="Sword", item_tier="rare")
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
