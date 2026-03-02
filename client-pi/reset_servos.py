from picarx import Picarx
import time

def reset_servos():
    print("Initializing PiCar-X...")
    px = Picarx()
    
    print("Resetting servos to 0 degrees...")
    
    px.set_dir_servo_angle(0)
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    
    time.sleep(0.5)
    print("Servos reset complete.")

if __name__ == "__main__":
    reset_servos()
