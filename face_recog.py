import face_recognition
import os

import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

path = "C:/Users/CraftingTable/Desktop/hackfortmr/pics"
known_face_encodings = []
known_face_names = []

for file in os.listdir(path):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        image_path = os.path.join(path, file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            encoding = encodings[0]
            known_face_encodings.append(encoding)
            # Use the filename as the name, stripping extension and any suffix after '_'
            name = os.path.splitext(file)[0].split('_')[0]
            known_face_names.append(name)

students = list(set(known_face_names))

face_locations = []
face_encodings = []

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    ret, frame = video_capture.read()
    # Process the full frame to detect faces from further away
    rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            if name in known_face_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottom_left_corner_of_text = (10, 100)
                font_scale = 1.5
                font_color = (255, 0, 0)
                thickness = 3
                line_type = 2
                cv2.putText(frame, name + " Present", bottom_left_corner_of_text,
                            font, font_scale, font_color, thickness, line_type)

                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])
                    
                    # Update Supabase using backend module
                    from backend.database import update_attendance
                    update_attendance(name, 1)

    cv2.imshow("camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
