import mediapipe as mp
import cv2
import mouse
import pyautogui


class HandTracker:
    def __init__(self, mode=False, maxHands=2, minDetConf=0.5, minTrConf=0.5, mouseTracking=False):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, minDetConf, minTrConf)
        self.mpDraw = mp.solutions.drawing_utils
        self.mouseTracking = mouseTracking

    def findHandsandList(self, img, list=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        listLM = []
        gX = 0
        gY = 0
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            handLms = self.results.multi_hand_landmarks[0]
            self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if list:
                    listLM.append([id, cx, cy])
                if id == 0 or id == 5 or id == 9 or id == 13 or id == 17:
                    gX += cx
                    gY += cy
            gX /= 5
            gY /= 5
            cv2.circle(img, (int(gX), int(gY)), 10, (0, 0, 204), cv2.FILLED)
            if self.mouseTracking:
                W, H = pyautogui.size()
                h, w, _ = img.shape
                mouse.move(W - W * (gX) / w, H * (gY) / h)
        return img, listLM, (gX, gY)

    def mouseTrack(self, img):
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                gX = 0
                gY = 0
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 0 or id == 5 or id == 9 or id == 13 or id == 17:
                        gX += cx
                        gY += cy
                gX /= 5
                gY /= 5
                cv2.circle(img, (int(gX), int(gY)), 10, (0, 0, 204), cv2.FILLED)
                if self.mouseTracking:
                    W, H = pyautogui.size()
                    h, w, _ = img.shape
                    mouse.move(W - W * (gX) / w, H * (gY) / h)
        return img

    def setMouseTracking(self):
        self.mouseTracking = not self.mouseTracking

    def getMouseTracking(self):
        return self.mouseTracking

