import zmq
import os
import cv2
import numpy as np
from camera import Camera
from speaker import Speaker
from picarx.preset_actions import Picarx, ActionFlow
from panorama import PanoramaScanner
from dotenv import load_dotenv
import time

load_dotenv() 
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT', '5555')

if not SERVER_IP:
    raise ValueError("SERVER_IP not set in .env file")

def main():
    camera = Camera(jpeg_quality=70)
    camera.set_config(640, 480)
    camera.start()
    print(f"Camera initialized.")
    
    print("Warming up camera...")
    for i in range(60):
        _ = camera.capture_array()
        time.sleep(0.1)
    print("Camera ready!")
    
    speaker = Speaker()

    px = Picarx()
    flow = ActionFlow(px)
    flow.start()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 900000) 
    socket.setsockopt(zmq.SNDTIMEO, 2000) 
    socket.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")

    scanner = PanoramaScanner(px, camera)
    
    encoded_grid = scanner.scan()
    if encoded_grid:
        socket.send_multipart(encoded_grid)
        ack = socket.recv_json()
        if 'reasoning' in ack:
            speaker.speak(ack['reasoning'])

    try:
        while True:
            try:
                buffer = camera.capture_and_encode()
                start_time = time.time()

                socket.send(buffer)
                
                message = socket.recv_json()
                end_time = time.time()
                
                command = message.get('command', '')

                if command == 'scan':
                    encoded_grid = scanner.scan()
                    if encoded_grid:
                        socket.send_multipart(encoded_grid)
                        message = socket.recv_json()
                    else:
                        message = {} 
                    
                    command = '' 
                
                if message and 'reasoning' in message:
                    speaker.speak(message['reasoning'])

                if command:
                    flow.add_action(command)
                    flow.wait_actions_done()
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
        flow.stop()
        socket.close()

if __name__ == "__main__":
    main()