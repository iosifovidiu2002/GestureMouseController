import cv2
import time
import numpy as np
import HandTracking as ht
from pynput.mouse import Button, Controller

mouse = Controller()


def angle(x1, y1, x2, y2):
    vector_1 = [x1, y1]
    vector_2 = [x2, y2]
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return np.arccos(dot_product)


cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

pTime = 0
cTime = 0
distances = {}
last_activation_time = time.time()
detector = ht.HandTracker(mouseTracking=False, minDetConf=0.75, minTrConf=0.75)
clicked = False
mouseTracking = False
while True:
    success, img = cap.read()
    img, landmarks, g = detector.findHandsAndList(img, list=True)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if len(landmarks) != 0:
        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]
        x3, y3 = landmarks[12][1], landmarks[12][2]
        cv2.circle(img, (x1, y1), 15, (204, 0, 204), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (204, 0, 204), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (204, 0, 204), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 204, 0), thickness=10)
        cv2.line(img, (x1, y1), (x3, y3), (0, 204, 0), thickness=10)

        a1 = angle(g[0] - x1, g[1] - y1, g[0] - x2, g[1] - y2)
        a2 = angle(g[0] - x1, g[1] - y1, g[0] - x3, g[1] - y3)
        print(a2)

        # Activate Click Mechanism
        if a2 < 0.2:
            if time.time() - last_activation_time > 0.4:
                mouseTracking = not mouseTracking
                detector.setMouseTracking(mouseTracking)
                last_activation_time = time.time()

        # Click-Mechanism
        if detector.getMouseTracking():
            if a1 < 0.405:
                print(" Click")
                if clicked:
                    mouse.press(Button.left)
                    clicked = False
                else:
                    clicked = True
            else:
                mouse.release(Button.left)
                print("No click")
                clicked = False

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Track hand", img)
    cv2.waitKey(1)
