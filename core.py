import multiprocessing
import os
import queue
import threading
import time
from collections import deque
from datetime import datetime

import cv2
import face_recognition
import numpy as np
from cvzone import cornerRect

from excel import generate_attendance_report

IMG_BACKGROUND = cv2.imread("assets/background.png")
STATUS_IMG = {
    "active": cv2.imread("assets/status/active.png"),
    "present": cv2.imread("assets/status/present.png"),
    "marked": cv2.imread("assets/status/marked.png"),
    "already_marked": cv2.imread("assets/status/already-marked.png"),
}


def detect_faces(faces_queue, console_status_queue, exit_flag):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    student_img = None
    status_code = "active"
    student_id = ""
    first_name = last_name = ""

    def update_console_status():
        nonlocal status_code, student_img, student_id, first_name, last_name

        while not exit_flag.value:
            try:
                status, student_id, name, student_img = console_status_queue.get(timeout=0.1)
                first_name, last_name = name.split()
            except queue.Empty:
                    continue

            status_code = "present"
            time.sleep(1.5)

            status_code = status
            time.sleep(1)
    
            status_code = "active"
            time.sleep(2)
    
    threading.Thread(target=update_console_status).start()

    counter = 0

    while True:
        ret, frame = cap.read()

        if not ret: 
            break

        IMG_BACKGROUND[120 : 120 + 480, 100 : 100 + 640] = frame
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(frame)

        counter += 1
        if counter % 5 == 0:
            # Only send every tenth frame to the other process
            faces_queue.put((frame, face_locations))

        for top, right, bottom, left in face_locations:
            cornerRect(
                IMG_BACKGROUND, (100 + left, 120 + top, right - left, bottom - top), 
                rt=0
            )
        
        IMG_BACKGROUND[85:85 + 550, 820:820 + 370] = STATUS_IMG[status_code]
        if status_code == "present":
            IMG_BACKGROUND[145:145 + 216, 896:896 + 216] = student_img
            (w, _), _ = cv2.getTextSize(first_name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = 820 + (370 - w) // 2
            cv2.putText(IMG_BACKGROUND, first_name, (offset, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            (w, _), _ = cv2.getTextSize(last_name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = 820 + (370 - w) // 2
            cv2.putText(IMG_BACKGROUND, last_name, (offset, 475), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.putText(IMG_BACKGROUND, student_id, (975, 555), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Camera", IMG_BACKGROUND)
        cv2.waitKey(1)

        if cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1:
            exit_flag.value = 1
            break

    cap.release()
    cv2.destroyAllWindows()


def cache_database(path):
    face_encodings = []
    names = []
    ids = []
    student_imgs = []
    for filename in os.listdir(path):
        # Fix so that it doesn't read hidden files
        if not filename.startswith("."):
            img = cv2.imread(os.path.join(path, filename), cv2.COLOR_BGR2RGB)
            student_imgs.append(img)
            face_encodings.append(face_recognition.face_encodings(img)[0])
            names.append(" ".join(filename.split("_")[1:]).split(".")[0].title())
            ids.append(int(filename.split("_")[0]))
    return face_encodings, ids, names, student_imgs


def process_frame(faces_queue, console_status_queue, exit_flag, attendees):
    known_face_encodings, known_face_ids, known_face_names, known_student_imgs = cache_database(
        "Student_DB"
    )
    previous_two = deque([None, None], maxlen=2)

    while True:
        try:
            frame, face_locations = faces_queue.get(timeout=1)
        except queue.Empty:
            if exit_flag.value:
                break
            else:
                continue
        
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )

            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                status = "already_marked"
                name = known_face_names[best_match_index]
                student_id = known_face_ids[best_match_index]
                student_img = known_student_imgs[best_match_index]

                # Check if it is the same student in the past two frames and skip if it is
                if student_id == previous_two[0] == previous_two[1]:
                    continue
                previous_two.append(student_id)

                if student_id not in attendees:
                    status = "marked"
                    attendees[student_id] = (name, datetime.now().strftime("%I:%M %p"))
                
                console_status_queue.put((status, str(student_id), name, student_img))



def create_session():
    faces_queue = multiprocessing.Queue()
    console_status_queue = multiprocessing.Queue()
    exit_flag = multiprocessing.Value("i", 0)
    attendees = multiprocessing.Manager().dict()

    detect_faces_process = multiprocessing.Process(
        target=detect_faces,
        args=(
            faces_queue,
            console_status_queue,
            exit_flag,
        ),
    )
    detect_faces_process.start()

    process_frame_process = multiprocessing.Process(
        target=process_frame,
        args=(
            faces_queue,
            console_status_queue,
            exit_flag,
            attendees,
        ),
    )
    process_frame_process.start()

    detect_faces_process.join()

    # Empty the queue after the detect_faces_process has finished
    while console_status_queue.qsize() > 0:
        try:
            console_status_queue.get()
        except queue.Empty:
            break

    process_frame_process.join()

    generate_attendance_report(attendees)


if __name__ == "__main__":
    create_session()
