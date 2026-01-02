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

def main():
    """
    Main function to run the application.
    """
    print("Starting LetsFight Module Test: Normalization & Smoothing...")

    # Initialize Modules
    webcam = Webcam()
    pose_extractor = PoseExtractor()
    pose_processor = PoseProcessor(alpha=0.5)

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
                
                # Print debug info
                if processed_landmarks:
                    nose = processed_landmarks[0] # Landmark 0 is Nose
                    print(f"Smoothing applied. Nose: x={nose['x']:.2f}, y={nose['y']:.2f}, z={nose['z']:.2f}")
            else:
                print("No pose detected")

            # Display frame (optional, for visual feedback that loop is running)
            cv2.imshow('LetsFight - Phase 3 Test', frame)

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
