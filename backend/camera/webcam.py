"""
backend/camera/webcam.py

This module is responsible for handling webcam input using OpenCV.
It should read frames from the default camera and provide them for processing.
"""

import cv2

class Webcam:
    def __init__(self, device_id=0):
        """
        Initialize the webcam.
        
        Args:
            device_id (int): Camera device ID (default is 0).
        """
        self.cap = cv2.VideoCapture(device_id)
        if not self.cap.isOpened():
            print("Error: Could not open video device.")
            return

    def read_frame(self):
        """
        Capture a single frame from the webcam.
        
        Returns:
            frame: A numpy array representing the image frame, or None if failed.
        """
        ret, frame = self.cap.read()
        if not ret:
            # print("Error: Failed to capture frame.")
            return None
        return frame

    def release(self):
        """
        Release the camera resource.
        """
        if self.cap.isOpened():
            self.cap.release()

