"""
backend/pose/pose_extractor.py

This module handles pose estimation using MediaPipe Pose.
It extracts landmarks from the input frame given by the webcam.
"""

import cv2
import mediapipe as mp

class PoseExtractor:
    def __init__(self):
        """
        Initialize MediaPipe Pose.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        """
        Process the image frame and extract pose landmarks.
        
        Args:
            frame: Input image frame (BGR format).
            
        Returns:
            landmarks: Raw MediaPipe pose landmarks (33 points) or None if not found.
        """
        # Convert frame to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.pose.process(frame_rgb)
        
        if results.pose_landmarks:
            return results.pose_landmarks
            
        return None

