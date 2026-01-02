"""
backend/action/feature_extractor.py

This module extracts interpretable features from normalized pose landmarks.
Features include joint angles, limb distances, and velocities.
"""

import math

class FeatureExtractor:
    def __init__(self):
        """
        Initialize FeatureExtractor.
        Keeps track of previous state for temporal features (velocity).
        """
        self.prev_landmarks = None
        
        # Landmark Indices (MediaPipe)
        self.LEFT_SHOULDER = 11
        self.RIGHT_SHOULDER = 12
        self.LEFT_ELBOW = 13
        self.RIGHT_ELBOW = 14
        self.LEFT_WRIST = 15
        self.RIGHT_WRIST = 16
        self.LEFT_HIP = 23
        self.RIGHT_HIP = 24

    def _calculate_distance(self, p1, p2):
        """
        Calculate Euclidean distance between two points.
        
        Args:
            p1, p2: Dicts with 'x', 'y', 'z'.
            
        Returns:
            float: Euclidean distance.
        """
        dx = p1['x'] - p2['x']
        dy = p1['y'] - p2['y']
        dz = p1['z'] - p2['z']
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def _calculate_angle(self, a, b, c):
        """
        Calculate the angle at point b given points a, b, c.
        Uses vector dot product.
        
        Args:
            a, b, c: Dicts with 'x', 'y', 'z'.
            
        Returns:
            float: Angle in degrees (0 to 180).
        """
        # Vectors BA and BC
        ba = {'x': a['x'] - b['x'], 'y': a['y'] - b['y'], 'z': a['z'] - b['z']}
        bc = {'x': c['x'] - b['x'], 'y': c['y'] - b['y'], 'z': c['z'] - b['z']}
        
        # Dot product
        dot_product = ba['x'] * bc['x'] + ba['y'] * bc['y'] + ba['z'] * bc['z']
        
        # Magnitudes
        mag_ba = math.sqrt(ba['x']**2 + ba['y']**2 + ba['z']**2)
        mag_bc = math.sqrt(bc['x']**2 + bc['y']**2 + bc['z']**2)
        
        if mag_ba * mag_bc == 0:
            return 0.0
            
        # Cosine rule with clamping to avoid domain errors [-1, 1]
        cosine_angle = dot_product / (mag_ba * mag_bc)
        cosine_angle = max(-1.0, min(1.0, cosine_angle))
        
        angle = math.acos(cosine_angle)
        return math.degrees(angle)

    def extract(self, landmarks, dt=1.0):
        """
        Extract features from the current frame's normalized landmarks.
        
        Args:
            landmarks: List of dicts (normalized).
            dt: Time delta between frames (default 1.0 for simple per-frame delta).
            
        Returns:
            dict: Extracted features.
        """
        features = {}

        # 1. Joint Angles (Elbows)
        # Left Elbow: L_Shoulder (11) - L_Elbow (13) - L_Wrist (15)
        features['left_elbow_angle'] = self._calculate_angle(
            landmarks[self.LEFT_SHOULDER],
            landmarks[self.LEFT_ELBOW],
            landmarks[self.LEFT_WRIST]
        )
        
        # Right Elbow: R_Shoulder (12) - R_Elbow (14) - R_Wrist (16)
        features['right_elbow_angle'] = self._calculate_angle(
            landmarks[self.RIGHT_SHOULDER],
            landmarks[self.RIGHT_ELBOW],
            landmarks[self.RIGHT_WRIST]
        )

        # 2. Distances (Wrist to Shoulder/Hip)
        # Left Wrist to Shoulder
        features['left_wrist_shoulder_dist'] = self._calculate_distance(
            landmarks[self.LEFT_WRIST], landmarks[self.LEFT_SHOULDER]
        )
        
        # Right Wrist to Shoulder
        features['right_wrist_shoulder_dist'] = self._calculate_distance(
            landmarks[self.RIGHT_WRIST], landmarks[self.RIGHT_SHOULDER]
        )
        
        # Hip Center Calculation
        hip_center = {
            'x': (landmarks[self.LEFT_HIP]['x'] + landmarks[self.RIGHT_HIP]['x']) / 2.0,
            'y': (landmarks[self.LEFT_HIP]['y'] + landmarks[self.RIGHT_HIP]['y']) / 2.0,
            'z': (landmarks[self.LEFT_HIP]['z'] + landmarks[self.RIGHT_HIP]['z']) / 2.0
        }
        
        features['left_wrist_hip_dist'] = self._calculate_distance(
            landmarks[self.LEFT_WRIST], hip_center
        )
        features['right_wrist_hip_dist'] = self._calculate_distance(
            landmarks[self.RIGHT_WRIST], hip_center
        )

        # 3. Velocities (Wrists)
        if self.prev_landmarks:
            # Left Wrist Velocity
            dist_l = self._calculate_distance(landmarks[self.LEFT_WRIST], self.prev_landmarks[self.LEFT_WRIST])
            features['left_wrist_velocity'] = dist_l / dt
            
            # Right Wrist Velocity
            dist_r = self._calculate_distance(landmarks[self.RIGHT_WRIST], self.prev_landmarks[self.RIGHT_WRIST])
            features['right_wrist_velocity'] = dist_r / dt
        else:
            features['left_wrist_velocity'] = 0.0
            features['right_wrist_velocity'] = 0.0

        # Update previous state
        # We need to copy the landmarks or ensure they aren't mutated elsewhere. 
        # Since we create new dicts in PoseProcessor, this reference should be safe for this frame.
        self.prev_landmarks = landmarks

        return features
