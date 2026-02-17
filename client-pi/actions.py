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

def scan(car):
    tilt_angles = [30, 0, -30]
    pan_start = -45
    pan_end = 45
    step = 10  # Speed of scan (higher = faster)

    for tilt in tilt_angles:
        car.set_cam_tilt_angle(tilt)
        
        for pan in range(pan_start, pan_end + 1, step):
            car.set_cam_pan_angle(pan)
            time.sleep(0.05)        
        time.sleep(0.1) 
        
    car.set_cam_tilt_angle(0)
    car.set_cam_pan_angle(0)

actions_dict.clear()
actions_dict["forward"] = forward
actions_dict["backward"] = backward
actions_dict["turn_left"] = turn_left
actions_dict["turn_right"] = turn_right
actions_dict["scan"] = scan
