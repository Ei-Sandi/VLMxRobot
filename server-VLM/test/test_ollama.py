import os
import sys
import cv2

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OLLAMA_MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT
from ollama_client import OllamaClient


def test_ollama(image_path: str):
    """Test Ollama with a static image."""
    
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    print(f"Image loaded: {image_path}")
    print(f"Image shape: {frame.shape}")
    print(f"Model: {OLLAMA_MODEL_NAME}")
    print("-" * 50)
    
    ollama = OllamaClient(OLLAMA_MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT)
    
    print("Analyzing image...")
    result = ollama.analyze_frame(frame)
    
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_ollama.py <image_path>")
        sys.exit(1)
    
    test_ollama(sys.argv[1])
