import os
from dotenv import load_dotenv
from utils import load_system_prompt

load_dotenv()

# Server Configuration
PORT = 5555

STOP_COMMAND = { "action": "stop", "speed": 0, "angle": 0, "duration": 0 }

# VLM_API_KEY = "ollama"
# VLM_BASE_URL = "http://localhost:11434/v1"
# VLM_MODEL_NAME = "llava:7b"

VLM_API_KEY = os.getenv("VLM_API_KEY", "your-google-api-key-here")
VLM_BASE_URL = os.getenv("VLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
VLM_MODEL_NAME = os.getenv("VLM_MODEL_NAME", "gemini-robotics-er-1.5-preview")
SYSTEM_PROMPT = load_system_prompt()
