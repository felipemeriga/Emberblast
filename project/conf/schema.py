game_section_configuration_schema = {
    'jobs': {
        'required': True,
        'type': 'dict',
    },
    'races': {
        'required': True,
        'type': 'dict'
    }
}

job_section_configuration_schema = {
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
