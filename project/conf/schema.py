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
    },
}

race_section_configuration_schema = {
    **attribute_section_schema
}

level_up_attributes_configuration_schema = {
    **attribute_section_schema
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

items_validation_schema = {
    'type': {
        'required': True,
        'type': 'string',
        'allowed': ['recovery', 'healing', 'equipable']
    },
    'tier': {
        'required': True,
        'type': 'string',
        'allowed': ['common', 'uncommon', 'rare', 'legendary']
    },
    'description': {
        'required': True,
        'type': 'string',
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
    'side-effects': {
        'required': False,
        'type': 'list', 'schema': {'type': 'string'}
    }
}

general_item_validation_schema = {
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
        'type': 'string',
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
    'side-effects': {
        'required': False,
        'type': 'list', 'schema': {'type': 'string'}
    }
}
