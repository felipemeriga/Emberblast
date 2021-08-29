from enum import Enum
from typing import Dict

from project.interface import IBotDecisioning, IGame, IAction, IPlayer, IPlayingMode


class BotDecisioning(IBotDecisioning):

    def __init__(self, game: IGame) -> None:
        self.game = game
        self.current_bot = None
        self.current_play_style = IPlayingMode.NEUTRAL

    def move(self) -> None:
        pass

    def probability_of_damage(self, foe: IPlayer) -> bool:
        if self.current_bot.job.intelligence > self.current_bot.job.strength:
            if self.current_bot.get_attribute_real_value('intelligence') > self.current_bot.get_attribute_real_value(
                    'magic_resist'):
                return True
        else:
            if self.current_bot.get_attribute_real_value('strength') > self.current_bot.get_attribute_real_value(
                    'armour'):
                return True
        return False

    def select_playing_mode(self) -> None:
        remaining_players = self.game.get_remaining_players(player=self.current_bot, include_hidden=True)
        low_life_level = self.current_bot.life * 0.3

        if self.current_bot.life > low_life_level:
            self.current_play_style = IPlayingMode.AGGRESSIVE
        elif self.current_bot.life < low_life_level and len(remaining_players) > 1:
            self.current_play_style = IPlayingMode.DEFENSIVE
        elif self.current_bot.life < low_life_level and len(remaining_players) == 1 and self.probability_of_damage(
                remaining_players[0]):
            self.current_play_style = IPlayingMode.AGGRESSIVE
        else:
            self.current_play_style = IPlayingMode.DEFENSIVE

    def decide(self, player: IPlayer, actions_left: Dict[str, IAction]) -> None:
        # move phase
        self.current_bot = player
        self.select_playing_mode()
