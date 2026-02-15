# Server-VLM

ZeroMQ server for receiving camera frames from Raspberry Pi client and processing them with Vision Language Models (Gemini or Ollama).

## Overview

This server receives JPEG-encoded images from the Raspberry Pi client via ZeroMQ, processes them with a Vision Language Model, displays the frames in a video stream window, and sends back robot control commands.

## Features

- **Multiple VLM Providers**: Choose between Google Gemini or local Ollama
- **Factory Pattern**: Easy switching between providers via configuration
- **Modular Architecture**: Abstracted VLM interface with provider-specific implementations
- **Test Scripts**: Standalone scripts to test each provider with static images

## Requirements

- Python 3.8+
- Network connectivity with the Raspberry Pi client
- For Gemini: Google API key
- For Ollama: Local Ollama installation

## Installation

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment variables by creating a `.env` file:
```bash
cp .env-example .env
```

3. Configure your `.env` file:
```env
# Optional: Override VLM provider (default is in config.py)
# VLM_PROVIDER=gemini

# Required for Gemini provider
GOOGLE_API_KEY=your_key_here
```

4. Configure server settings in `config.py`:
   - `VLM_PROVIDER`: Default provider ("ollama" or "gemini")
   - `PORT`: Server listening port (default: 5555)
   - `SYSTEM_PROMPT`: Instructions for the VLM
   - Model names and URLs

## Usage

### Start the Server

```bash
python server.py
```

The server will:
- Use the VLM provider specified in config or .env
- Listen on port 5555 (configurable)
- Display incoming frames in "PiCar-X VLM Stream" window
- Analyze frames with the VLM
- Send control commands back to the client

**Controls:**
- Press `q` in the video window to stop the server
- Press `Ctrl+C` in the terminal to shut down

### Test VLM Providers

Test each provider with a static image without needing the client:

```bash
# Test Ollama
python test/test_ollama.py path/to/image.jpg

# Test Gemini
python test/test_gemini.py path/to/image.jpg
```

## Project Structure

```
server-VLM/
├── server.py              # Main server application
├── config.py              # Configuration (ports, models, prompts)
├── vlm.py                 # Abstract VLM base class with factory
├── gemini_client.py       # Gemini VLM implementation
├── ollama_client.py       # Ollama VLM implementation
├── .env-example           # Environment variables template
├── requirements.txt       # Python dependencies
├── test/
│   ├── test_gemini.py    # Test script for Gemini
│   └── test_ollama.py    # Test script for Ollama
└── README.md
```

## Architecture

The server uses an abstract `VLM` base class that both `GeminiClient` and `OllamaClient` inherit from. This allows:
- **Easy provider switching**: Change `VLM_PROVIDER` in config or .env
- **Consistent interface**: Both providers implement `analyze_frame()`
- **Factory pattern**: `VLM.create()` instantiates the correct provider

## Configuration

### config.py
- `VLM_PROVIDER`: Default VLM provider ("ollama" or "gemini")
- `PORT`: Server listening port
- `GEMINI_MODEL_NAME`: Gemini model identifier
- `OLLAMA_MODEL_NAME`: Ollama model name
- `OLLAMA_URL`: Ollama API endpoint
- `SYSTEM_PROMPT`: Instructions for the VLM
- `DEFAULT_COMMAND`: Command to send on successful frame processing
- `STOP_COMMAND`: Command to send on error

### .env (optional overrides)
- `VLM_PROVIDER`: Override the default provider
- `GOOGLE_API_KEY`: Required for Gemini

## Network Setup

To connect from Raspberry Pi:
1. Find your laptop's IP address:
   - Linux/Mac: `ip addr` or `ifconfig`
   - Windows: `ipconfig`
2. Set this IP in the client's `.env` file as `SERVER_IP`
3. Ensure firewall allows connections on port 5555

## Switching VLM Providers

### Method 1: Edit config.py (default)
```python
VLM_PROVIDER = "gemini"  # or "ollama"
```

### Method 2: Override with .env
```env
VLM_PROVIDER=gemini
```

The server will automatically use the specified provider on startup.

