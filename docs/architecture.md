# Architecture Overview

## Technology Stack
- **Backend:** Python
- **Pose Estimation:** MediaPipe Pose
- **Action Analysis:** Rule-based Classifier (MVP)
- **Streaming:** WebSockets (Python `websockets` lib)
- **Frontend:** Three.js (JavaScript)

## Data Flow
1. **Camera Input:** `webcam.py` captures frames from the user's camera.
2. **Pose Extraction:** `pose_extractor.py` processes frames using MediaPipe to get (x, y, z) landmarks.
3. **Action Analysis:** `action_classifier.py` analyzes the landmarks to detect actions (e.g., "Jab").
4. **Streaming:** `websocket_server.py` broadcasts the landmark data and action result to connected clients.
5. **Visualization:** 
    - `websocket_client.js` receives the data.
    - `skeleton.js` updates the 3D local model.
    - `scene.js` renders the scene.

## Directory Structure
- `backend/`: Python code for processing and server.
- `frontend/`: HTML/JS code for client-side rendering.
- `docs/`: Project documentation.
