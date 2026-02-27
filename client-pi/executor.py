from picarx import Picarx
from actions import actions_dict

class Executor:
    def __init__(self, car: Picarx, speaker=None) -> None:
        self.car = car
        self.speaker = speaker

    def execute(self, action_item: dict) -> str:
        """
        Executes a command from the VLM.
        Expected format: { "action": "forward", "speed": 30, "angle": 0, "duration": 1.0 }
        """
        if not action_item or not isinstance(action_item, dict):
            print(f"Invalid action format (expected dict): {action_item}")
            return None

        name = action_item.get("action")
        # Extract all other keys as arguments (speed, angle, duration)
        kwargs = {k: v for k, v in action_item.items() if k != "action"}

        if name in actions_dict: 
            print(f"Executing: {name} with {kwargs}")
            try:
                if name in ["speak", "ask"]:
                    if self.speaker:
                        actions_dict[name](self.speaker, **kwargs)
                    else:
                        print("Speaker not initialized")
                elif name in ["look_left", "look_right", "look_up", "look_down"]:
                    # These return "capture" signal
                    return actions_dict[name](self.car, **kwargs)
                else:
                    actions_dict[name](self.car, **kwargs)
            except Exception as e:
                print(f"Error executing action {name}: {e}")
        else:
            print(f"Action '{name}' not found. Available: {list(actions_dict.keys())}")
        return None
