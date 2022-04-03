from random import randrange
from typing import List

from emberblast.conf import get_configuration
from emberblast.game import DeathMatch
from emberblast.map import MapFactory
from emberblast.orchestrator import DeathMatchOrchestrator
from emberblast.player import ControlledPlayer, dynamic_jobs_classes, dynamic_races_classes, BotPlayer
from emberblast.save import get_normalized_saved_files_dict, recover_saved_game_orchestrator
from emberblast.item import Bag
from emberblast.utils import JOBS_SECTION, RACES_SECTION
from emberblast.utils.name_generator import generate_name
from emberblast.item import Equipment
from emberblast.interface import IMap, IControlledPlayer, IBotPlayer, IGameOrchestrator, IGameFactory
from emberblast.communicator import communicator_injector


@communicator_injector()
class GameFactory(IGameFactory):
    def __init__(self):
        """
        Constructor of the class, responsible for creating the game, and performing the proper communicator.
        """
        self.begin_question_results = None

    def pre_initial_settings(self) -> IGameOrchestrator:
        """
        Executes the first game communicator, checking if the player wants to create a new game, or load an existing one.

        :rtype: IGameOrchestrator.
        """
        normalized_files = get_normalized_saved_files_dict()

        # Checking first if there are any saved games
        if len(normalized_files) > 0:
            first_game_question = self.communicator.questioner.perform_first_question()
            if first_game_question == 'new':
                return self.new_game()
            elif first_game_question == 'continue':
                normalized_files = get_normalized_saved_files_dict()
                selected_file = self.communicator.questioner.get_saved_game(normalized_files)
                game_orchestrator = recover_saved_game_orchestrator(selected_file)
                return game_orchestrator
        else:
            return self.new_game()

    def new_game(self) -> IGameOrchestrator:
        """
        Creates a new game, prompting the user the necessary communicator of how the game will be, and
        instantiate the proper objects, according to what was requested.

        :rtype: IGameOrchestrator.
        """
        players = []
        self.begin_question_results = self.communicator.questioner.perform_game_create_questions()
        controlled_players = self.init_players()
        players.extend(controlled_players)

        bots = self.init_bots()
        players.extend(bots)

        game_map = self.init_map(len(bots) + 4)

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

    def init_players(self) -> List[IControlledPlayer]:
        """
        Method used for generating the controlled players.

        :rtype: IControlledPlayer.
        """
        controlled_players = []

        for i in range(int(self.begin_question_results.get('controlled_players_number', 1))):
            bag = Bag()
            equipment = Equipment()
            self.communicator.informer.create_new_character(i)
            existing_names = [x for x in map(lambda player: player.name, controlled_players)]

            new_character_responses = self.communicator.questioner.perform_character_creation_questions(
                existing_names)
            controlled_player = ControlledPlayer(new_character_responses.get('nickname'),
                                                 dynamic_jobs_classes[new_character_responses.get('job')](),
                                                 dynamic_races_classes[new_character_responses.get('race')](),
                                                 bag,
                                                 equipment)
            controlled_players.append(controlled_player)

        return controlled_players

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
