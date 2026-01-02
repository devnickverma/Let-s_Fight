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

def main():
    """
    Main function to run the application.
    """
    print("Starting LetsFight Feature Extraction Test...")

    # Initialize Modules
    webcam = Webcam()
    pose_extractor = PoseExtractor()
    pose_processor = PoseProcessor(alpha=0.5)
    feature_extractor = FeatureExtractor()

    print("Press 'q' to exit.")

    try:
        while True:
            # Capture frame
            frame = webcam.read_frame()

            if frame is None:
                # print("No frame captured.")
                continue

            # Process frame for pose
            raw_landmarks = pose_extractor.process_frame(frame)
            
            if raw_landmarks:
                # Normalize and Smooth
                processed_landmarks = pose_processor.process(raw_landmarks.landmark)
                
                # Extract Features
                if processed_landmarks:
                    features = feature_extractor.extract(processed_landmarks)
                    
                    # Print Summary
                    # L_Elbow Angle, L_Wrist Vel | R_Elbow Angle, R_Wrist Vel
                    print(f"L: {features['left_elbow_angle']:.0f} deg, Vel: {features['left_wrist_velocity']:.2f} | "
                          f"R: {features['right_elbow_angle']:.0f} deg, Vel: {features['right_wrist_velocity']:.2f}")

            else:
                print("No pose detected")

            # Display frame (optional, for visual feedback that loop is running)
            cv2.imshow('LetsFight - Phase 4 Test', frame)

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
