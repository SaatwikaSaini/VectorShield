import cv2
import numpy as np
from core.config import BiometricConfig
from core.engine import VectorEngine

def main():
    config = BiometricConfig()
    try:
        engine = VectorEngine(config)
    except RuntimeError as e:
        print(f"[CRITICAL] {e}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Failed to discover local video hardware input stream.")
        return

    print("=== VECTORSHIELD: PRESENTATION ATTACK SIMULATOR ===")
    print(" [E] Enroll Template  |  [L] Test Live  |  [S] Test Spoof Attack  |  [Q] Quit")
    print("-" * 60)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Intermittent transmission drop encountered.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = engine.face_cascade.detectMultiScale(gray, config.scale_factor_face, config.min_neighbors_face)
        
        # Intercept inputs asynchronously at root frame step
        key = cv2.waitKey(1) & 0xFF
        command = None
        if key in [ord('e'), ord('l'), ord('s')]:
            command = chr(key)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_roi = gray[y:y+h, x:x+w]
            
            # Form current frame matrix representation
            current_vector = engine.extract_features(face_roi)

            if command == 'e':
                engine.save_template(current_vector)
                print(f"\n[*] ENROLL SUCCESS: 10-D Array Stored: {current_vector.tolist()}")
                command = None  # Reset latch

            elif command in ['l', 's']:
                results = engine.evaluate_match(current_vector)
                
                if "error" in results:
                    print(f"\n[!] VERIFICATION FAILURE: {results['error']}. Press 'E' to enroll first.")
                    command = None
                    continue

                test_type = "LIVE VALIDATION" if command == 'l' else "SPOOF ATTACK SIMULATION"
                status_label = "AUTHORIZED" if results["is_accepted"] else "ACCESS DENIED"
                
                print("\n" + "=" * 65)
                print(f" SIMULATION STEP : {test_type}")
                print("-" * 65)
                print(f" Stored Baseline  : {results['stored_template']}")
                print(f" Captured Matrix  : {results['captured_template']}")
                print(f" Vector Distance  : {results['distance']:.4f}")
                print(f" Threshold Limit  : {config.security_threshold:.4f}")
                print(f" Authentication   : {status_label}")
                print("=" * 65)

                if command == 's' and results["is_accepted"]:
                    print("[SECURITY ALERT] Spoof Attack Successful! Vector space validation bypassed.")
                
                command = None

        cv2.imshow('VectorShield: Biometric Engine Console', frame)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()