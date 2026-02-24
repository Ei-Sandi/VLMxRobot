from picarx import Picarx
from actions import actions_dict

class Executor:
    def __init__(self, car: Picarx) -> None:
        self.car = car

    def execute(self, action_item: dict) -> None:
        """
        Executes a command from the VLM.
        Expected format: { "action": "forward", "speed": 30, "angle": 0, "duration": 1.0 }
        """
        if not action_item or not isinstance(action_item, dict):
            print(f"Invalid action format (expected dict): {action_item}")
            return

        name = action_item.get("action")
        # Extract all other keys as arguments (speed, angle, duration)
        kwargs = {k: v for k, v in action_item.items() if k != "action"}

        if name in actions_dict: 
            print(f"Executing: {name} with {kwargs}")
            try:
                # Calls the function from actions.py with the arguments
                actions_dict[name](self.car, **kwargs)
            except Exception as e:
                print(f"Error executing action {name}: {e}")
        else:
            print(f"Action '{name}' not found. Available: {list(actions_dict.keys())}")
