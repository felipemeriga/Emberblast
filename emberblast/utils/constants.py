import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

GAME_SECTION = 'game'
JOBS_SECTION = 'jobs'
RACES_SECTION = 'races'
ITEMS_SECTION = 'items'
SKILLS_SECTION = 'skills'
SIDE_EFFECTS_SECTION = 'side_effects'
ITEMS_PROBABILITIES_SECTION = 'items_probabilities'
LEVEL_UP_INCREMENT = 'level_up_attributes_increment'
EXPERIENCE_EARNED_ACTION = 'experience_earned_action'
PASS_ACTION_NAME = 'pass'

DELAYED_ACTIONS = ['attack', 'skill', 'defend', 'hide', 'search', 'item']