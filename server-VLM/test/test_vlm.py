import cv2
import sys
import os
import json
import base64
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from vlm import VLM
try:
    from config import VLM_API_KEY, VLM_BASE_URL, VLM_MODEL_NAME, SYSTEM_PROMPT
except ImportError:
    print("Could not import config.py inside the parent directory. Make sure config.py exists.")
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

    vlm_client = VLM(
        api_key=VLM_API_KEY, 
        base_url=VLM_BASE_URL, 
        model_name=VLM_MODEL_NAME, 
        system_prompt=SYSTEM_PROMPT
    )

    print("-" * 50)
    print(f"User Prompt: '{user_prompt}'")
    print("Analyzing frame...")
    print("-" * 50)

    try:
        result = vlm_client.analyze_frame(frame, user_prompt)
        print("\n--- VLM Response ---")
        print(json.dumps(result, indent=2))
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
