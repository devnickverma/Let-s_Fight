# LetsFight

An AIML-first real-time boxing action analysis system.

## Project Overview
LetsFight analyzes boxing movements in real-time using computer vision and renders a 3D visualization of the fighter's skeleton in the browser. It is designed to be a lightweight, tech-focused implementation avoiding heavy game engines.

## Tech Stack
- **Backend:** Python (MediaPipe, OpenCV, WebSockets)
- **Frontend:** Three.js (WebGL)

## MVP Goals
- Real-time skeleton tracking (MediaPipe Pose).
- Basic action recognition (Rule-based).
- Low-latency data streaming via WebSockets.
- Browser-based 3D visualization.

## Setup Instructions (Scaffolding Only)
1. **Backend:**
   - Install dependencies (TBD: `mediapipe`, `opencv-python`, `websockets`).
   - Run `python backend/main.py`.

2. **Frontend:**
   - Serve the `frontend/` directory (e.g., using VS Code Live Server or `python -m http.server`).
   - Open `index.html` in a browser.

## Directory Structure
- `backend/`: Core logic and server.
- `frontend/`: 3D visualization.
- `docs/`: Documentation.

## Status
- [x] Scaffolding complete.
- [ ] Core logic implementation pending.
