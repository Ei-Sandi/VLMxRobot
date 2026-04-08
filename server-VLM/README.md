# Server-VLM

The cognitive reasoning server for the project. It receives camera frames from the Raspberry Pi client via ZeroMQ and processes them with Vision Language Models (like Google Gemini or Ollama) using a unified OpenAI-compatible interface to generate actionable robotic commands.

## Overview

This server acts as the "brain" of the robot. It continuously receives JPEG-encoded images, processes them contextually using a VLM, and immediately responds with a structured JSON payload dictating the robot's next physical action (e.g., move, look around, or speak). 

## Features

- **Unified VLM Interface**: Uses the `openai` Python library to connect to any compatible provider natively.
- **ZeroMQ Streaming**: Employs REQ/REP patterns for robust, low-latency image streaming and command response.
- **Stateful Memory**: Maintains recent text and image history for context, while pruning older payloads to respect context windows.
- **Safe Command Parsing**: Utilizes Pydantic schema validation to ensure the VLM constructs strict, physically safe actions.
- **Configurable Backend**: Switch seamlessly between cloud (Gemini) and local (Ollama) inference models via environment variables.

## Requirements

- Python 3.8+
- Network connectivity with the Raspberry Pi (must be on the same network or routeable)
- **For Cloud Inference**: Valid API key (e.g., Google Gemini)
- **For Local Inference**: Ollama installed and running (default port 11434)

## Installation

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment variables by copying the template:
```bash
cp .env-example .env
```

3. Configure your `.env` for your preferred provider:

   **Option A: Gemini (Cloud - Recommended for speed)**
   ```env
   VLM_API_KEY="your-google-api-key-here"
   VLM_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   VLM_MODEL_NAME="gemini-1.5-flash"
   ```

   **Option B: Ollama (Local)**
   ```env
   VLM_API_KEY="ollama"
   VLM_BASE_URL="http://localhost:11434/v1"
   VLM_MODEL_NAME="llava:7b"
   ```

## Usage

### Start the Server

```bash
python server.py
```

The runtime routine will:
- Initialize the VLM client.
- Bind the ZeroMQ socket on port `5555` (default).
- Wait for incoming frames from the PiCar-X.
- Output routing logic and VLM thought-processes to the terminal console.

**Controls**:
- Press `Ctrl+C` in the terminal to force shutdown.

### Manual VLM Testing

You can evaluate the prompt behavior and VLM capability without booting the physical robot using the provided test scripts:

```bash
# Basic test using default prompt behavior
python scripts/test_vlm.py path/to/sample_image.jpg

# Custom injection prompt
python scripts/test_vlm.py path/to/sample_image.jpg "Do you see a blue cup?"
```

## System Architecture

```text
server-VLM/
├── server.py              # Main loop (ZMQ + Memory + Model processing)
├── config.py              # Configuration and environment variables
├── core/
│   ├── network/zmq_handler.py    # ZeroMQ communication
│   ├── memory/context.py         # Conversation history & image pruning
│   ├── models/vlm_wrapper.py     # VLM interface wrapper
│   └── actions/parser.py         # JSON schema validation & fallback
├── prompts/               # System behaviors and task templates
└── scripts/               # Diagnostic and testing utilities
```

## Action Schema

The VLM is strictly instructed (via `prompts/system_prompt.txt`) to output JSON controlling three independent subsystems:
- **Movement**: `forward`, `backward`, `stop`, `turn_left`, `turn_right`
- **Camera (Head)**: `look_left`, `look_right`, `look_up`, `look_down`, `reset_camera`
- **Speech**: `speak`, `ask`

All returned payloads are validated through `parser.py` before transmission back to the client.
