import cv2
import base64
import json
import requests
from typing import Dict, Any
import numpy as np
from vlm import VLM

class OllamaClient(VLM):
    def __init__(self, model_name: str, ollama_url: str, system_prompt: str):
        super().__init__(model_name, system_prompt)
        self.ollama_url = ollama_url
    
    def analyze_frame(self, frame: np.ndarray, temperature: float = 0.1) -> Dict[str, Any]:
        _, buffer_jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer_jpg).decode('utf-8')
        
        payload = {
            "model": self.model_name,
            "prompt": self.system_prompt,
            "stream": False,
            "format": "json",
            "images": [jpg_as_text],
            "options": {
                "temperature": temperature
            }
        }
        
        response = requests.post(self.ollama_url, json=payload)
        response.raise_for_status()
        
        ollama_response = response.json()
        response_text = ollama_response.get('response', '')
        
        try:
            result = json.loads(response_text)
            
            if 'reasoning' in result and 'command' in result:
                return result
            elif 'action' in result and 'speed' in result:
                action = result.get('action', 'unknown')
                return {
                    "reasoning": f"Moving {action}.",
                    "command": result
                }
            else:
                raise ValueError(f"Unexpected response structure: {result}")
                
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {response_text}")
            raise ValueError(f"Invalid JSON response from model: {e}")