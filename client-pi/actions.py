import time
from picarx import Picarx

class Actions:
    @staticmethod
    def move_forward(car, speed=5, angle=0, duration=1):
        car.set_dir_servo_angle(angle)
        car.forward(speed)
        time.sleep(duration)
        car.stop()
        car.set_dir_servo_angle(0) 

    @staticmethod
    def move_backward(car, speed=5, angle=0, duration=1):
        car.set_dir_servo_angle(angle)
        car.backward(speed)
        time.sleep(duration)
        car.stop()
        car.set_dir_servo_angle(0)
    
    @staticmethod
    def stop(car, speed=0, angle=0, duration=0):
        car.stop()
        car.set_dir_servo_angle(0)

    @staticmethod
    def look_left(car, angle=35, duration=1):
        car.cam_pan_servo_calibrate(angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def look_right(car, angle=-35, duration=1):
        car.cam_pan_servo_calibrate(angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def look_up(car, angle=35, duration=1):
        car.cam_tilt_servo_calibrate(angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def look_down(car, angle=-35, duration=1):
        car.cam_tilt_servo_calibrate(angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def speak(speaker, text="Hello"):
        if hasattr(speaker, 'speak'):
            speaker.speak(text)
        else:
            print("Speaker object does not have speak method or is None")

    @staticmethod
    def ask(speaker, text=""):
        if hasattr(speaker, 'speak'):
            speaker.speak(text)
        else:
            print("Speaker object does not have speak method or is None")

actions_dict = {
    "forward": Actions.move_forward,
    "backward": Actions.move_backward,
    "stop": Actions.stop,
    "look_left": Actions.look_left,
    "look_right": Actions.look_right,
    "look_up": Actions.look_up,
    "look_down": Actions.look_down,
    "speak": Actions.speak,
    "ask": Actions.ask,
}