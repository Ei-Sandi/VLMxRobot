# Server-VLM

ZeroMQ server for receiving camera frames from Raspberry Pi client and processing them with Vision Language Models.

## Overview

This server receives JPEG-encoded images from the Raspberry Pi client via ZeroMQ, displays them in a video stream window, and sends back robot control commands.

## Requirements

- Python 3.7+
- Network connectivity with the Raspberry Pi client

## Installation

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure the server settings in `config.py` if needed (default port is 5555).

## Usage

Start the server to listen for incoming frames:
```bash
python ZeroMQserver.py
```

The server will:
- Listen on port 5555 (configurable in `config.py`)
- Display incoming frames in a window titled "PiCar-X VLM Stream"
- Send control commands back to the client

**Controls:**
- Press `q` in the video window to stop the server
- Press `Ctrl+C` in the terminal to shut down

## Configuration

Edit `config.py` to customize:
- `PORT`: Server listening port (default: 5555)
- `DEFAULT_COMMAND`: Command to send when frame is received successfully
- `STOP_COMMAND`: Command to send when frame processing fails

## Files

- `ZeroMQserver.py` - Main server application for receiving and displaying frames
- `config.py` - Server configuration (port, default commands)

## Network Setup

To connect from Raspberry Pi:
1. Find your laptop's IP address:
   - Linux/Mac: `ip addr` or `ifconfig`
   - Windows: `ipconfig`
2. Set this IP in the client's `.env` file as `SERVER_IP`
3. Ensure firewall allows connections on port 5555

