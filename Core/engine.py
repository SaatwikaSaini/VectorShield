import cv2
import numpy as np
import csv
import os
from core.config import BiometricConfig

class VectorEngine:
    """Handles the feature extraction math and database storage layers."""
    def __init__(self, config: BiometricConfig = BiometricConfig()):
        self.config = config
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load facial feature Haar Cascade XML reference.")

    def extract_features(self, face_roi) -> np.ndarray:
        """Downsamples and flattens a facial region matrix into an idealized 10-D space."""
        resized = cv2.resize(face_roi, self.config.grid_shape)
        normalized = np.round(resized.flatten() / 255.0, 2)
        return normalized

    def save_template(self, vector: np.ndarray) -> None:
        """Saves a baseline vector array template into database storage."""
        with open(self.config.csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(vector.tolist())

    def load_template(self) -> np.ndarray:
        """Reads the currently stored template from database storage."""
        if not os.path.exists(self.config.csv_filename):
            raise FileNotFoundError("No active biometric template discovered on disk.")
            
        with open(self.config.csv_filename, 'r') as file:
            reader = csv.reader(file)
            raw_data = next(reader)
            return np.array([float(val) for val in raw_data])

    def evaluate_match(self, current_vector: np.ndarray) -> dict:
        """Calculates distance between vectors and assesses authentication validation."""
        try:
            stored_vector = self.load_template()
        except FileNotFoundError:
            return {"error": "Missing Template"}

        # Perform geometric distance validation (Euclidean / L2 Norm)
        distance = float(np.linalg.norm(stored_vector - current_vector))
        is_accepted = distance < self.config.security_threshold
        
        return {
            "stored_template": stored_vector.tolist(),
            "captured_template": current_vector.tolist(),
            "distance": distance,
            "is_accepted": is_accepted
        }