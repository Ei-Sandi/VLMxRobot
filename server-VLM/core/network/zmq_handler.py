import zmq
import cv2
import numpy as np
import logging
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ZMQServer:
    def __init__(self, port: int):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        
    def start(self):
        self.socket.bind(f"tcp://*:{self.port}")
        logger.info(f"ZMQ Server listening on port {self.port}")

    def receive_frame(self) -> Tuple[str, Optional[np.ndarray]]:
        """Receives the multipart message (prompt, image buffer) and decodes it."""
        try:
            parts = self.socket.recv_multipart()
            if len(parts) == 2:
                prompt_bytes, buffer = parts
                prompt = prompt_bytes.decode('utf-8')
                nparr = np.frombuffer(buffer, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                return prompt, frame
        except Exception as e:
            logger.error(f"Error receiving frame from ZMQ: {e}")
            
        return "", None

    def send_response(self, response: Dict[str, Any]):
        """Sends the JSON response back to the client."""
        self.socket.send_json(response)

    def close(self):
        self.socket.close()
        self.context.term()
        logger.info("ZMQ Server stopped.")
