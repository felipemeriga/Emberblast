from InquirerPy import prompt
from typing import List

from project.game import DeathMatch
from project.map import MapFactory, Map
from project.orchestrator import GameOrchestrator, DeathMatchOrchestrator
from project.player import ControlledPlayer, dynamic_jobs_classes, dynamic_races_classes, bot_factory, BotPlayer
from project.questions import perform_game_create_questions, perform_first_question
from project.questions.save import get_saved_game
from project.save import get_normalized_saved_files_dict, recover_saved_game_orchestrator


class GameFactory:
    def __init__(self):
        """
        Constructor of the class, responsible for creating the game, and performing the proper questions.
        """
        self.begin_question_results = None

    def pre_initial_settings(self) -> GameOrchestrator:
        """
        Executes the first game questions, checking if the player wants to create a new game, or load an existing one.

        :rtype: GameOrchestrator.
        """
        normalized_files = get_normalized_saved_files_dict()

        # Checking first if there are any saved games
        if len(normalized_files) > 0:
            first_game_question = perform_first_question()
            if first_game_question == 'new':
                return self.new_game()
            elif first_game_question == 'continue':
                normalized_files = get_normalized_saved_files_dict()
                selected_file = get_saved_game(normalized_files)
                game_orchestrator = recover_saved_game_orchestrator(selected_file)
                return game_orchestrator
        else:
            return self.new_game()

    def new_game(self) -> GameOrchestrator:
        """
        Creates a new game, prompting the user the necessary questions of how the game will be, and
        instantiate the proper objects, according to what was requested.

        :rtype: GameOrchestrator.
        """
        self.begin_question_results = perform_game_create_questions()
        main_player = self.init_players()

        bots = self.init_bots()

        game_map = self.init_map(len(bots) + 3)

        if self.begin_question_results.get('game') == 'Deathmatch':
            game = DeathMatch(main_player, bots, game_map)
            game.calculate_turn_order()
            game.game_map.define_player_initial_position_random(game.get_all_players())
            game.game_map.distribute_random_items()
            orchestrator = DeathMatchOrchestrator(game)
            return orchestrator

    def init_map(self, map_size: int) -> Map:
        """
        Calls MapFactory to create a new map, depending on the number of players, that will be proportional to map size.

        :param int map_size: The size of the map, may change depending the number of players.
        :rtype: Map.
        """
        return MapFactory().create_map(map_size)

    def init_players(self) -> ControlledPlayer:
        """
        Method used for generating the controlled players.

        :rtype: ControlledPlayer.
        """
        return ControlledPlayer(self.begin_question_results.get('nickname'),
                                dynamic_jobs_classes[self.begin_question_results.get('job')](),
                                dynamic_races_classes[self.begin_question_results.get('race')]())

    def init_bots(self) -> List[BotPlayer]:
        """
        Method used for generating the bots, which will call bot_factory, that randomly picks
        available races and jobs for each player.

        :rtype: List[BotPlayer].
        """
        return bot_factory(self.begin_question_results.get('bots_number'))
