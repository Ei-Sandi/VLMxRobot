import os
import sys
import cv2
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GEMINI_MODEL_NAME, SYSTEM_PROMPT
from gemini_client import GeminiClient

def test_gemini(image_path: str):
    """Test Gemini with a static image."""
    load_dotenv()
    
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    print(f"Image loaded: {image_path}")
    print(f"Image shape: {frame.shape}")
    print(f"Model: {GEMINI_MODEL_NAME}")
    print("-" * 50)
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    
    gemini = GeminiClient(GEMINI_MODEL_NAME, google_api_key, SYSTEM_PROMPT)
    
    print("Analyzing image...")
    result = gemini.analyze_frame(frame)
    
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_gemini.py <image_path>")
        sys.exit(1)
    
    test_gemini(sys.argv[1])
