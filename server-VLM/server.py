import cv2
import logging
from config import PORT, STOP_COMMAND, VLM_API_KEY, VLM_BASE_URL, VLM_MODEL_NAME, SYSTEM_PROMPT, get_task_guidance
from core.network.zmq_handler import ZMQServer
from core.models.vlm_wrapper import VLM
from core.memory.context import ContextManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize Network
    server = ZMQServer(port=PORT)
    server.start()

    # Initialize VLM
    vlm = VLM(
        api_key=VLM_API_KEY,
        base_url=VLM_BASE_URL,
        model_name=VLM_MODEL_NAME
    )
    
    # Initialize Memory
    context_manager = ContextManager(max_history_turns=30)
    
    print(f"Using VLM Model: {VLM_MODEL_NAME} at {VLM_BASE_URL}")
    print("Press 'q' in the video window to stop.")

    try:
        while True:
            # 1. Block and wait for Robot Client to send image + prompt
            prompt, frame = server.receive_frame()

            response = {
                "reasoning": "Frame not received",
                "status": "completed",
                "command": STOP_COMMAND
            }
            
            if frame is None:
                print("Frame not received! Stopping robot.")
                server.send_response(response)
                continue

            cv2.imshow("PiCar-X VLM Stream", frame)
            
            # Local debug view escape hatch
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
            try:
                # 2. Combine the new prompt and frame with our conversation history
                context_manager.add_user_message(prompt, frame)
                task_guidance = get_task_guidance(prompt)
                messages = context_manager.get_messages(SYSTEM_PROMPT, task_guidance=task_guidance)
                
                # 3. Request inference
                result = vlm.generate(messages)
                
                parsed_command = result["parsed_command"]
                raw_text = result["raw_text"]
                
                # 4. Save the exact raw response to history to fulfill few-shot/memory loop
                context_manager.add_assistant_message(raw_text)
                
                print(parsed_command)
                response = parsed_command
                
            except Exception as e:
                logger.error(f"Error analyzing frame: {e}")
                # Rollback memory so we don't end up out-of-sync
                context_manager.remove_last_user_message()
                response = {
                    "reasoning": f"System error during analysis: {str(e)}",
                    "status": "completed",
                    "command": STOP_COMMAND
                }
            
            # 5. Send the safely parsed dictionary back to the robot execution pipeline
            server.send_response(response)
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.close()
        cv2.destroyAllWindows()
        print("Server stopped.")

if __name__ == "__main__":
    main()
