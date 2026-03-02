import cv2
import zmq
import numpy as np
from config import PORT, STOP_COMMAND, VLM_API_KEY, VLM_BASE_URL, VLM_MODEL_NAME, SYSTEM_PROMPT
from vlm_cw import VLM

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")

    vlm = VLM(
        api_key=VLM_API_KEY,
        base_url=VLM_BASE_URL,
        model_name=VLM_MODEL_NAME,
        system_prompt=SYSTEM_PROMPT
    )
    
    print(f"Server listening on port {PORT}")
    print(f"Using VLM Model: {VLM_MODEL_NAME} at {VLM_BASE_URL}")
    print("Press 'q' in the video window to stop.")

    try:
        while True:
            parts = socket.recv_multipart()
            prompt_bytes, buffer = parts
            prompt = prompt_bytes.decode('utf-8')

            nparr = np.frombuffer(buffer, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            response = {
                "reasoning": "Frame not received",
                "status": "completed",
                "command": STOP_COMMAND
            }
            
            if frame is None:
                print("Frame not received! Stopping robot.")
            else: 
                cv2.imshow("PiCar-X VLM Stream", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
                try:
                    result = vlm.analyze_frame(frame, prompt=prompt)
                    print(result)
                    response = result
                except Exception as e:
                    print(f"Error analyzing frame: {e}")
                    response = {
                        "reasoning": f"Error: {str(e)}",
                        "status": "completed",
                        "command": STOP_COMMAND
                    }
            
            socket.send_json(response)
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        socket.close()
        cv2.destroyAllWindows()
        print("Server stopped.")

if __name__ == "__main__":
    main()