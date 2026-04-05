import base64
import cv2
import numpy as np
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ContextManager:
    """
    Handles the conversational memory for the VLA.
    Responsible for assembling the system prompt and pruning old images to save bandwidth/tokens.
    """
    def __init__(self, max_history_turns: int = 30):
        self.max_history_turns = max_history_turns
        self.history: List[Dict[str, Any]] = []

    def clear(self):
        """Clears the conversational memory."""
        logger.info("Context memory cleared.")
        self.history = []

    def _encode_image(self, frame: np.ndarray) -> str:
        """Converts an OpenCV numpy array frame to a base64 string."""
        _, buffer_jpg = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer_jpg).decode('utf-8')

    def add_user_message(self, prompt: str, frame: np.ndarray = None):
        """
        Formats the user input and the current image.
        """
        content = []
        
        # Attach the text instruction if provided
        if prompt and prompt.strip():
            content.append({"type": "text", "text": f"User Instruction: {prompt}"})
        
        # Attach the image if provided
        if frame is not None:
            base64_img = self._encode_image(frame)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_img}",
                    "detail": "low" # Use low detail for speed unless you need fine text reading
                }
            })

        self.history.append({"role": "user", "content": content})
        self._prune_history()

    def add_assistant_message(self, response_text: str):
        """Saves the raw JSON text from the VLM into history."""
        # Check to ensure we don't save an empty string from a failed API call
        if response_text:
            self.history.append({"role": "assistant", "content": response_text})

    def remove_last_user_message(self):
        """Used to rollback memory if the API call fails."""
        if len(self.history) > 0 and self.history[-1]["role"] == "user":
            self.history.pop()
            logger.info("Rolled back last user message due to API failure.")

    def _prune_history(self):
        """
        Keeps history under the max_history limit.
        Replaces actual image payloads in older turns with text placeholders 
        to drastically reduce latency and token costs.
        """
        # Truncate oldest messages if we exceed max turns (x2 because user+assistant = 1 turn)
        max_messages = self.max_history_turns * 2
        if len(self.history) > max_messages:
             self.history = self.history[-max_messages:]

        # Iterate through history (excluding the very last user message we just added)
        for msg in self.history[:-1]:
            if msg["role"] == "user" and isinstance(msg["content"], list):
                for item in msg["content"]:
                    if item.get("type") == "image_url":
                        # Replace the heavy base64 string with a short text note to save tokens
                        item["type"] = "text"
                        item["text"] = "[Image redacted]"
                        # Remove the image_url key entirely
                        if "image_url" in item:
                            del item["image_url"]

    def get_messages(self, system_prompt: str) -> List[Dict[str, Any]]:
        """
        Compiles the system prompt and the pruned history into the exact format 
        required by the OpenAI API.
        """
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        # Append the ongoing history
        messages.extend(self.history)
        return messages

    def get_messages_for_debug(self, system_prompt: str) -> List[Dict[str, Any]]:
        """
        Returns a debug-safe view of the message context where image payloads are redacted.
        Useful for terminal logging without printing base64 image content.
        """
        messages = self.get_messages(system_prompt)
        redacted_messages: List[Dict[str, Any]] = []

        for msg in messages:
            content = msg.get("content")

            if isinstance(content, list):
                redacted_content = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "image_url":
                        detail = "low"
                        image_url = item.get("image_url")
                        if isinstance(image_url, dict):
                            detail = image_url.get("detail", "low")

                        redacted_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": "[base64 image omitted]",
                                "detail": detail,
                            },
                        })
                    elif isinstance(item, dict):
                        redacted_content.append(dict(item))
                    else:
                        redacted_content.append(item)

                redacted_messages.append({"role": msg.get("role"), "content": redacted_content})
            elif isinstance(msg, dict):
                redacted_messages.append(dict(msg))
            else:
                redacted_messages.append(msg)

        return redacted_messages
