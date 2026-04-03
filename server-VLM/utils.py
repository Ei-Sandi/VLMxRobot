import json
from pathlib import Path
from typing import Any, Dict, Optional

def load_system_prompt() -> str:
    """Load the canonical system prompt from prompts/system_prompt.txt."""
    prompt_path = Path(__file__).resolve().parent / "prompts" / "system_prompt.txt"
    try:
        return prompt_path.read_text(encoding="utf-8").strip()
    except OSError:
        # Safe fallback so imports do not crash in misconfigured environments.
        return "You are a safe robot navigation assistant. Always output valid JSON and stop if unsure."

def load_task_templates() -> Dict[str, Any]:
    """Load reusable task templates used to steer VLM behavior."""
    templates_path = Path(__file__).resolve().parent / "prompts" / "task_templates.json"
    try:
        return json.loads(templates_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

TASK_TEMPLATES = load_task_templates()

def get_task_guidance(user_prompt: str, vlm=None) -> Optional[str]:
    """
    Select a task template from the user prompt using the VLM to classify it,
    and convert it into a compact system guidance block (rules + few-shot examples).
    """
    prompt = (user_prompt or "").strip()
    if not prompt or not vlm:
        return None

    available_templates = list(TASK_TEMPLATES.keys())
    if not available_templates:
        return None

    # Ask the VLM to classify the prompt
    sys_msg = (
        f"You are a classification assistant. Categorize the user's prompt into EXACTLY ONE "
        f"of the following categories: {', '.join(available_templates)}. "
        f"If the prompt does not clearly fit any of these, output exactly the word 'None'."
        f"Do not output any other text or punctuation, just the category name."
    )

    try:
        response = vlm.client.chat.completions.create(
            model=vlm.model_name,
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        template_key = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Task classification failed: {e}")
        template_key = "None"

    if template_key == "None" or template_key not in TASK_TEMPLATES:
        return None

    template = TASK_TEMPLATES.get(template_key)

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
