from picarx import Picarx
from actions import actions_dict

class Executor:
    def __init__(self, car: Picarx) -> None:
        self.car = car

    def execute(self, action_item) -> None:
        name = action_item
        kwargs = {}

        if isinstance(action_item, (tuple, list)):
            if len(action_item) == 2 and isinstance(action_item[1], dict):
                name, kwargs = action_item
        elif isinstance(action_item, str):
            name = action_item
        
        if not name or not isinstance(name, str):
            print(f"Invalid action format: {action_item}")
            return

        if name in actions_dict:
            try:
                actions_dict[name](self.car, **kwargs)
            except Exception as e:
                print(f"Error executing action {name}: {e}")
        else:
            print(f"Action {name} not found, available actions: {list(actions_dict.keys())}")
