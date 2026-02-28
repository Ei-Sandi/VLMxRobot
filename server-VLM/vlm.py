import base64
import json
import cv2
import numpy as np
from typing import Dict, Any
from openai import OpenAI

class VLM:
    def __init__(self, api_key: str, base_url: str, model_name: str, system_prompt: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_name = model_name
        self.system_prompt = system_prompt

    def analyze_frame(self, frame: np.ndarray, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Analyze a frame using the configured VLM model via OpenAI-compatible API."""
        
        _, buffer_jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer_jpg).decode('utf-8')
        
        # Construct messages
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"User Instruction: {prompt}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{jpg_as_text}"
                        }
                    }
                ]
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"} # Ensure JSON output if supported
            )
            
            response_content = response.choices[0].message.content
            
            # Clean up the response if it contains markdown code blocks
            if "```json" in response_content:
                response_content = response_content.split("```json")[1].split("```")[0].strip()
            elif "```" in response_content:
                response_content = response_content.split("```")[1].split("```")[0].strip()

            result = json.loads(response_content)
            
            # Validate basic structure
            required_keys = ["reasoning", "status", "command"]
            if not all(k in result for k in required_keys):
                # Try to salvage partial response or wrap it
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
            # Could return a fallback error response
            return {
                "reasoning": f"JSON Parse Error: {str(e)}",
                "status": "completed",
                "command": {"action": "stop", "speed": 0, "angle": 0, "duration": 0}
            }
        except Exception as e:
            print(f"VLM API Error: {str(e)}")
            raise e
