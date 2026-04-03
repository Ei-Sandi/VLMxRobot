import time
from picarx import Picarx

class Actions:
    @staticmethod
    def wait_for_duration(duration, car, check_safeguard):
        start_time = time.time()
        while time.time() - start_time < duration:
            if check_safeguard and check_safeguard(car):
                return True
            time.sleep(0.05)
        return False

    @staticmethod
    def move_forward(car, speed=5, angle=0, duration=1, check_safeguard=None):
        car.set_dir_servo_angle(angle)
        car.forward(speed)
        
        triggered = Actions.wait_for_duration(duration, car, check_safeguard)
        
        car.stop()
        car.set_dir_servo_angle(0) 

        if triggered:
            return "safeguard"

    @staticmethod
    def move_backward(car, speed=5, angle=0, duration=1, check_safeguard=None):
        car.set_dir_servo_angle(-angle)
        car.backward(speed)
        
        time.sleep(duration)
        
        car.stop()
        car.set_dir_servo_angle(0)

    @staticmethod
    def stop(car, speed=0, angle=0, duration=0, check_safeguard=None):
        car.stop()
        car.set_dir_servo_angle(0)

    @staticmethod
    def look_left(car, angle=35, duration=1, check_safeguard=None):
        car.set_cam_pan_angle(angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def look_right(car, angle=35, duration=1, check_safeguard=None):
        car.set_cam_pan_angle(-angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def look_up(car, angle=35, duration=1, check_safeguard=None):
        car.set_cam_tilt_angle(angle)
        time.sleep(duration)
        return "capture"

    @staticmethod
    def look_down(car, angle=35, duration=1, check_safeguard=None):
        car.set_cam_tilt_angle(-angle)
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
