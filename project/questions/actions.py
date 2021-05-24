import emojis
from InquirerPy import prompt


def ask_actions_questions():
    actions_questions = [
        {
            "type": "list",
            "message": "Select an action:",
            "choices": [
                {
                    "name": emojis.encode("Move: :runner:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "move"
                    }
                },
                {
                    "name": emojis.encode("Attack: :crossed_swords:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "attack"
                    }
                },
                {
                    "name": emojis.encode("Skill: :fire:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "attack"
                    }
                },
                {
                    "name": emojis.encode("Defend: :shield:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "attack"
                    }
                },
                {
                    "name": emojis.encode("Hide: :ninja:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "attack"
                    }
                },
                {
                    "name": emojis.encode("Search: :eye:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "attack"
                    }
                },
                {
                    "name": emojis.encode("Item: :test_tube:"),
                    "value": {
                        "attribute": "health_points",
                        "value": "attack"
                    }
                },

            ],
            "default": "Defend",
            "invalid_message": "You need to select at least one action to execute!",
            "show_cursor": True,
            "max_height": "100"
        }
    ]
    result = prompt(questions=actions_questions)
    print(result)

