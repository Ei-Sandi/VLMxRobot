import logging
import sys
import os
import time
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

    def generate(self, messages: list, temperature: float = 0.1, retries: int = 1) -> Dict[str, Any]:
        """
        Sends the compiled message history to the VLM and parses the output.
        If the output does not match the JSON schema, it prompts the VLM to correct it.
        """
        prompt_tokens_total = 0
        output_tokens_total = 0
        eval_seconds_total = 0.0

        for attempt in range(retries + 1):
            try:
                logger.info(f"Sending request to VLM API... (Attempt {attempt + 1}/{retries + 1})")
                start_time = time.time()
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": "json_object"} 
                )
                end_time = time.time()
                eval_seconds = end_time - start_time
                eval_seconds_total += eval_seconds
                
                message_obj = response.choices[0].message
                response_content = message_obj.content or ""
                reasoning = getattr(message_obj, 'reasoning', None) or ""
                
                logger.info(f"VLM responded with {len(response_content)} characters.")
                if not response_content:
                    logger.error(f"Response content is empty! Full response object: {response}")
                
                prompt_tokens_total += response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0
                output_tokens_total += response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0
                
                parser = ActionParser()
                # Use parser conditionally, checking if it resulted in fallback
                result = parser.parse(response_content)
                
                # Check if it was a parsing error fallback
                if result.get("goal") == "Emergency stop due to error.":
                    if attempt < retries:
                        logger.warning("Formatting failed. Asking VLM to reformat output.")
                        # Append the bad response and ask for a correction
                        
                        assistant_msg = {"role": "assistant", "content": response_content}
                        if reasoning:
                            assistant_msg["content"] = f"<reasoning>\n{reasoning}\n</reasoning>\n{response_content}"
                            
                        messages.append(assistant_msg)
                        messages.append({
                            "role": "user", 
                            "content": "Your previous response was incorrectly formatted or missing the JSON block entirely. Please output ONLY a valid JSON object matching the required schema. Ensure it is not empty."
                        })
                        continue
                    else:
                        logger.error("Max retries reached. Using fallback.")

                return {
                    "parsed_command": result,
                    "raw_text": response_content,
                    "usage": {
                        "prompt_tokens": prompt_tokens_total,
                        "output_tokens": output_tokens_total,
                        "eval_seconds": eval_seconds_total
                    }
                }

            except Exception as e:
                logger.error(f"VLM API Error: {str(e)}")
                if attempt < retries:
                    logger.warning("Retrying due to API error...")
                    continue
                
                parser = ActionParser()
                fallback = parser.get_safe_fallback(f"VLM API Error: {str(e)}")
                return {
                    "parsed_command": fallback,
                    "raw_text": "" 
                }
