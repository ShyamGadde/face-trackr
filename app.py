import cv2
import face_recognition
import cvzone


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('assets/background.png')

while True:
    ret, frame = cap.read()

    if not ret:
        break

    imgBackground[162:162 + 480, 55:55 + 640] = frame

    face_locations = face_recognition.face_locations(frame)
    for top, right, bottom, left in face_locations:
        cvzone.cornerRect(imgBackground, (55 + left, 162 + top, right - left, bottom - top), rt=0)
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Camera", imgBackground)
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
