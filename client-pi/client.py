import zmq
import os
import cv2
import numpy as np
from camera import Camera
from speaker import Speaker
from picarx import Picarx
from executor import Executor
from dotenv import load_dotenv
import time

load_dotenv() 
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT', '5555')

if not SERVER_IP:
    raise ValueError("SERVER_IP not set in .env file")

def check_safeguard(car=None):
    if car is None: return False
    try:
        distance = round(car.ultrasonic.read(), 2)
        if distance <= 10:
            print(f"Safeguard triggered! Distance: {distance}")
            return True
    except Exception as e:
        print(f"Safeguard check failed: {e}")
    return False

def main():
    camera = None
    socket = None
    px = None
    try:
        camera = Camera(jpeg_quality=70)
        camera.set_config(1920, 1080)
        camera.start()
        print("Camera initialized.")
        
        print("Warming up camera...")
        for i in range(30):
            _ = camera.capture_array()
            time.sleep(0.1)
        print("Camera ready!")
        
        speaker = Speaker() 
        px = Picarx()

        print("Resetting servos to 0 degrees...")
        px.reset()
        time.sleep(0.5)

        executor = Executor(px, speaker, check_safeguard=check_safeguard)

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.RCVTIMEO, 300000) 
        socket.setsockopt(zmq.SNDTIMEO, 2000) 
        socket.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")
        print(f"Connected to {SERVER_IP}:{SERVER_PORT}")

        prompt = None
        skip_next_capture = False
        while True:
            try:
                if prompt is None:
                    prompt = input("Enter instruction: ") 
                    speaker.speak(prompt)
                        
                    if prompt.lower() in ["bye", "exit"]:
                        break
                
                if not skip_next_capture:
                    buffer = camera.capture_and_encode()
                skip_next_capture = False
                
                start_time = time.time()
                
                socket.send_string(prompt, flags=zmq.SNDMORE)
                socket.send(buffer)
                prompt = ""  
                
                message = socket.recv_json()
                end_time = time.time()
                
                command = message.get('command', '')
                reasoning = message.get('reasoning', '')
                status = message.get('status', 'running')

                if reasoning:
                    speaker.speak(reasoning)

                if command:
                    command_result = executor.execute(command) 
                    print(f"Executed Command: {command}")
                    
                    if command_result == "capture":
                        buffer = camera.capture_and_encode()
                        px.set_cam_pan_angle(0)
                        px.set_cam_tilt_angle(0)
                        skip_next_capture = True
                        continue

                    if isinstance(command, dict) and command.get("action") == "ask":
                        prompt = input("Answer: ") 
                        continue

                    if command_result == "safeguard":
                        prompt = "Safeguard triggered! There is an object in front of you."
                        continue

                if status == "completed":
                    speaker.speak("Task completed. What should I do next?")
                    prompt = None

                response_time = end_time - start_time
                print(f"Response time: {response_time:.3f} seconds")
                time.sleep(1)
            
            except zmq.Again:
                print("Server timeout. Reconnecting to recover state...")
                socket.close()
                socket = context.socket(zmq.REQ)
                socket.setsockopt(zmq.RCVTIMEO, 300000) 
                socket.setsockopt(zmq.SNDTIMEO, 2000) 
                socket.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")
                prompt = None 
                continue

            except KeyboardInterrupt:
                print("\nStopping...")
                break
    finally:
        if camera: camera.clean_up()
        if socket: socket.close()
        if px: px.close() 

if __name__ == "__main__":
    main()
