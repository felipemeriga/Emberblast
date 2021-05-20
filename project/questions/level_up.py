from InquirerPy import prompt
import emojis


def ask_attributes_to_improve():
    # TODO - Those improvements points are hardcoded, we need to make them dynamic, combinating attributes of the
    #  class and the race
    health_points = 5
    magic_points = 5
    move_speed = 1
    strength = 3
    intelligence = 3
    accuracy = 1
    armour = 3
    magic_resist = 3
    will = 1

    level_up_questions = [
        {
            "type": "list",
            "message": "Select an action:",
            "choices": [
                {
                    "name": emojis.encode("+{points} Health Points :green_heart:".format(points=health_points)),
                    "value": {
                        "attribute": "health_points",
                        "value": health_points
                    }
                },
                {
                    "name": emojis.encode("+{points} Magic Points :blue_heart:".format(points=magic_points)),
                    "value": {
                        "attribute": "magic_points",
                        "value": magic_points
                    }
                },
                {
                    "name": emojis.encode("+{points} Move Speed :runner:".format(points=move_speed)),
                    "value": {
                        "attribute": "move_speed",
                        "value": move_speed
                    }
                },
                {
                    "name": emojis.encode("+{points} Strength :punch:".format(points=strength)),
                    "value": {
                        "attribute": "strength",
                        "value": strength
                    }
                },
                {
                    "name": emojis.encode("+{points} Intelligence :books:".format(points=intelligence)),
                    "value": {
                        "attribute": "intelligence",
                        "value": intelligence
                    }
                },
                {
                    "name": emojis.encode("+{points} Accuracy :dart:".format(points=accuracy)),
                    "value": {
                        "attribute": "accuracy",
                        "value": accuracy
                    }
                },
                {
                    "name": emojis.encode("+{points} Armour :anger:".format(points=armour)),
                    "value": {
                        "attribute": "armour",
                        "value": armour
                    }
                },
                {
                    "name": emojis.encode("+{points} Magic Resist :cyclone:".format(points=magic_resist)),
                    "value": {
                        "attribute": "magic_resist",
                        "value": magic_resist
                    }
                },
                {
                    "name": emojis.encode("+{points} Will :pray:".format(points=will)),
                    "value": {
                        "attribute": "will",
                        "value": will
                    }
                },
            ],
            "default": None,
            "multiselect": True,
            "validate": lambda result: len(result) == 2,
            "invalid_message": "You need to select 2 attributes to improve!",
            "show_cursor": True,
            "max_height": "100"
        },
    ]

    result = prompt(questions=level_up_questions)
    return result[0]
