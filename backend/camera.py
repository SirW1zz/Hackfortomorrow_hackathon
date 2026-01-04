import face_recognition
import cv2
import numpy as np
import os
import time
from backend.database import get_all_students, update_attendance

# Global variables to cache encodings
known_face_encodings = []
known_face_names = []

def load_known_faces():
    global known_face_encodings, known_face_names
    path = "C:/Users/CraftingTable/Desktop/hackfortmr/pics"
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist.")
        return

    print("Loading known faces...")
    for file in os.listdir(path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(path, file)
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                
                if len(encodings) > 0:
                    encoding = encodings[0]
                    known_face_encodings.append(encoding)
                    # Extract name: "christy_1.jpg" -> "christy"
                    name = os.path.splitext(file)[0].split('_')[0]
                    known_face_names.append(name)
                    print(f"Loaded {name} from {file}")
            except Exception as e:
                print(f"Could not load {file}: {e}")
    print(f"Loaded {len(known_face_names)} faces.")

def scan_class(duration=15):
    """
    Scans for faces for a specified duration (seconds).
    Implements digital zoom/scanning logic.
    Updates database: Present for detected, Absent for others.
    """
    if not known_face_encodings:
        load_known_faces()

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open video capture.")
        return

    detected_students = set()
    start_time = time.time()
    
    print(f"Starting scan for {duration} seconds...")

    while (time.time() - start_time) < duration:
        ret, frame = video_capture.read()
        if not ret:
            break

        # 1. Full Frame Scan
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        found_names = process_frame(rgb_frame)
        detected_students.update(found_names)

        # 2. Digital Zoom / Quadrant Scan (Simulated PTZ)
        # If we haven't found everyone, or just to be robust, scan quadrants
        # Split frame into 4 quadrants
        h, w, _ = frame.shape
        half_h, half_w = h // 2, w // 2
        
        quadrants = [
            (0, half_h, 0, half_w),       # Top-Left
            (0, half_h, half_w, w),       # Top-Right
            (half_h, h, 0, half_w),       # Bottom-Left
            (half_h, h, half_w, w)        # Bottom-Right
        ]

        for q in quadrants:
            y1, y2, x1, x2 = q
            roi = frame[y1:y2, x1:x2]
            # Upscale the quadrant to simulate zoom (optional, but helps some detectors)
            # roi_zoomed = cv2.resize(roi, (w, h), interpolation=cv2.INTER_LINEAR)
            rgb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            
            found_names_roi = process_frame(rgb_roi)
            detected_students.update(found_names_roi)

        # Draw boxes and names on the frame
        for name in found_names:
            # Note: We don't have exact coordinates here because process_frame just returns names
            # To draw boxes, we'd need to refactor process_frame to return locations too.
            # For now, let's just put the list of detected people on the screen.
            cv2.putText(frame, f"Detected: {name}", (10, 50 + 30 * list(detected_students).index(name)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Scanning... (Press q to quit early)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Update Database
    all_students = get_all_students()
    print(f"Scan complete. Detected: {detected_students}")
    
    for student in all_students:
        # Clean student name from DB just in case
        student_clean = student.strip()
        if student_clean in detected_students:
            update_attendance(student_clean, 1)
        else:
            update_attendance(student_clean, 0)

    return list(detected_students)

def process_frame(rgb_image):
    """
    Helper to detect faces in an image and return found names.
    """
    found = []
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5) # Stricter tolerance
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                found.append(name)
    
    return found

if __name__ == "__main__":
    # Test run
    load_known_faces()
    scan_class(duration=5)
