from abc import ABC, abstractmethod
from typing import Dict, Any
import numpy as np


class VLM(ABC):
    """Abstract base class for Vision Language Models."""
    
    def __init__(self, model_name: str, system_prompt: str):
        self.model_name = model_name
        self.system_prompt = system_prompt
    
    @abstractmethod
    def analyze_frame(self, frame: np.ndarray, temperature: float = 0.5) -> Dict[str, Any]:
        """Analyze a frame and return results."""
        pass
    
    @staticmethod
    def create(provider: str, model_name: str, system_prompt: str, **kwargs):
        """Factory method to create VLM instances."""
        if provider.lower() == "gemini":
            from gemini_client import GeminiClient
            google_api_key = kwargs.get("google_api_key")
            if not google_api_key:
                raise ValueError("google_api_key is required for Gemini")
            return GeminiClient(model_name, google_api_key, system_prompt)
        
        elif provider.lower() == "ollama":
            from ollama_client import OllamaClient
            ollama_url = kwargs.get("ollama_url")
            if not ollama_url:
                raise ValueError("ollama_url is required for Ollama")
            return OllamaClient(model_name, ollama_url, system_prompt)
        
        else:
            raise ValueError(f"Unknown provider: {provider}. Choose 'gemini' or 'ollama'")
