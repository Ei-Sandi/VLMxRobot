import cv2
import zmq
import numpy as np
from config import PORT, DEFAULT_COMMAND, STOP_COMMAND, MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT
from ollama_client import OllamaClient

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")

    ollama = OllamaClient(MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT)
    
    print(f"Server listening on port {PORT}...")
    print("Press 'q' in the video window to stop.")

    try:
        while True:    
            try:
                buffer = socket.recv()
                nparr = np.frombuffer(buffer, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                command = DEFAULT_COMMAND
                
                if frame is None:
                    print("Frame not received! Stopping robot.")
                    command = STOP_COMMAND
                else: 
                    cv2.imshow("PiCar-X VLM Stream", frame)
                    try:
                        result = ollama.analyze_frame(frame)
                        print(result)
                    except Exception as e:
                        print(f"Error analyzing frame: {e}")
                    
                socket.send_json(command)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except zmq.ZMQError as e:
                print(f"ZMQ Error: {e}")
                break
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        socket.close()
        cv2.destroyAllWindows()
        print("Server stopped.")

if __name__ == "__main__":
    main()