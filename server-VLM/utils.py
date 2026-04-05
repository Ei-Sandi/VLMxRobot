import json
from pathlib import Path
from typing import Any, Dict, Optional

def load_system_prompt() -> str:
    """Load the canonical system prompt from prompts/system_prompt.txt."""
    prompt_path = Path(__file__).resolve().parent / "prompts" / "system_prompt.txt"
    try:
        return prompt_path.read_text(encoding="utf-8").strip()
    except OSError:
        return "You are a safe robot navigation assistant. Always output valid JSON and stop if unsure."
