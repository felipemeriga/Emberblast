from typing import List, Union

import emojis
from InquirerPy import prompt
from emberblast.interface import IPlayer, IEnemiesQuestioner


class EnemiesQuestionerCMD(IEnemiesQuestioner):

    def ask_enemy_to_check(self, enemies: List[IPlayer]) -> Union[str, bool, list, IPlayer]:
        choices = []
        for enemy in enemies:
            choices.append({
                'name': '{enemy} ({job})'.format(enemy=enemy.name,
                                                 job=enemy.job.get_name()),
                'value': enemy
            })
        enemies_questions = [
            {
                'type': 'list',
                'message': 'Select an enemy:',
                'choices': choices,
                'invalid_message': 'You need to select at least one enemy to check!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]

        result = prompt(questions=enemies_questions)
        selected_enemy = result[0]
        return selected_enemy

    def ask_enemy_to_attack(self, enemies: List[IPlayer], skill_type: str = '') -> Union[str, bool, list, IPlayer]:
        choices = []
        action_type = 'attack: :punch:'

        if skill_type == 'recover':
            action_type = 'recover: :green_heart:'
        elif skill_type == 'buff':
            action_type = 'buff:'
        elif skill_type == 'debuff':
            action_type = 'debuff:'

        for enemy in enemies:
            choices.append({
                'name': '{enemy} ({job}) (life: {life})'.format(enemy=enemy.name,
                                                                job=enemy.job.get_name(),
                                                                life=enemy.life),
                'value': enemy
            })
        choices.append({
            'name': emojis.encode('Cancel :x: '),
            'value': None
        })
        enemies_questions = [
            {
                'type': 'list',
                'message': emojis.encode('Select an enemy to {action}'.format(action=action_type)),
                'choices': choices,
                'invalid_message': 'You need to select at least one enemy to attack!',
                'show_cursor': True,
                'max_height': '100'
            }
        ]
        result = prompt(questions=enemies_questions)
        selected_enemy = result[0]
        return selected_enemy
