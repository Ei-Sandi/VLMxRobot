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

actions_dict = {
    "forward": Actions.move_forward,
    "backward": Actions.move_backward,
    "stop": Actions.stop
}