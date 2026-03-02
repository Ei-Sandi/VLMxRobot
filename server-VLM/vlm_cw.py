import base64
import json
import cv2
import numpy as np
from typing import Dict, Any
from openai import OpenAI

class VLM:
    def __init__(self, api_key: str, base_url: str, model_name: str, system_prompt: str, max_history_turns: int = 30):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_name = model_name
        self.system_prompt = system_prompt
        
        self.context_window = []
        self.max_history_turns = max_history_turns

    def clear_context(self):
        """Clears the conversational memory."""
        self.context_window = []

    def _trim_and_optimize_context(self):
        """Keeps context within limits and replaces past images with text placeholders."""
        # Max history limit = user msg + assistant msg
        max_messages = self.max_history_turns * 2
        if len(self.context_window) > max_messages:
            self.context_window = self.context_window[-max_messages:]

        for i, msg in enumerate(self.context_window):
            if i == len(self.context_window) - 1:
                continue

            if msg["role"] == "user" and isinstance(msg["content"], list):
                text_instruction = ""
                for item in msg["content"]:
                    if item["type"] == "text":
                        text_instruction = item["text"]
                
                msg["content"] = f"{text_instruction}\n[Image from this past turn has been removed. Refer to 'reasoning' and 'plan' in the corresponding Assistant response.]"


    def analyze_frame(self, frame: np.ndarray, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Analyze a frame using the configured VLM model via OpenAI-compatible API."""
        
        _, buffer_jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer_jpg).decode('utf-8')

        if not prompt or prompt.strip() == "":
            instruction_text = "System Note: No new user instruction. Continue autonomous execution based on your previous reasoning and goal."
        else:
            instruction_text = f"User Instruction: {prompt}"
        
        user_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": instruction_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{jpg_as_text}"
                    }
                }
            ]
        }

        self.context_window.append(user_message)

        messages = [{"role": "system", "content": self.system_prompt}] + self.context_window

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            
            response_content = response.choices[0].message.content
            
            self.context_window.append({
                "role": "assistant",
                "content": response_content
            })            

            self._trim_and_optimize_context()

            if "```json" in response_content:
                response_content = response_content.split("```json")[1].split("```")[0].strip()
            elif "```" in response_content:
                response_content = response_content.split("```")[1].split("```")[0].strip()

            result = json.loads(response_content)
            
            required_keys = ["reasoning", "status", "command"]
            if not all(k in result for k in required_keys):
                if "command" in result:
                    if "reasoning" not in result:
                        result["reasoning"] = "Command generated without reasoning."
                    if "status" not in result:
                        result["status"] = "running"
                    return result
                else: 
                     raise ValueError(f"Missing required keys in response: {result.keys()}")

            return result

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {response_content}")
            return {
                "reasoning": f"JSON Parse Error: {str(e)}",
                "status": "completed",
                "command": {"action": "stop", "speed": 0, "angle": 0, "duration": 0}
            }
        except Exception as e:
            print(f"VLM API Error: {str(e)}")
            if self.context_window and self.context_window[-1]["role"] == "user":
                self.context_window.pop()
            raise e
            