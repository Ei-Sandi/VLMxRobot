# Server-VLM

ZeroMQ server for receiving camera frames from Raspberry Pi client and processing them with Vision Language Models (Gemini or Ollama) using a unified OpenAI-compatible interface.

## Overview

This server acts as the brain of the robot. It receives JPEG-encoded images from the Raspberry Pi client via ZeroMQ, processes them with a Vision Language Model (VLM), displays the frames in a video stream window, and sends back robot control commands (movement, camera, speech).

## Features

- **Unified VLM Interface**: Uses the `openai` python library to connect to any OpenAI-compatible VLM provider (Ollama, Gemini, etc.).
- **ZeroMQ Streaming**: Low-latency image streaming and command response.
- **Conversation Memory**: Keeps recent text/image history while pruning old image payloads.
- **Safe Command Parsing**: Pydantic schema validation with emergency fallback stop.
- **Configurable Control**: Easy switching between models via environment variables.
- **Manual Testing**: Script to test VLM responses with static images.

## Requirements

- Python 3.8+
- Network connectivity with the Raspberry Pi client
- For Gemini: Google API key
- For Ollama: Local Ollama installation running (usually on port 11434)

## Installation

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment variables by copying the example:
```bash
cp .env-example .env
```

3. Configure your `.env` file for your chosen provider:

   **Option A: Gemini (Default, cloud)**
   ```env
   VLM_API_KEY="your-google-api-key-here"
   VLM_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   VLM_MODEL_NAME="gemini-1.5-flash"
   ```

   **Option B: Ollama (local)**
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

The server will:
- Initialize the VLM client based on your `.env` configuration.
- Listen on port 5555 (default).
- Display incoming frames in "PiCar-X VLM Stream" window.
- Analyze frames and send JSON commands back to the robot.

**Controls:**
- Press `q` in the video window to stop the server.
- Press `Ctrl+C` in the terminal to force shut down.

### Test VLM Manually

You can test the VLM response to a static image without running the full robot loop:

```bash
# Basic usage (defaults to generic prompt)
./venv/bin/python3 scripts/test_vlm.py path/to/image.jpg

# Custom prompt
./venv/bin/python3 scripts/test_vlm.py path/to/image.jpg "Is there a clear path forward?"
```

## Project Structure

```
server-VLM/
├── server.py              # Main runtime loop (network + memory + model)
├── config.py              # Env config + loads prompts/system_prompt.txt
├── .env-example           # Environment variables template
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── core/
│   ├── network/zmq_handler.py      # ZeroMQ REQ/REP receive/send abstraction
│   ├── memory/context.py           # Message history + image pruning
│   ├── models/vlm_wrapper.py       # OpenAI-compatible VLM wrapper
│   └── actions/parser.py           # Strict JSON schema parser/fallback
├── prompts/
│   ├── system_prompt.txt           # Canonical robot behavior prompt
│   └── task_templates.json         # Task templates/few-shot references (actively injected)
└── scripts/
   ├── test_vlm.py                 # Manual static-image VLM test
   └── simple_image_server.py      # Debug REQ/REP image receiver
```

## System Prompt & Actions

The behavior prompt is maintained in `prompts/system_prompt.txt` and loaded by `config.py` into `SYSTEM_PROMPT` at startup. The VLM is instructed to output JSON commands for:
- **Movement**: `forward`, `backward`, `stop`.
- **Camera**: `look_left`, `look_right`, `look_up`, `look_down`.
- **Speech**: `speak`, `ask`.

## Runtime Workflow

1. Client sends multipart ZeroMQ message: `(prompt, jpg_frame_bytes)`.
2. `server.py` receives frame and appends user turn into context memory.
3. `config.py` selects task guidance from `task_templates.json` based on prompt keywords.
4. `context.py` builds model messages with base system prompt + selected task guidance + conversation history.
5. `vlm_wrapper.py` calls the configured OpenAI-compatible endpoint.
6. `parser.py` validates model JSON into strict action schema.
7. Safe parsed command is returned to the robot over ZeroMQ.

## Network Setup

To connect from Raspberry Pi:
1. Find your laptops IP address:
   - Linux/Mac: `ip addr` or `ifconfig`
   - Windows: `ipconfig`
2. Set this IP in the **Clients** `.env` file as `SERVER_IP`.
3. Ensure your firewall allows inbound connections on port 5555.
