import pickle
from collections import deque
from datetime import datetime
from multiprocessing import Manager, Process, Queue, Value
from queue import Empty
from threading import Thread
from time import sleep

import cv2
import face_recognition
from cvzone import cornerRect
from numpy import argmin, frombuffer, uint8

from database import Database
from excel import generate_attendance_report

IMG_BACKGROUND = cv2.imread("assets/background.png")
STATUS_IMG = {
    "active": cv2.imread("assets/status/active.png"),
    "present": cv2.imread("assets/status/present.png"),
    "marked": cv2.imread("assets/status/marked.png"),
    "already_marked": cv2.imread("assets/status/already-marked.png"),
}


def detect_faces(faces_queue, console_status_queue, exit_flag):
    """
    It captures video from the webcam, detects faces in the video, and displays the video with the
    detected faces on the screen. It also sends the frames to the other process for face recognition.
    
    :param faces_queue: A multiprocessing.Queue object that will be used to send frames to the other
    process
    :param console_status_queue: A queue that will be used to send messages to the console thread
    :param exit_flag: A multiprocessing.Value object that is set to 1 when the program is exiting
    """
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    student_img = None
    status_code = "active"
    student_id = ""
    first_name = last_name = ""

    def update_console_status():
        """
        It updates the status on the console. It is run in a separate thread. It is also used to display the student's image, name, and ID on the console. It is also used to display the status of the console on the console.
        """
        nonlocal status_code, student_img, student_id, first_name, last_name

        while not exit_flag.value:
            try:
                status, student_id, name, student_img = console_status_queue.get(
                    timeout=0.1
                )
                first_name, last_name = name.split()
            except Empty:
                continue

            status_code = "present"
            sleep(1.5)

            status_code = status
            sleep(1)

            status_code = "active"
            sleep(2)

    Thread(target=update_console_status).start()

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
                IMG_BACKGROUND,
                (100 + left, 120 + top, right - left, bottom - top),
                rt=0,
            )

        IMG_BACKGROUND[85 : 85 + 550, 820 : 820 + 370] = STATUS_IMG[status_code]
        if status_code == "present":
            IMG_BACKGROUND[145 : 145 + 216, 896 : 896 + 216] = student_img
            (w, _), _ = cv2.getTextSize(first_name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = 820 + (370 - w) // 2
            cv2.putText(
                IMG_BACKGROUND,
                first_name,
                (offset, 450),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            (w, _), _ = cv2.getTextSize(last_name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = 820 + (370 - w) // 2
            cv2.putText(
                IMG_BACKGROUND,
                last_name,
                (offset, 475),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                IMG_BACKGROUND,
                student_id,
                (975, 555),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

        cv2.imshow("Camera", IMG_BACKGROUND)
        cv2.waitKey(1)

        if cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1:
            exit_flag.value = 1
            break

    cap.release()
    cv2.destroyAllWindows()


def cache_database(database):
    """
    It takes a database name, connects to the database, fetches all the data, closes the database
    connection, decodes the images, and unpickles the face encodings. It returns all the data. It is used to cache the data in the database so that it can be used by the other process.
    
    :param database: The path to the database file
    :return: known_face_ids, known_face_names, known_student_imgs, known_face_encodings
    """
    db = Database(database)
    (
        known_face_ids,
        known_face_names,
        known_student_imgs,
        known_face_encodings,
    ) = zip(*db.fetch())

    del db

    known_student_imgs = tuple(
        map(
            lambda buffer: cv2.imdecode(
                frombuffer(buffer, uint8), cv2.IMREAD_COLOR
            ),
            known_student_imgs,
        )
    )

    known_face_encodings = tuple(map(pickle.loads, known_face_encodings))

    return known_face_ids, known_face_names, known_student_imgs, known_face_encodings


def process_frame(faces_queue, console_status_queue, exit_flag, attendees):
    """
    It takes a frame, finds the faces in it, and then compares them to the faces in the database. If it
    finds a match, it will add the student to the list of attendees. It will also send the student's name, ID, and image to the console process. 
    
    :param faces_queue: A queue that contains the frame and the face locations
    :param console_status_queue: A queue that is used to send the status of the student to the console
    :param exit_flag: A multiprocessing.Value object that is set to True when the program is exiting
    :param attendees: a dictionary of student_id: (name, time)
    """
    (
        known_face_ids,
        known_face_names,
        known_student_imgs,
        known_face_encodings,
    ) = cache_database("student.db")
    previous_two = deque([None, None], maxlen=2)

    while True:
        try:
            frame, face_locations = faces_queue.get(timeout=1)
        except Empty:
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
            best_match_index = argmin(face_distances)
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
    """
    It creates two processes, one to detect faces and one to process the frames. 
    
    The first process, detect_faces, is responsible for detecting faces in the video stream and putting
    them in a queue. 
    
    The second process, process_frame, is responsible for taking the faces from the queue and processing
    them. 
    """
    faces_queue = Queue()
    console_status_queue = Queue()
    exit_flag = Value("i", 0)
    attendees = Manager().dict()

    detect_faces_process = Process(
        target=detect_faces,
        args=(
            faces_queue,
            console_status_queue,
            exit_flag,
        ),
    )
    detect_faces_process.start()

    process_frame_process = Process(
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
        except Empty:
            break

    process_frame_process.join()

    generate_attendance_report(attendees)


if __name__ == "__main__":
    create_session()
