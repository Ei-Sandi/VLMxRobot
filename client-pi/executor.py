from picarx import Picarx
from actions import actions_dict
import inspect

class Executor:
    def __init__(self, car: Picarx, speaker=None, check_safeguard=None) -> None:
        self.car = car
        self.speaker = speaker
        self.check_safeguard = check_safeguard

    def execute(self, action_item: dict) -> str:
        """
        Executes a command from the VLM.
        Expected format: { "action": "forward", "speed": 30, "angle": 0, "duration": 1.0 }
        """
        if not action_item or not isinstance(action_item, dict):
            print(f"Invalid action format (expected dict): {action_item}")
            return None

        name = action_item.get("action")
        # Extract all other keys as arguments, dropping nulls from model output
        raw_kwargs = {k: v for k, v in action_item.items() if k != "action" and v is not None}

        if name in actions_dict: 
            action_fn = actions_dict[name]

            # Keep only kwargs accepted by the action function to avoid unexpected-arg errors
            accepted_params = set(inspect.signature(action_fn).parameters.keys())
            kwargs = {k: v for k, v in raw_kwargs.items() if k in accepted_params}

            print(f"Executing: {name} with {kwargs}")
            try:
                if name in ["speak", "ask"]:
                    if self.speaker:
                        action_fn(self.speaker, **kwargs)
                    else:
                        print("Speaker not initialized")
                elif name in ["look_left", "look_right", "look_up", "look_down"]:
                    # These return "capture" signal
                    return action_fn(self.car, check_safeguard=self.check_safeguard, **kwargs)
                else:
                    return action_fn(self.car, check_safeguard=self.check_safeguard, **kwargs)
            except Exception as e:
                print(f"Error executing action {name}: {e}")
        else:
            print(f"Action '{name}' not found. Available: {list(actions_dict.keys())}")
        return None
