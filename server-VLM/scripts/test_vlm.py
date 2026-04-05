import cv2
import sys
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from config import VLM_API_KEY, VLM_BASE_URL, VLM_MODEL_NAME, SYSTEM_PROMPT
    from core.models.vlm_wrapper import VLM
    from core.memory.context import ContextManager
except ImportError as e:
    print(f"Could not import project modules. Error: {e}")
    sys.exit(1)

def test_vlm_manual(image_path, user_prompt):
    print(f"Initializing VLM with:")
    print(f"  Model: {VLM_MODEL_NAME}")
    print(f"  Base URL: {VLM_BASE_URL}")

    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    print(f"Loading image: {image_path}")
    frame = cv2.imread(image_path)
    
    if frame is None:
        print("Error: Failed to load image. Check file format.")
        return

    print("Resizing image to 336x224...")
    frame = cv2.resize(frame, (336, 224))

    vlm_client = VLM(
        api_key=VLM_API_KEY, 
        base_url=VLM_BASE_URL, 
        model_name=VLM_MODEL_NAME
    )
    context = ContextManager(max_history_turns=1)
    context.add_user_message(user_prompt, frame)
    messages = context.get_messages(SYSTEM_PROMPT)

    print("-" * 50)
    print(f"User Prompt: '{user_prompt}'")
    print("Analyzing frame...")
    print("-" * 50)

    try:
        result = vlm_client.generate(messages)
        print("\n--- VLM Response ---")
        print(json.dumps(result["parsed_command"], indent=2))
        print("\n--- Raw Model JSON ---")
        if "raw_text" in result:
            print(repr(result["raw_text"]))
        else:
            print("No raw text returned.")

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

        print("--------------------")
    except Exception as e:
        print(f"\nError during analysis: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_vlm.py <path_to_image> [optional_prompt]")
        print("Example: python3 test_vlm.py test_image.jpg 'Move forward safely'")
    else:
        img_path = sys.argv[1]
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Describe what you see and decide the next move."
        test_vlm_manual(img_path, prompt)
