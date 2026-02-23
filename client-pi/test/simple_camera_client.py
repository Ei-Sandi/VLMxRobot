import cv2
import zmq
import sys
import os
import time
from dotenv import load_dotenv

# Add parent directory to path to import local modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera import Camera

load_dotenv() 
SERVER_IP = os.getenv('SERVER_IP')
PORT = os.getenv('SERVER_PORT', '5555')

def main():
    print(f"Connecting to server at tcp://{SERVER_IP}:{PORT}")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{SERVER_IP}:{PORT}")

    print("Initializing camera...")
    camera = Camera(jpeg_quality=70)
    camera.set_config(1920, 1080)
    camera.start()
    print("Starting capture loop...")
    for i in range(20):
        _ = camera.capture_array()
        time.sleep(0.1)
    
    try:
        print("Capturing and encoding image...")
        buffer = camera.capture_and_encode()
    except Exception as e:
        print(f"Error capturing image: {e}")
        camera.clean_up()
        return

    camera.clean_up()
    
    socket.send(buffer)
    
    print("Waiting for reply...")
    message = socket.recv()
    print(f"Received reply: {message}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        SERVER_IP = sys.argv[1]
    main()
