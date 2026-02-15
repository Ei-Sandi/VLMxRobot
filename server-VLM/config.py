import os
from dotenv import load_dotenv

load_dotenv()

# Server Configuration
PORT = 5555

DEFAULT_COMMAND = {
    "action": "forward",
    "speed": 40
}

STOP_COMMAND = {
    "action": "stop",
    "speed": 0
}

# VLM Provider Configuration
VLM_PROVIDER = "gemini"  # "ollama" or "gemini"

GEMINI_MODEL_NAME = "gemini-robotics-er-1.5-preview"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_NAME = "gemma3:4b-it-qat"

# Default system prompt (can be overridden via SYSTEM_PROMPT env variable)
DEFAULT_SYSTEM_PROMPT = """
You are the visual navigation system for a small robot car (PiCar-X).
Analyze the image provided.
Your goal is to navigate open space and avoid obstacles.

OUTPUT FORMAT:
You must output a STRICT JSON object with no markdown formatting.
The JSON must have two fields:
1. "reasoning": A short string explaining what you see (e.g., "Clear path ahead", "Wall close").
2. "command": An object containing "action" (forward, left, right, backward, stop) and "speed" (0-100).

EXAMPLE RESPONSE:
{
    "reasoning": "The path is clear, but there is a table leg on the left.",
    "command": {"action": "forward", "speed": 40}
}

CRITICAL RULES:
- If the image is blurry or dark, STOP.
- If an obstacle is very close (taking up >50% of view), STOP or turn.
- Do NOT output markdown code blocks (```json). Just the raw JSON.
"""

# Allow override from environment variable
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)