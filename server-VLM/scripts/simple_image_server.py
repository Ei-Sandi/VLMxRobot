import zmq
import cv2
import numpy as np
import sys
import os
import time
import json

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

    print("Waiting for multipart (prompt, image)...")

    prompt = ""
    img = None
    parts = socket.recv_multipart()

    print(f"Received {len(parts)} message part(s)")

    try:
        if len(parts) == 2:
            prompt = parts[0].decode("utf-8", errors="replace")
            image_buffer = parts[1]
            print(f"Prompt: {prompt}")
            print(f"Image bytes: {len(image_buffer)}")
            nparr = np.frombuffer(image_buffer, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif len(parts) == 1:
            # Backward-compatible path for older clients
            print("Legacy single-part message received.")
            nparr = np.frombuffer(parts[0], np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            print("Unexpected message format.")

        if img is not None:
            timestamp = int(time.time())
            filename = f"single_image_{timestamp}.jpg"
            cv2.imwrite(filename, img)
            print(f"Saved image to {filename}")
        else:
            print("Failed to decode image payload.")
    except Exception as e:
        print(f"Error processing message: {e}")
    
    response = {
        "reasoning": "Debug server received frame successfully.",
        "plan": ["Acknowledge frame", "Stop for safety"],
        "status": "completed",
        "command": {
            "action": "stop",
            "speed": None,
            "angle": None,
            "duration": None,
            "text": f"Debug ack for prompt: {prompt}" if prompt else None
        }
    }

    socket.send_json(response)
    print(f"Sent response: {json.dumps(response)}")
    
    print("Terminating server.")
    socket.close()
    context.term()

if __name__ == "__main__":
    main()
