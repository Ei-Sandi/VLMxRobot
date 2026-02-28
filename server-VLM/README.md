# Server-VLM

ZeroMQ server for receiving camera frames from Raspberry Pi client and processing them with Vision Language Models (Gemini or Ollama) using a unified OpenAI-compatible interface.

## Overview

This server acts as the brain of the robot. It receives JPEG-encoded images from the Raspberry Pi client via ZeroMQ, processes them with a Vision Language Model (VLM), displays the frames in a video stream window, and sends back robot control commands (movement, camera, speech).

## Features

- **Unified VLM Interface**: Uses the `openai` python library to connect to any OpenAI-compatible VLM provider (Ollama, Gemini, etc.).
- **ZeroMQ Streaming**: Low-latency image streaming and command response.
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

   **Option A: Gemini (Default)**
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

The server will:
- Initialize the VLM client based on your `.env` configuration.
- Listen on port 5555 (default).
- Display incoming frames in "PiCar-X VLM Stream" window.
- Analyze frames and send JSON commands back to the robot.

**Controls:**
- Press `q` in the video window to stop the server.
- Press `Ctrl+C` in the terminal to force shut down.

### Test VLM Manually

You can test the VLM\s response to a static image without running the full robot loop:

```bash
# Basic usage (defaults to generic prompt)
./venv/bin/python3 test/test_vlm.py path/to/image.jpg

# Custom prompt
./venv/bin/python3 test/test_vlm.py path/to/image.jpg "Is there a clear path forward?"
```

## Project Structure

```
server-VLM/
├── server.py              # Main ZeroMQ server application
├── config.py              # Configuration loading and System Prompt
├── vlm.py                 # Unified VLM class (OpenAI wrapper)
├── .env-example           # Environment variables template
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── test/
    └── test_vlm.py        # Manual VLM testing script
```

## System Prompt & Actions

The behavior of the robot is defined in `config.py` under `SYSTEM_PROMPT`. The VLM is instructed to output JSON commands for:
- **Movement**: `forward`, `backward`, `stop`.
- **Camera**: `look_left`, `look_right`, `look_up`, `look_down`.
- **Speech**: `speak`, `ask`.

## Network Setup

To connect from Raspberry Pi:
1. Find your laptops IP address:
   - Linux/Mac: `ip addr` or `ifconfig`
   - Windows: `ipconfig`
2. Set this IP in the **Clients** `.env` file as `SERVER_IP`.
3. Ensure your firewall allows inbound connections on port 5555.
