# Client-Pi

Raspberry Pi client for capturing and streaming camera frames to the VLM server via ZeroMQ.

## Overview

This client captures images from a Raspberry Pi camera, encodes them as JPEG, and sends them to a remote server for Vision Language Model (VLM) processing. The server responds with commands based on the image analysis.

## Requirements

- Raspberry Pi with camera module
- Python 3.7+
- Active network connection to the VLM server

## Installation

1. Install system dependencies (Raspberry Pi):
```bash
sudo apt-get update
sudo apt-get install python3-opencv python3-picamera2
```

2. Create a virtual environment and install Python dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure the connection:
```bash
cp .env-example .env
```
Edit `.env` and set your server's IP address:
```
SERVER_IP=<YOUR_SERVER_IP_ADDRESS>
SERVER_PORT=5555
```

## Usage

Run the client to start capturing and sending frames:
```bash
python ZeroMQclient.py
```

Press `Ctrl+C` to stop the client.

## Configuration

- **Image resolution**: Default is 640x480 (configurable in `ZeroMQclient.py`)
- **JPEG quality**: Default is 70 (configurable in `ZeroMQclient.py`)
- **Server connection**: Set via `.env` file

## Files

- `Camera.py` - Camera interface using Picamera2
- `ZeroMQclient.py` - Main client application for ZeroMQ communication
- `.env-example` - Example environment configuration
