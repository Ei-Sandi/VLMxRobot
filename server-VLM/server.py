import os
import cv2
import zmq
import numpy as np
from dotenv import load_dotenv
from config import PORT, DEFAULT_COMMAND, STOP_COMMAND, OLLAMA_MODEL_NAME, OLLAMA_URL, GEMINI_MODEL_NAME, SYSTEM_PROMPT, VLM_PROVIDER
from vlm import VLM

def main():
    load_dotenv()
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")

    provider = os.getenv("VLM_PROVIDER", VLM_PROVIDER).lower()
    
    if provider == "gemini":
        google_api_key = os.getenv("GOOGLE_API_KEY")
        vlm = VLM.create("gemini", GEMINI_MODEL_NAME, SYSTEM_PROMPT, google_api_key=google_api_key)
    else:
        vlm = VLM.create("ollama", OLLAMA_MODEL_NAME, SYSTEM_PROMPT, ollama_url=OLLAMA_URL)
    
    print(f"Server listening on port {PORT} using {provider.upper()} provider")
    print("Press 'q' in the video window to stop.")

    try:
        while True:
            buffer = socket.recv()
            nparr = np.frombuffer(buffer, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            command = DEFAULT_COMMAND
            
            if frame is None:
                print("Frame not received! Stopping robot.")
                command = STOP_COMMAND
            else: 
                cv2.imshow("PiCar-X VLM Stream", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
                try:
                    result = vlm.analyze_frame(frame)
                    print(result)
                except Exception as e:
                    print(f"Error analyzing frame: {e}")
            
            socket.send_json(command)
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        socket.close()
        cv2.destroyAllWindows()
        print("Server stopped.")

if __name__ == "__main__":
    main()