import time
import cv2 as cv
import mediapipe as mp
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from pynput.mouse import Button, Controller
import pyautogui
import warnings
import csv
import src.config as config
from src.Levels import ChangeLevel
from src.config import mouse, keyboard, Key

print(Button)
CamWidth, CamHeight = 1920, 1080
smooth = 7
FrameRate = 30

warnings.filterwarnings('ignore')
scalar = MinMaxScaler(feature_range=(0, 1))


def AddtoCSV(lmListML, action):
    lmListML.append(action)
    with open('train.csv', 'a+', newline='') as write_obj:
        writer = csv.writer(write_obj)
        writer.writerow(lmListML)


def trainModel(Nearest_Neighbors=10):
    data = pd.read_csv("train.csv", sep=",", header=0)
    data.head()
    y = data.iloc[:, -1]
    X = data.iloc[:, :21]
    rescaledX = scalar.fit_transform(X)
    a = KNeighborsClassifier(n_neighbors=Nearest_Neighbors)
    a.fit(rescaledX, y)
    return a


classifier = trainModel()


def FindMostFrequent(List):
    return max(set(List), key=List.count)


class HandControl(ChangeLevel):
    def __init__(self):
        super().__init__()
        self.mpHands = mp.solutions.hands
        self.DistancePixels = 50
        self.maxHands = 1
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mpHands.Hands(self.maxHands)
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.cIndexFingerLocX, self.cIndexFingerLocY = 0, 0
        self.pIndexFingerLocX, self.pIndexFingerLocY = 0, 0
        self.PreviousLocList = []
        self.lmList = []
        self.lmListML = []

    def Landmarks(self, img):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)
        return img

    def findLm(self, img):
        self.lmList = []
        self.lmListML = []
        xList = []
        yList = []
        if self.results.multi_hand_landmarks:
            handLMS = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(handLMS.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([cx, cy])
                self.lmListML.append(
                    math.sqrt(math.pow(cx - self.lmList[0][0], 2) + math.pow(cy - self.lmList[0][1], 2))
                )
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            cv.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
            return self.lmList

    def DrawSwipe(self, img):
        if self.isSwipe:
            cv.putText(img, "Swipe", (10, 250), cv.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0), 2, cv.LINE_AA)
            for i in range(len(self.Swipes) - 1):
                cv.line(img, (1280 - self.Swipes[i][0], self.Swipes[i][1]),(1280 - self.Swipes[i + 1][0], self.Swipes[i + 1][1]),(0, 255, 0), 5)

    def MoveMouse(self):
        mouse.release(Button.left)
        mouse.move(- 3 * self.Factor * (self.clocX - self.plocX), 3 * self.Factor * (self.clocY - self.plocY))
        config.OKTime = None

    def HoldMouse(self):
        pyautogui.mouseDown(button='left')
        mouse.move(- 2 * self.Factor * (self.clocX - self.plocX), 2 * self.Factor * (self.clocY - self.plocY))
        config.OKTime = None

    def CheckAction(self, img, PauseOrNot):
        try:
            self.Factor = self.DistancePixels / self.lmListML[1]
        except ZeroDivisionError:
            self.Factor = 1.0
        NewList = [i * self.Factor for i in self.lmListML]
        y_pred = classifier.predict(scalar.transform([NewList]))
        #AddtoCSV(NewList, 2)

        return config.ActionList[y_pred[0]]

    def NewLoc(self, wScr, hScr):
        x1, y1 = self.lmList[9][0:]
        x2, y2 = self.lmList[8][0:]
        x3 = np.interp(x1, (FrameRate, CamWidth - FrameRate), (0, wScr))
        y3 = np.interp(y1, (FrameRate, CamHeight - FrameRate), (0, hScr))
        x4 = np.interp(x2, (FrameRate, CamWidth - FrameRate), (0, wScr))
        y4 = np.interp(y2, (FrameRate, CamHeight - FrameRate), (0, hScr))
        self.clocX = round(self.plocX + (x3 - self.plocX) / smooth)
        self.clocY = round(self.plocY + (y3 - self.plocY) / smooth)
        self.cIndexFingerLocX = round(self.pIndexFingerLocX + (x4 - self.pIndexFingerLocX) / smooth)
        self.cIndexFingerLocY = round(self.pIndexFingerLocY + (y4 - self.pIndexFingerLocY) / smooth)
        return x1, y1

    def ChangeLoc(self):
        self.plocX, self.plocY = self.clocX, self.clocY
        self.pIndexFingerLocX, self.pIndexFingerLocY = self.cIndexFingerLocX, self.cIndexFingerLocY


class MouseMovement:
    def __init__(self):
        self.currentTimeLeft = time.time()
        self.currentTimeRight = time.time()
        self.PauseOrNot = False

    def MouseSingleClickLeft(self):
        mouse.release(Button.left)
        if self.PauseOrNot:
            pass
        elif (time.time() - self.currentTimeLeft) > 1:
            mouse.click(Button.left)
            mouse.release(Button.left)
            self.currentTimeLeft = time.time()
        config.OKTime = None

    def Pause(self, img):
        mouse.release(Button.left)
        if config.OKTime is None:
            config.OKTime = time.time()
        elif config.OKTime + 2 <= time.time():
            self.PauseOrNot = not self.PauseOrNot
            config.OKTime = None
        else:
            cv.putText(img, str(round(time.time() - config.OKTime, 1)), (260, 100), cv.FONT_HERSHEY_DUPLEX, 3,
                       (0, 255, 0), 2, cv.LINE_AA)

    def MouseSingleClickRight(self):
        mouse.release(Button.left)
        if self.PauseOrNot:
            pass
        elif (time.time() - self.currentTimeRight) > 1:
            mouse.click(Button.right)
            mouse.release(Button.right)
            self.currentTimeRight = time.time()
        config.OKTime = None

    def ReleaseMouse(self):
        mouse.release(Button.left)

    def ScrollDown(self):
        mouse.scroll(0, -.5)

    def ScrollUp(self):
        mouse.scroll(0, .5)
