import os

import cv2
import cvzone
import face_recognition

IMG_BACKGROUND = cv2.imread("assets/background.png")


def locate_faces():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        IMG_BACKGROUND[162 : 162 + 480, 55 : 55 + 640] = frame
        face_locations = face_recognition.face_locations(frame)

        for top, right, bottom, left in face_locations:
            cvzone.cornerRect(
                IMG_BACKGROUND, (55 + left, 162 + top, right - left, bottom - top), rt=0
            )

        cv2.imshow("Camera", IMG_BACKGROUND)
        cv2.waitKey(1)

        if cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1:
            break
    
    cap.release()
    cv2.destroyAllWindows()


def cache_known_encoding(folder):
    face_encodings = []
    names = []
    roll = []
    for filename in os.listdir(folder):
        # Fix so that it doesn't read hidden files
        if not filename.startswith('.'):
            img = cv2.imread(os.path.join(folder, filename), cv2.COLOR_BGR2RGB)
            face_encodings.append(face_recognition.face_encodings(img)[0])
            names.append(' '.join(filename.split('_')[1:]).split('.')[0].title())
            roll.append(int(filename.split('_')[0]))
    return face_encodings, names, roll

locate_faces()
