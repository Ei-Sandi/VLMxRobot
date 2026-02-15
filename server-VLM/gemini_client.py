import json
import cv2
import numpy as np
from typing import Dict, Any
from google import genai
from google.genai import types
from vlm import VLM

class GeminiClient(VLM):
    def __init__(self, model_name: str, google_api_key: str, system_prompt: str):
        super().__init__(model_name, system_prompt)
        self.client = genai.Client(api_key=google_api_key)

    def _create_config(self, temperature: float = 0.5) -> types.GenerateContentConfig:
        """Create a generation config with the specified temperature."""
        return types.GenerateContentConfig(
            temperature=temperature,
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )

    def generate_content(self, image=None, temperature: float = 0.5):
        """Generate content using the Gemini model with optional image input."""
        config = self._create_config(temperature)

        contents = [self.system_prompt]
        if image is not None:
            contents.insert(0, image)

        image_response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config,
        )

        return image_response.text

    def analyze_frame(self, frame: np.ndarray, temperature: float = 0.5) -> Dict[str, Any]:
        """Analyze a frame using Gemini vision model."""
        _, buffer_jpg = cv2.imencode('.jpg', frame)
        
        image_part = types.Part.from_bytes(
            data=buffer_jpg.tobytes(),
            mime_type="image/jpeg"
        )
        
        response_text = self.generate_content(image=image_part, temperature=temperature)
        
        return {"response": response_text}