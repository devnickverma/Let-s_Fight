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

def main():
    """
    Main function to run the application.
    """
    print("Starting LetsFight Module Test: Pose Extraction...")

    # Initialize Webcam and PoseExtractor
    webcam = Webcam()
    pose_extractor = PoseExtractor()

    print("Press 'q' to exit.")

    try:
        while True:
            # Capture frame
            frame = webcam.read_frame()

            if frame is None:
                # print("No frame captured.")
                continue

            # Process frame for pose
            landmarks = pose_extractor.process_frame(frame)
            
            if landmarks:
                print(f"Detected {len(landmarks.landmark)} landmarks")
            else:
                print("No pose detected")

            # Display frame
            cv2.imshow('LetsFight - Pose Test (Press q to exit)', frame)

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
