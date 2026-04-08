# Goal-Oriented Robotic Planning and Navigation with Vision Language Models

A robotic navigation framework that integrates **Vision Language Models (VLMs)** for high-level reasoning, object detection, and path planning. The system enables a Raspberry Pi-based robot (SunFounder PiCar-X) to understand its environment visually and execute natural language instructions (e.g., "Find the yellow rubber duck") using models like Google Gemini or local open-weight models via Ollama.

## Key Features

- **Brain-Client Architecture**:
  - **Client (PiCar-X)**: Lightweight Python agent handling motor control, camera streaming, and sensor readings.
  - **Server (Brain)**: High-performance ZeroMQ server running state-of-the-art VLMs for cognitive decision making.
- **Unified VLM Backend**: 
  - Supports **Google Gemini 1.5/3 Pro** (Cloud) for high-speed, accurate reasoning.
  - Supports **Ollama** (Local) for offline, privacy-focused inference (e.g., LLaVA).
  - Uses an OpenAI-compatible API format for easy model swapping.
- **Rich Interaction**:
  - **Movement**: Navigate with obstacle avoidance and dynamic steering.
  - **Vision**: Scan the room by moving the camera head (independent of the chassis).
  - **Speech**: Speak to users or ask questions using Text-to-Speech (TTS).

## Hardware Stack

- **Robot**: SunFounder PiCar-X (Raspberry Pi 4 Model B)
- **Host Machine**: Any PC/Laptop (Windows/Linux/Mac) capable of running Python 3.8+
- **Camera**: Standard Pi Camera Module or USB Webcam

## Project Structure

```text
VLMxRobot/
├── client-pi/          # Code running on the Robot (Raspberry Pi)
│   ├── actions.py      # Motor & Servo control logic
│   ├── camera.py       # Camera streaming
│   ├── client.py       # Main ZMQ client loop
│   └── ...
├── server-VLM/         # Code running on the Host (Brain)
│   ├── server.py       # Main ZMQ server & VLM handler
│   ├── config.py       # System configurations and prompt loading
│   ├── core/           # Core modules (network, memory, models, actions)
│   └── ...
└── README.md           # This file
```

## Quick Start

### 1. Server Setup (The Brain)
Run this on your host machine (PC/Laptop).

```bash
cd server-VLM
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure API Keys
cp .env-example .env
# Edit .env to add your VLM_API_KEY (e.g., Google API Key) or configure Ollama

# Start the Server
python server.py
```

### 2. Client Setup (The Robot)
Run this on the Raspberry Pi.

```bash
cd client-pi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Connection
cp .env-example .env
# Edit .env and set SERVER_IP to your host machine's IP address

# Start the Robot
python client.py
```

## How It Works

1. **Capture**: The robot captures an image of its current view.
2. **Transmit**: The image is sent over Wi-Fi via ZeroMQ to the server.
3. **Analyze**: The VLM server analyzes the image against the user's instruction.
4. **Plan**: The VLM generates a structured JSON command (e.g., `{ "action": "look_left", "angle": 30 }`).
5. **Execute**: The robot receives the JSON, parses it, and executes the physical movement.
6. **Loop**: The cycle repeats until the task is successfully completed.

## 📚 Documentation

For more detailed information, check the specific module readmes:
- [Server Documentation](server-VLM/README.md)
- [Client Documentation](client-pi/README.md)
