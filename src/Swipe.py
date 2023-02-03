import time
import cv2 as cv
import numpy as np
import math
import pyautogui
import src.config as config

class DetectSwipe():
    def __init__(self):
        super().__init__()
        self.cIndexFingerLocY = None
        self.cIndexFingerLocX = None
        self.SwipeDistance = 500
        self.StartCounting = False
        self.Counter = 0
        self.SwipeTracker = []
        self.Swipes = []
        self.Factor = 0
        self.HasSwiped = False
        self.isSwipe = False

    def RecordSwipe(self, img, y_pred):
        if (self.StartCounting is True and len(self.SwipeTracker) == 30):
            self.StartCounting = False
            config.SwipeTime = time.time()
            self.Swipes = []
            self.Swipes = self.SwipeTracker
            self.SwipeTracker = []
        elif y_pred == "Swipe Action" and self.StartCounting is False and time.time() - config.SwipeTime > 2:
            self.HasSwiped = False
            self.SwipeTracker.append((self.cIndexFingerLocX, self.cIndexFingerLocY, y_pred))
            self.StartCounting = True
            self.isSwipe = False
        elif self.StartCounting is True:
            self.SwipeTracker.append((self.cIndexFingerLocX, self.cIndexFingerLocY, y_pred))

        if time.time() - config.SwipeTime < 2 and len(self.Swipes) != 0:
            if not self.HasSwiped:
                self.CheckSwipe()
            else:
                self.isSwipe = True


    def CheckSwipe(self):
        TotalDistance = [math.sqrt(
            math.pow(self.Swipes[i + 1][0] - self.Swipes[i][0], 2) + math.pow(self.Swipes[i + 1][1] - self.Swipes[i][1],
                                                                              2)) for i in range(len(self.Swipes) - 1)]
        if np.array(self.Swipes).T.tolist()[2].count("Swipe Action") > 3 and sum(TotalDistance) * self.Factor > 500:
            print(np.array(self.Swipes).T.tolist())
            if sum([self.Swipes[i][0] - self.Swipes[i + 1][0] for i in range(len(self.Swipes) - 1)]) < 0:
                pyautogui.hotkey('alt', 'shift', 'tab', _pause=False)
                print("FORWARD")
            else:
                pyautogui.hotkey('alt', 'tab')
                print("Backward")
            self.HasSwiped = True
