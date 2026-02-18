import time
from picarx.preset_actions import ActionFlow, Picarx, actions_dict, forward, backward

def turn_left(car):
    car.set_dir_servo_angle(-30)
    car.forward(5)
    time.sleep(1)
    car.stop()
    car.set_dir_servo_angle(0)

def turn_right(car):
    car.set_dir_servo_angle(30)
    car.forward(5)
    time.sleep(1)
    car.stop()
    car.set_dir_servo_angle(0)

# Dummy scan function to add in actions_dict keys
# Real logic is overridden in client.py
def scan(car):
    pass

actions_dict.clear()
actions_dict["forward"] = forward
actions_dict["backward"] = backward
actions_dict["turn_left"] = turn_left
actions_dict["turn_right"] = turn_right
actions_dict["scan"] = scan
