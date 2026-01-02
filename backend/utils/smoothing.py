"""
backend/utils/smoothing.py

This module contains the PoseProcessor class which handles:
1. Landmark Normalization: Invariant to scale and position.
2. Temporal Smoothing: Exponential Moving Average (EMA) to reduce jitter.
"""

import math

class PoseProcessor:
    def __init__(self, alpha=0.5):
        """
        Initialize the PoseProcessor.

        Args:
            alpha (float): Smoothing factor (0 < alpha <= 1). 
                           Lower = smoother but more lag. Higher = more responsive.
        """
        self.alpha = alpha
        self.previous_landmarks = None

        # MediaPipe Landmark Indices
        self.LEFT_SHOULDER = 11
        self.RIGHT_SHOULDER = 12
        self.LEFT_HIP = 23
        self.RIGHT_HIP = 24

    def normalize(self, landmarks):
        """
        Normalize landmarks to be invariant to scale and translation.
        Origin = Hip Center.
        Scale = 1.0 / Torso Length.

        Args:
            landmarks: List of landmark objects (from MediaPipe or processed dicts).
                       Must support attribute access like l.x, l.y, l.z.

        Returns:
            normalized_list: List of dicts {'x', 'y', 'z', 'visibility'}.
        """
        # Convert to list of dicts for easier manipulation if needed, 
        # but here we compute metrics first.
        
        # Helper to get coords
        def get_coords(idx):
            l = landmarks[idx]
            return {'x': l.x, 'y': l.y, 'z': l.z, 'visibility': l.visibility}

        # 1. Calculate Hip Center (Origin)
        left_hip = get_coords(self.LEFT_HIP)
        right_hip = get_coords(self.RIGHT_HIP)
        
        hip_center = {
            'x': (left_hip['x'] + right_hip['x']) / 2,
            'y': (left_hip['y'] + right_hip['y']) / 2,
            'z': (left_hip['z'] + right_hip['z']) / 2
        }

        # 2. Calculate Shoulder Center
        left_shoulder = get_coords(self.LEFT_SHOULDER)
        right_shoulder = get_coords(self.RIGHT_SHOULDER)
        
        shoulder_center = {
            'x': (left_shoulder['x'] + right_shoulder['x']) / 2,
            'y': (left_shoulder['y'] + right_shoulder['y']) / 2,
            'z': (left_shoulder['z'] + right_shoulder['z']) / 2
        }

        # 3. Calculate Torso Size (Distance between Hip Center and Shoulder Center)
        dx = shoulder_center['x'] - hip_center['x']
        dy = shoulder_center['y'] - hip_center['y']
        dz = shoulder_center['z'] - hip_center['z']
        torso_size = math.sqrt(dx*dx + dy*dy + dz*dz)

        # Safety check for zero division
        if torso_size < 1e-6:
            # Fallback: scale = 1 if torso size is degenerate
            scale = 1.0
        else:
            scale = 1.0 / torso_size

        normalized_list = []
        for l in landmarks:
            # Translation relative to hip center
            tx = l.x - hip_center['x']
            ty = l.y - hip_center['y']
            tz = l.z - hip_center['z']

            # Scaling
            nx = tx * scale
            ny = ty * scale
            nz = tz * scale

            normalized_list.append({
                'x': nx,
                'y': ny,
                'z': nz,
                'visibility': l.visibility
            })

        return normalized_list

    def smooth(self, current_landmarks):
        """
        Apply Exponential Moving Average (EMA) smoothing.

        Args:
            current_landmarks: List of dicts {'x', 'y', 'z', 'visibility'}.

        Returns:
            smoothed_landmarks: List of dicts after smoothing.
        """
        if self.previous_landmarks is None:
            self.previous_landmarks = current_landmarks
            return current_landmarks

        smoothed_landmarks = []
        for i, curr in enumerate(current_landmarks):
            prev = self.previous_landmarks[i]
            
            # EMA formula: New = alpha * Current + (1 - alpha) * Previous
            sx = self.alpha * curr['x'] + (1 - self.alpha) * prev['x']
            sy = self.alpha * curr['y'] + (1 - self.alpha) * prev['y']
            sz = self.alpha * curr['z'] + (1 - self.alpha) * prev['z']
            
            # Use current visibility (or smooth it too, but usually raw is fine)
            sv = curr['visibility'] 

            smoothed_landmarks.append({
                'x': sx,
                'y': sy,
                'z': sz,
                'visibility': sv
            })

        self.previous_landmarks = smoothed_landmarks
        return smoothed_landmarks

    def process(self, landmarks):
        """
        Main pipeline: Normalize -> Smooth.

        Args:
            landmarks: Raw landmarks from MediaPipe.

        Returns:
            processed_landmarks: Normalized and smoothed landmarks.
        """
        if not landmarks:
            return None

        # 1. Normalize
        normalized = self.normalize(landmarks)

        # 2. Smooth
        smoothed = self.smooth(normalized)

        return smoothed
