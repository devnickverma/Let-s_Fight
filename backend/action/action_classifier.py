"""
backend/action/action_classifier.py

This module implements a rule-based action classifier for the MVP.
It analyzes pose landmarks to detect specific boxing actions (e.g., jab, cross, hook).
"""

"""
backend/action/action_classifier.py

This module implements a rule-based action classifier for the MVP.
It analyzes pose features to detect IDLE, JAB, and GUARD actions.
"""

"""
backend/action/action_classifier.py

This module implements a rule-based action classifier for the MVP.
It analyzes pose features to detect IDLE, JAB, and GUARD actions.
"""

from collections import deque

class ActionClassifier:
    def __init__(self):
        """
        Initialize the rule-based classifier with thresholds and state.
        """
        # Thresholds (Normalized Units based on Torso Length)
        self.VELOCITY_JAB_THRESH = 0.35
        self.VELOCITY_GUARD_THRESH = 0.12 # Slightly higher leniency
        
        # Angles in Degrees
        self.ELBOW_JAB_ANGLE = 145.0 # Near full extension
        
        # Distances (Normalized)
        self.WRIST_SHOULDER_GUARD_DIST = 0.65 
        
        # Temporal Logic
        self.MAX_HISTORY = 5
        self.left_vel_history = deque(maxlen=self.MAX_HISTORY)
        self.right_vel_history = deque(maxlen=self.MAX_HISTORY)
        
        # Guard Persistence
        self.guard_frames = 0
        self.GUARD_PERSISTENCE = 5
        
        # Jab Cooldown
        self.jab_cooldown = 0
        
        # Debouncing
        self.consecutive_frames = 0
        self.current_potential_action = "IDLE"
        self.stable_action = "IDLE"
        self.stable_confidence = 0.0
        self.DEBOUNCE_THRESHOLD = 2 

    def classify(self, features):
        """
        Classify the current action based on features.
        Priority: JAB > GUARD > IDLE.
        """
        potential_action = "IDLE"
        confidence = 0.0
        
        # Extract features
        l_vel = features.get('left_wrist_velocity', 0)
        r_vel = features.get('right_wrist_velocity', 0)
        l_angle = features.get('left_elbow_angle', 0)
        r_angle = features.get('right_elbow_angle', 0)
        l_dist_shoulder = features.get('left_wrist_shoulder_dist', 100)
        r_dist_shoulder = features.get('right_wrist_shoulder_dist', 100)
        
        # Update histories
        self.left_vel_history.append(l_vel)
        self.right_vel_history.append(r_vel)
        
        # Handle Cooldown
        if self.jab_cooldown > 0:
            self.jab_cooldown -= 1
            
        # --- Rule 1: JAB (Temporal) ---
        # Check if ANY frame in recent history had high velocity (Burst)
        # AND current frame has high extension
        left_burst = any(v > self.VELOCITY_JAB_THRESH for v in self.left_vel_history)
        right_burst = any(v > self.VELOCITY_JAB_THRESH for v in self.right_vel_history)
        
        is_left_jab = left_burst and (l_angle > self.ELBOW_JAB_ANGLE)
        is_right_jab = right_burst and (r_angle > self.ELBOW_JAB_ANGLE)
        
        if (is_left_jab or is_right_jab) and self.jab_cooldown == 0:
            potential_action = "JAB"
            self.jab_cooldown = 15 # Prevent spamming
            
            # Confidence
            vel_score = max(l_vel, r_vel) / self.VELOCITY_JAB_THRESH
            angle_score = max(l_angle, r_angle) / 180.0
            confidence = min(1.0, (vel_score + angle_score) / 2.0)
            
            # Reset Guard counter if jabbing
            self.guard_frames = 0

        # --- Rule 2: GUARD (Stable) ---
        elif potential_action == "IDLE": # Only check if not JAB
            is_guard_pose = (l_dist_shoulder < self.WRIST_SHOULDER_GUARD_DIST and 
                             r_dist_shoulder < self.WRIST_SHOULDER_GUARD_DIST and
                             l_vel < self.VELOCITY_GUARD_THRESH and 
                             r_vel < self.VELOCITY_GUARD_THRESH)
            
            if is_guard_pose:
                self.guard_frames += 1
            else:
                self.guard_frames = 0
                
            if self.guard_frames >= self.GUARD_PERSISTENCE:
                potential_action = "GUARD"
                confidence = min(1.0, self.guard_frames / 10.0) # Increases with stability

        # --- Rule 3: IDLE ---
        if potential_action == "IDLE":
             # Confidence drops as movement increases
             avg_vel = (l_vel + r_vel) / 2.0
             confidence = max(0.0, 1.0 - (avg_vel * 2.0))

        # --- Debouncing ---
        if potential_action == self.current_potential_action:
            self.consecutive_frames += 1
        else:
            self.consecutive_frames = 1
            self.current_potential_action = potential_action
            
        # Instant switch for JAB (it's fast), Debounce others
        if potential_action == "JAB":
             self.stable_action = "JAB"
             self.stable_confidence = confidence
        elif self.consecutive_frames >= self.DEBOUNCE_THRESHOLD:
            self.stable_action = potential_action
            self.stable_confidence = confidence
            
        return {
            "action": self.stable_action,
            "confidence": self.stable_confidence
        }

