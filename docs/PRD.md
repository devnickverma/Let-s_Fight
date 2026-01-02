# Product Requirements Document (PRD)

## Project Name: LetsFight

### 1. Overview
LetsFight is an AIML-first real-time boxing action analysis system. It uses computer vision to detect boxing moves and provides real-time feedback via a 3D interface.

### 2. Objectives
- Real-time pose estimation using MediaPipe.
- Action classification for boxing moves (Jab, Cross, Hook, Uppercut).
- Low-latency streaming of pose data.
- 3D visualization of the fighter's skeleton in the browser.

### 3. MVP Features
- [ ] Webcam input support.
- [ ] Basic pose extraction (33 landmarks).
- [ ] Simple rule-based action classifier.
- [ ] WebSocket server-client communication.
- [ ] 3D skeleton rendering using Three.js.

### 4. Constraints
- No Unity/Unreal/Godot.
- Browser-based frontend.
- Python backend.
