import time
from src.Swipe import DetectSwipe
import src.config as config
from src.config import keyboard, Key, mouse, Button


class ChangeLevel(DetectSwipe):
    def __init__(self):
        super().__init__()
        self.lmList = None
        print("LEVEL CHECK")
        self.CurrentPositionY = None
        self.CurrentLevelTime = time.time()
        self.PositionYCounter = 0

    def CheckLevel(self, Action, Action2):
        config.OKTime = None
        mouse.release(Button.left)
        if self.CurrentPositionY is not None:
            if time.time() - self.CurrentLevelTime > 1:
                self.CurrentPositionY = None

        if self.CurrentPositionY is None:
            self.CurrentPositionY = self.lmList[9][1]
        self.PositionYCounter += -(self.lmList[9][1] - self.CurrentPositionY)
        LoopDuration = self.PositionYCounter // 5
        if LoopDuration >= 0:
            for i in range(LoopDuration):
                Action()
        else:
            for i in range(abs(LoopDuration)):
                Action2()
        self.PositionYCounter = self.PositionYCounter % 5
        self.CurrentPositionY = self.lmList[9][1]
        self.CurrentLevelTime = time.time()
