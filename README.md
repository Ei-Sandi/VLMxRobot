## Goal-Oriented Robotic Planning and Navigation in Indoor Environments Using Local Vision Language Models

This repository contains the source code and documentation for a final year BSc Computer Science dissertation project at Coventry University. The project explores **Goal-Oriented Robotic Planning** by integrating Vision Language Models (VLMs) for high-level reasoning and navigation. The system is designed to navigate indoor environments using real-time obstacle avoidance and strategic planning, leveraging both local VLMs (via Ollama) and cloud-based models (Gemini) for comparative analysis and robust decision-making.

### Project Overview

The system utilizes a **SunFounder PiCar-X** as the physical agent, controlled by a Raspberry Pi 4. To overcome the computational limitations of the Pi, high-level visual processing and strategic logic are offloaded to a local inference server (laptop). The server processes panoramic visual data and generates actionable navigation commands, which are sent back to the robot.

#### Key Features

- **Hybrid VLM Integration**: Supports switching between local execution (Ollama) and cloud-based inference (Google Gemini) for flexible performance trade-offs.
- **Panoramic Environmental Understanding**: The robot captures and stitches multiple images to form a comprehensive view of its surroundings before making decisions.
- **Client-Server Architecture**: Uses ZeroMQ (ZMQ) for low-latency communication between the Raspberry Pi (Client) and the Inference Server.
- **Goal-Oriented Navigation**: The VLM processes visual context to plan paths towards specific goals while avoiding obstacles.
- **Hardware Abstraction**: modular design separates low-level robot control (motors, servos) from high-level logic.

#### Hardware Stack

**Robot Agent:**
- **Chassis**: SunFounder PiCar-X
- **Controller**: Raspberry Pi 4 Model B (4GB RAM)
- **Hat**: Robot HAT v4
- **Camera**: Standard Pi Camera Module
- **OS**: Raspberry Pi OS (Legacy)

**Inference Server:**
- **OS**: Ubuntu 22.04 LTS (or similar)
- **CPU**: AMD Ryzen 3 (or equivalent)
- **GPU**: AMD Radeon Graphics (Optional, for local inference acceleration)
- **VLM Backend**: Ollama (Local) / Google Gemini API (Cloud)

### Software Architecture

The project consists of two main components:
1.  **Client (Raspberry Pi)**: Handles hardware interfacing, image capture, panoramic stitching, and executing movement commands.
2.  **Server (Laptop/PC)**: Hosts the VLM, processes incoming image data, and generates navigation instructions.

Communication is handled via TCP sockets (ZeroMQ).

### Requirements

See `client-pi/requirements.txt` and `server-VLM/requirements.txt` for specific Python dependencies.

Key Libraries:
- `opencv-python`: Image processing and stitching.
- `pyzmq`: Network communication.
- `ollama` / `google-genai`: Vision Language Model interfaces.
- `picarx`: SunFounder robot control library.