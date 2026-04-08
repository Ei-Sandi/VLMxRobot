# Client-Pi

The Raspberry Pi client module for the project. It is responsible for capturing and streaming camera frames to the VLM server via ZeroMQ, and executing the physical robotic commands returned by the server.

## Overview

This client acts as the physical embodiment of the VLM. It captures images from a Raspberry Pi camera, encodes them as JPEG, and sends them to a remote server for Vision Language Model (VLM) processing. The server responds with actionable commands based on the image analysis, which this client then translates into motor, servo, and speaker actions.

## Hardware Requirements

- Raspberry Pi 4 Model B (or compatible)
- SunFounder PiCar-X Kit
- Raspberry Pi Camera Module (or compatible webcam)
- Active Wi-Fi connection to the VLM server

## Installation

1. Install system dependencies (Raspberry Pi OS):
```bash
sudo apt-get update
sudo apt-get install python3-opencv python3-libcamera
```

2. Create a virtual environment and install Python dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Install SunFounder hardware dependencies (robot-hat and picar-x):
```bash
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat && sudo python3 setup.py install && cd ..

git clone https://github.com/sunfounder/picar-x.git
cd picar-x && sudo python3 setup.py install && cd ..
```

4. Configure the connection to the server:
```bash
cp .env-example .env
```
Edit `.env` and set your host server's IP address:
```env
SERVER_IP=<YOUR_SERVER_IP_ADDRESS>
SERVER_PORT=5555
```

## Running the Client

To start the client, use the following command:

```bash
python client.py
```
Press `Ctrl+C` to gracefully stop the client and reset the servos.

## Configuration

- **Image Resolution**: Default is typically 640x480 (configurable in `client.py` / `camera.py`)
- **JPEG Quality**: Optimized for low latency over Wi-Fi.
- **Server Connection**: Managed via the `.env` file.

## Client File Structure

```text
client-pi/
├── actions.py       # Translation layer for PySloth motor movements
├── camera.py        # Interface for hardware accelerated camera capture
├── client.py        # Main loop for ZMQ communication and dispatching
├── speaker.py       # Handles Text-to-Speech (TTS) output
├── executor.py      # Execution logic mapping
├── requirements.txt # Python package dependencies
└── ...
```

## Troubleshooting
- **Connection Issues**: Ensure the Raspberry Pi can ping the host machine and that firewall rules are not interfering.
- **Camera Issues**: Verify the camera is properly connected and that the Pi camera module is enabled in `raspi-config`.
