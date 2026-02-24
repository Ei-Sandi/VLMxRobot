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

def main():
    camera = Camera(jpeg_quality=70)
    camera.set_config(1920, 1080)
    camera.start()
    print(f"Camera initialized.")
    
    print("Warming up camera...")
    for i in range(60):
        _ = camera.capture_array()
        time.sleep(0.1)
    print("Camera ready!")
    
    speaker = Speaker() 

    px = Picarx()
    executor = Executor(px)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 300000) 
    socket.setsockopt(zmq.SNDTIMEO, 2000) 
    socket.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            try:
                prompt = input("Enter instruction: ") 

                speaker.speak(prompt)
                    
                if prompt.lower() in ["bye", "exit"]:
                    break

                speaker.speak(prompt)
                
                while True:
                    buffer = camera.capture_and_encode()
                    start_time = time.time()
                    
                    socket.send_string(prompt, flags=zmq.SNDMORE)
                    socket.send(buffer)
                    
                    message = socket.recv_json()
                    end_time = time.time()
                    
                    command = message.get('command', '')
                    reasoning = message.get('reasoning', '')
                    status = message.get('status', 'running')

                    if reasoning:
                        speaker.speak(reasoning)
                    
                    if status == "completed":
                        break
                        
                    if command:
                        executor.execute(command)
                        print(f"Executed Command: {command}")

                    response_time = end_time - start_time
                    print(f"Response time: {response_time:.3f} seconds")
            
            except zmq.Again:
                print("Server timeout...")
                continue

            except KeyboardInterrupt:
                print("\nStopping...")
                break
    finally:
        camera.clean_up()
        socket.close()

if __name__ == "__main__":
    main()