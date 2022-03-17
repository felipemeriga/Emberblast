main_section_configuration_schema = {
    'game': {
        'required': True,
        'type': 'dict',
    },
}

game_section_configuration_schema = {
    'jobs': {
        'required': True,
        'type': 'dict',
    },
    'races': {
        'required': True,
        'type': 'dict'
    },
    'max_number_bots': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 100
    },
    'dice_sides': {
        'required': True,
        'type': 'number',
        'min': 2,
        'max': 50
    },
    "level_up_attributes_increment": {
        'required': True,
        'type': 'dict',
    },
    "experience_earned_action": {
        'required': True,
        'type': 'dict',
    },
    'items_probabilities': {
        'required': True,
        'type': 'dict',
    },
}

items_probabilities_schema = {
    'common': {
        'required': True,
        'type': 'float',
        'min': 0,
        'max': 1
    },
    'uncommon': {
        'required': True,
        'type': 'float',
        'min': 0,
        'max': 1
    },
    'rare': {
        'required': True,
        'type': 'float',
        'min': 0,
        'max': 1
    },
    'legendary': {
        'required': True,
        'type': 'float',
        'min': 0,
        'max': 1
    }
}

attribute_section_schema = {
    'health_points': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 50
    },
    'magic_points': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 50
    },
    'move_speed': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 10
    },
    'strength': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 10
    },
    'intelligence': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 10
    },
    'accuracy': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 10
    },
    'armour': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 10
    },
    'magic_resist': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 10
    },
    'will': {
        'required': True,
        'type': 'number',
        'min': 0,
        'max': 5
    },
}

job_section_configuration_schema = {
    **attribute_section_schema,
    'attack_type': {
        'required': True,
        'type': 'string',
        'allowed': ['melee', 'ranged']
    },
    'damage_vector': {
        'required': True,
        'type': 'string',
        'allowed': ['strength', 'intelligence']
    }
}

race_section_configuration_schema = {
    **attribute_section_schema
}

level_up_attributes_configuration_schema = {
    **attribute_section_schema
}

experience_earned_action_configuration_schema = {
    'attack': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 100,
    },
    'kill': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 100
    },
}

side_effects_configuration_schema = {
    'type': {
        'required': True,
        'type': 'string',
        'allowed': ['buff', 'debuff']
    },
    'attribute': {
        'required': True,
        'type': 'string',
        'allowed': ['health_points', 'magic_points', 'move_speed', 'strength', 'intelligence', 'accuracy', 'armour',
                    'magic_resist', 'will']
    },
    'base': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 100
    },
    'duration': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 20
    },
    'occurrence': {
        'required': True,
        'type': 'string',
        'allowed': ['constant', 'iterated']
    },
}

general_item_validation_schema = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'type': {
        'required': True,
        'type': 'string',
        'allowed': ['recovery', 'healing', 'equipment']
    },
    'tier': {
        'required': True,
        'type': 'string',
        'allowed': ['common', 'uncommon', 'rare', 'legendary']
    },
    'description': {
        'required': True,
        'type': 'string'
    },
    'weight': {
        'required': True,
        'type': 'float'
    },
}
healing_item_validation_schema = {
    **general_item_validation_schema,
    'attribute': {
        'required': True,
        'type': 'string',
        'allowed': ['health_points', 'magic_points', 'move_speed', 'strength', 'intelligence', 'accuracy', 'armour',
                    'magic_resist', 'will']
    },
    'base': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 100
    },
}

recovery_item_validation_schema = {
    **general_item_validation_schema,
    'status': {
        'required': True,
        'type': 'string',
    }
}

equipment_item_validation_schema = {
    **general_item_validation_schema,
    'base': {
        'required': True,
        'type': 'number',
        'min': 1,
        'max': 100
    },
    'attribute': {
        'required': True,
        'type': 'string',
        'allowed': ['health_points', 'magic_points', 'move_speed', 'strength', 'intelligence', 'accuracy', 'armour',
                    'magic_resist', 'will']
    },
    'side_effects': {
        'required': False,
        'type': 'list', 'schema': {'type': 'string'}
    },
    'category': {
        'required': True,
        'type': 'string',
        'allowed': ['weapon', 'boots', 'accessory', 'armour', 'shield']
    },
    'usage': {
        'required': True,
        'type': 'string',
        'allowed': ['all', 'melee', 'ranged']
    },
    'wielding': {
        'required': False,
        'type': 'number',
        'allowed': [1, 2]
    },
}

skills_validation_schema = {
    'name': {
        'type': 'string',
        'required': True
    },
    'description': {
        'type': 'string',
        'required': False
    },
    'base': {
        'type': 'number',
        'required': True
    },
    'cost': {
        'type': 'number',
        'required': True
    },
    'kind': {
        'type': 'string',
        'required': True,
        'allowed': ['inflict', 'recover', 'debuff', 'buff', 'trap']
    },
    'ranged': {
        'type': 'number',
        'required': True
    },
    'area': {
        'type': 'number',
        'required': True
    },
    'level_requirement': {
        'type': 'number',
        'required': True
    },
    'job': {
        'type': 'string',
        'required': True
    },
    'base_attribute': {
        'type': 'string',
        'required': True,
        'allowed': ['intelligence', 'strength']
    },
    'side_effects': {
        'required': False,
        'default': [],
        'type': 'list', 'schema': {'type': 'string'}
    },
    'applies_caster_only': {
        'required': False,
        'default': False,
        'type': 'boolean',
    },
    'punishment_side_effects': {
        'required': False,
        'default': [],
        'type': 'list', 'schema': {'type': 'string'}
    }
}
