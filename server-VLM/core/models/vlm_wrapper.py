import logging
import sys
import os
from typing import Dict, Any
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.actions.parser import ActionParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VLM:
    """
    VLM Wrapper using the standard OpenAI client.
    Can be pointed to OpenAI, vLLM, Ollama, or any compatible endpoint.
    """
    def __init__(self, api_key: str, base_url: str, model_name: str):
        logger.info(f"Initializing VLM Client for model: {model_name} at {base_url}")
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_name = model_name

    def generate(self, messages: list, temperature: float = 0.1) -> Dict[str, Any]:
        """
        Sends the compiled message history to the VLM and parses the output.
        """
        try:
            logger.info("Sending request to VLM API...")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"} 
            )
            
            response_content = response.choices[0].message.content
            logger.info(f"VLM responded with {len(response_content)} characters.")
            
            parser = ActionParser()
            result = parser.parse(response_content)
            
            return {
                "parsed_command": result,
                "raw_text": response_content
            }

        except Exception as e:
            logger.error(f"VLM API Error: {str(e)}")
            parser = ActionParser()
            fallback = parser.get_safe_fallback(f"VLM API Error: {str(e)}")
            return {
                "parsed_command": fallback,
                "raw_text": "" 
            }
