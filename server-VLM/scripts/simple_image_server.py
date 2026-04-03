import zmq
import cv2
import numpy as np
import sys
import os
import time

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import PORT
except ImportError:
    PORT = 5555

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    print(f"Binding to tcp://*:{PORT}")
    socket.bind(f"tcp://*:{PORT}")

    print("Waiting for image...")
    
    message = socket.recv()
    
    print(f"Received message of length {len(message)}")
    
    try:
        nparr = np.frombuffer(message, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is not None:
            timestamp = int(time.time())
            filename = f"single_image_{timestamp}.jpg"
            cv2.imwrite(filename, img)
            print(f"Saved image to {filename}")
            
        else:
            try:
                text = message.decode('utf-8')
                print(f"Message is text: {text}")
            except:
                print(f"Message is binary data of length {len(message)}")
    except Exception as e:
        print(f"Error processing message: {e}")
    
    response = {
        "reasoning": "Moving forward 2cm",
        "command": ["forward", {"speed": 5, "duration": 0.5}]
    }

    socket.send_json(response)
    print(f"Sent response: {response}")
    
    print("Terminating server.")
    socket.close()
    context.term()

if __name__ == "__main__":
    main()
