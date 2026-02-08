import zmq
import os
from camera import Camera
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
    for i in range(5):
        _ = camera.capture_array()
        time.sleep(0.1)
    print("Camera ready!")

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 900000) 
    socket.setsockopt(zmq.SNDTIMEO, 2000) 
    socket.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            try:
                buffer = camera.capture_and_encode()
                start_time = time.time()
                socket.send(buffer)
                message = socket.recv_json()
                end_time = time.time()
                response_time = end_time - start_time
                print(f"Received Command: {message}")
                print(f"Response time: {response_time:.3f} seconds")
            except KeyboardInterrupt:
                print("\nStopping...")
                break
    finally:
        camera.clean_up()
        socket.close()

if __name__ == "__main__":
    main()