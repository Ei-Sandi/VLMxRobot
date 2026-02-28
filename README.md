# Goal-Oriented Robotic Planning and Navigation with Vision Language Models

A robotic navigation framework that integrates **Vision Language Models (VLMs)** for high-level reasoning, object detection, and path planning. The system enables a **Raspberry Pi-based robot (PiCar-X)** to understand its environment visually and execute text-based natural language instructions (e.g., "Find the yellow rubber duck") using models like Google Gemini or Ollama.

## Key Features

- **Brain-Client Architecture**:
  - **Client (PiCar-X)**: Lightweight Python agent handling motor control, camera streaming, and sensor readings.
  - **Server (Laptop/PC)**: High-performance ZeroMQ server running state-of-the-art VLMs for decision making.

- **Unified VLM backend**: 
  - Supports **Google Gemini 3 Pro** (Cloud) for high-speed, accurate reasoning.
  - Supports **Ollama** (Local) for offline, privacy-focused inference (e.g., LLaVA).
  - Uses OpenAI-compatible API format for easy model swapping.

- **Rich Interaction**:
  - **Movement**: Navigate with obstacle avoidance and dynamic steering.
  - **Vision**: Scan the room by moving the camera head (independent of chassis).
  - **Speech**: Speak to users or ask questions using Text-to-Speech (TTS). (Instructions are currently typed text).

## Hardware Stack

- **Robot**: SunFounder PiCar-X (Raspberry Pi 4 Model B)
- **Host Machine**: Any PC/Laptop (Windows/Linux/Mac) capable of running Python 3.8+
- **Camera**: Standard Pi Camera Module or USB Webcam

## Project Structure

```bash
VLMxRobot/
├── client-pi/          # Code running on the Robot (Raspberry Pi)
│   ├── actions.py      # Motor & Servo control logic
│   ├── camera.py       # Camera streaming
│   ├── client.py       # Main ZMQ client loop
│   └── ...
├── server-VLM/         # Code running on the Host (Brain)
│   ├── server.py       # Main ZMQ server & VLM handler
│   ├── vlm.py          # Unified VLM interface
│   ├── config.py       # System prompts & configurations
│   └── ...
└── utils/              # Shared utilities (if any)
```

## Quick Start

### 1. Server Setup (The Brain)
Run this on your powerful laptop/PC.

```bash
cd server-VLM
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure API Keys
cp .env-example .env
# Edit .env to add your GOOGLE_API_KEY or configure Ollama

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
# Edit .env and set SERVER_IP to your laptop\s IP address

# Start the Robot
python client.py
```

## How It Works

1. **Capture**: The robot captures a simplified image of its view.
2. **Transmit**: The image is sent over Wi-Fi (ZMQ) to the server.
3. **Analyze**: The VLM server analyzes the image against the user\s instruction (e.g., "Find the yellow rubber duck").
4. **Plan**: The VLM generates a structured JSON command (e.g., `{ "action": "look_left", "angle": 30 }`).
5. **Execute**: The robot receives the JSON and executes the physical movement.
6. **Loop**: The cycle repeats until the task is marked "completed".

## 📚 Documentation

- [Server Documentation](server-VLM/README.md)
- [Client Documentation](client-pi/README.md)
