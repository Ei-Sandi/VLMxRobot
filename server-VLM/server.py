import cv2
import logging
from config import PORT, STOP_COMMAND, VLM_API_KEY, VLM_BASE_URL, VLM_MODEL_NAME, SYSTEM_PROMPT
from core.network.zmq_handler import ZMQServer
from core.models.vlm_wrapper import VLM
from core.memory.context import ContextManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    server = ZMQServer(port=PORT)
    server.start()

    vlm = VLM(
        api_key=VLM_API_KEY,
        base_url=VLM_BASE_URL,
        model_name=VLM_MODEL_NAME
    )
    
    context_manager = ContextManager(max_history_turns=30)
    
    print(f"Using VLM Model: {VLM_MODEL_NAME} at {VLM_BASE_URL}")
    print("Press 'q' in the video window to stop.")

    try:
        while True:
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

            resized_frame = cv2.resize(frame, (336, 224))

            cv2.imshow("PiCar-X VLM Stream", resized_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
            try:
                context_manager.add_user_message(prompt, resized_frame)
                messages = context_manager.get_messages(SYSTEM_PROMPT)
                
                result = vlm.generate(messages)
                
                parsed_command = result["parsed_command"]
                raw_text = result["raw_text"]
                
                usage = result.get("usage")
                if usage:
                    prompt_tokens = usage["prompt_tokens"]
                    output_tokens = usage["output_tokens"]
                    eval_seconds = usage["eval_seconds"]
                    tps = output_tokens / eval_seconds if eval_seconds > 0 else 0
                    print("-" * 20)
                    print(f"Prompt Tokens: {prompt_tokens}")
                    print(f"Output Tokens: {output_tokens}")
                    print(f"Speed: {tps:.2f} tokens per second")
                
                context_manager.add_assistant_message(raw_text)

                print(parsed_command)
                
                # Remove large text fields so we don't send them to the client side over ZeroMQ
                parsed_command.pop("image_description", None)
                parsed_command.pop("goal", None)
                parsed_command.pop("plan", None)
                
                response = parsed_command
                
            except Exception as e:
                logger.error(f"Error analyzing frame: {e}")
                context_manager.remove_last_user_message()
                response = {
                    "reasoning": f"System error during analysis: {str(e)}",
                    "status": "completed",
                    "command": STOP_COMMAND
                }
            
            server.send_response(response)
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.close()
        cv2.destroyAllWindows()
        print("Server stopped.")

if __name__ == "__main__":
    main()
