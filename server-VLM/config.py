import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

def _load_system_prompt() -> str:
	"""Load the canonical system prompt from prompts/system_prompt.txt."""
	prompt_path = Path(__file__).resolve().parent / "prompts" / "system_prompt.txt"
	try:
		return prompt_path.read_text(encoding="utf-8").strip()
	except OSError:
		# Safe fallback so imports do not crash in misconfigured environments.
		return "You are a safe robot navigation assistant. Always output valid JSON and stop if unsure."


def _load_task_templates() -> Dict[str, Any]:
	"""Load reusable task templates used to steer VLM behavior."""
	templates_path = Path(__file__).resolve().parent / "prompts" / "task_templates.json"
	try:
		return json.loads(templates_path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError):
		return {}


def get_task_guidance(user_prompt: str) -> Optional[str]:
	"""
	Select a task template from the user prompt and convert it into a compact
	system guidance block (rules + few-shot examples).
	"""
	prompt = (user_prompt or "").lower()

	template_key = None
	if any(k in prompt for k in ["safeguard", "blocked", "obstacle", "avoid", "collision"]):
		template_key = "obstacle_avoidance"
	elif any(k in prompt for k in ["find", "search", "locate", "look for", "scan"]):
		template_key = "search_and_scan"
	elif any(k in prompt for k in ["go to", "approach", "reach", "move to"]):
		template_key = "approach_target"

	if not template_key:
		return None

	template = TASK_TEMPLATES.get(template_key)
	if not template:
		return None

	lines = [
		f"Active task template: {template_key}",
		f"Description: {template.get('description', '')}",
		"Task-specific rules:",
		template.get("task_specific_rules", "")
	]

	examples = template.get("few_shot_examples", [])[:2]
	if examples:
		lines.append("Few-shot examples:")
		for idx, ex in enumerate(examples, start=1):
			user_input = ex.get("user_input", "")
			assistant_output = json.dumps(ex.get("assistant_output", {}), ensure_ascii=False)
			lines.append(f"Example {idx} user: {user_input}")
			lines.append(f"Example {idx} assistant: {assistant_output}")

	lines.append("Follow the base output schema exactly.")
	return "\n".join(lines)

# Server Configuration
PORT = 5555

STOP_COMMAND = { "action": "stop", "speed": 0, "angle": 0, "duration": 0 }

# VLM_API_KEY = "ollama"
# VLM_BASE_URL = "http://localhost:11434/v1"
# VLM_MODEL_NAME = "llava:7b"

VLM_API_KEY = os.getenv("VLM_API_KEY", "your-google-api-key-here")
VLM_BASE_URL = os.getenv("VLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
VLM_MODEL_NAME = os.getenv("VLM_MODEL_NAME", "gemini-robotics-er-1.5-preview")
SYSTEM_PROMPT = _load_system_prompt()
TASK_TEMPLATES = _load_task_templates()
