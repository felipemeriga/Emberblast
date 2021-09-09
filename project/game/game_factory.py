from random import randrange
from typing import List

from project.conf import get_configuration
from project.game import DeathMatch
from project.map import MapFactory
from project.orchestrator import DeathMatchOrchestrator
from project.player import ControlledPlayer, dynamic_jobs_classes, dynamic_races_classes, BotPlayer
from project.questions import perform_game_create_questions, perform_first_question
from project.questions import get_saved_game
from project.save import get_normalized_saved_files_dict, recover_saved_game_orchestrator
from project.item import Bag
from project.utils import JOBS_SECTION, RACES_SECTION
from project.utils.name_generator import generate_name
from project.item import Equipment
from project.interface import IMap, IControlledPlayer, IBotPlayer, IGameOrchestrator, IGameFactory


class GameFactory(IGameFactory):
    def __init__(self):
        """
        Constructor of the class, responsible for creating the game, and performing the proper questions.
        """
        self.begin_question_results = None

    def pre_initial_settings(self) -> IGameOrchestrator:
        """
        Executes the first game questions, checking if the player wants to create a new game, or load an existing one.

        :rtype: IGameOrchestrator.
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

    def new_game(self) -> IGameOrchestrator:
        """
        Creates a new game, prompting the user the necessary questions of how the game will be, and
        instantiate the proper objects, according to what was requested.

        :rtype: IGameOrchestrator.
        """
        players = []
        self.begin_question_results = perform_game_create_questions()
        main_player = self.init_players()
        players.append(main_player)

        bots = self.init_bots()
        players.extend(bots)

        game_map = self.init_map(len(bots) + 3)

        if self.begin_question_results.get('game') == 'Deathmatch':
            game = DeathMatch(players, game_map)
            game.calculate_turn_order()
            game.game_map.define_player_initial_position_random(game.get_all_players())
            game.game_map.distribute_random_items()
            orchestrator = DeathMatchOrchestrator(game)
            return orchestrator

    def init_map(self, map_size: int) -> IMap:
        """
        Calls MapFactory to create a new map, depending on the number of players, that will be proportional to map size.

        :param int map_size: The size of the map, may change depending the number of players.
        :rtype: IMap.
        """
        return MapFactory().create_map(map_size)

    def init_players(self) -> IControlledPlayer:
        """
        Method used for generating the controlled players.

        :rtype: IControlledPlayer.
        """
        bag = Bag()
        equipment = Equipment()

        controlled_player = ControlledPlayer(self.begin_question_results.get('nickname'),
                                             dynamic_jobs_classes[self.begin_question_results.get('job')](),
                                             dynamic_races_classes[self.begin_question_results.get('race')](),
                                             bag,
                                             equipment)
        return controlled_player

    def init_bots(self) -> List[IBotPlayer]:
        """
        Method used for generating the bots, which will call bot_factory, that randomly picks
        available races and jobs for each player.

        :rtype: List[IBotPlayer].
        """
        return bot_factory(self.begin_question_results.get('bots_number'))


def bot_factory(number_of_bots: int) -> List[IBotPlayer]:
    """
    Function that will generated all the bots, depending of the number that was informed as the argument,
    each bot race and job, will be picked randomly.

    :param int number_of_bots: Number of bots to create.
    :rtype: List[IBotPlayer].
    """
    bots = []
    jobs = list(get_configuration(JOBS_SECTION).keys())
    races = list(get_configuration(RACES_SECTION).keys())
    for n in range(int(number_of_bots)):
        name = generate_name()
        chosen_job = jobs[randrange(len(jobs))]
        chosen_race = races[randrange(len(races))]
        job = dynamic_jobs_classes[chosen_job]()
        race = dynamic_races_classes[chosen_race]()
        bag = Bag()
        equipment = Equipment()
        bots.append(BotPlayer(name, job, race, bag, equipment))

    return bots
