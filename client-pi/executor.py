from picarx.preset_actions import Picarx
from actions import actions_dict

class Executor:
    def __init__(self, car: Picarx) -> None:
        self.car = car

    def execute(self, action_item) -> None:
        name = action_item
        kwargs = {}

        if isinstance(action_item, tuple):
            if len(action_item) == 2 and isinstance(action_item[1], dict):
                name, kwargs = action_item
        elif isinstance(action_item, str):
            name = action_item
        
        if not name:
            return

        if name in actions_dict:
            actions_dict[name](self.car, **kwargs)
        else:
            print(f"Action {name} not found")
