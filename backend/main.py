"""
backend/main.py

Main entry point for the LetsFight backend.
Initializes modules (Camera, Pose, Action, Streaming) and runs the main loop.
"""

import cv2
import sys
import os

# Add the parent directory to sys.path to enable absolute imports from 'backend'
# This handles the case where main.py is run directly as a script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from backend.camera.webcam import Webcam
from backend.pose.pose_extractor import PoseExtractor
from backend.utils.smoothing import PoseProcessor
from backend.action.feature_extractor import FeatureExtractor
from backend.action.action_classifier import ActionClassifier
import cv2
import mediapipe as mp

def main():
    """
    Main function to run the application.
    """
    print("Starting LetsFight Main Pipeline (MVP)...")

    # Initialize Modules
    webcam = Webcam()
    pose_extractor = PoseExtractor()
    pose_processor = PoseProcessor(alpha=0.5)
    feature_extractor = FeatureExtractor()
    action_classifier = ActionClassifier()
    
    # MediaPipe Drawing Support
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    print("Pipeline Ready. Press 'q' to exit.")

    try:
        while True:
            # Capture frame
            frame = webcam.read_frame()

            if frame is None:
                continue
                
            h, w, c = frame.shape

            # Process frame for pose
            raw_landmarks = pose_extractor.process_frame(frame)
            
            if raw_landmarks:
                # 1. Visualize Raw Skeleton (Debugging)
                # We use raw landmarks for drawing to match the video frame 1:1
                mp_drawing.draw_landmarks(
                    frame, 
                    raw_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                # 2. Process for Logic
                processed_landmarks = pose_processor.process(raw_landmarks.landmark)
                
                if processed_landmarks:
                    # Extract Features
                    features = feature_extractor.extract(processed_landmarks)
                    
                    # Classify Action
                    result = action_classifier.classify(features)
                    
                    action = result['action']
                    conf = result['confidence']
                    
                    # 3. Overlay Action Label
                    color = (0, 255, 0) # Green for Idle
                    if action == "JAB": color = (0, 0, 255) # Red
                    elif action == "GUARD": color = (255, 0, 0) # Blue
                    
                    cv2.putText(frame, f"Action: {action} ({conf:.2f})", (20, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                                
                    # Debug Info
                    cv2.putText(frame, f"Vel: L={features['left_wrist_velocity']:.2f} R={features['right_wrist_velocity']:.2f}", 
                                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                    print(f"Action: {action:<8} | Conf: {conf:.2f}")

            else:
                cv2.putText(frame, "No Pose Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Display frame
            cv2.imshow('LetsFight - MVP Loop', frame)

            # Exit on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Cleanup
        webcam.release()
        cv2.destroyAllWindows()
        print("Exiting cleanly.")

if __name__ == "__main__":
    main()
