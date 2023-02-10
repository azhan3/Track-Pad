import cv2 as cv
import time
import src.Classes as Classes
from tkinter import *
import src.config as config
from src.config import mouse, Button
import numpy as np
from numba import jit

CamWidth, CamHeight = 1920, 1080

detector = Classes.HandControl()
MouseMovement = Classes.MouseMovement()


def a():
    pass


# Main Window
class MainWindow:
    def __init__(self, cap):
        self.MouseDict = {"Open Palm": detector.MoveMouse,
                          "Fist": self.NoAction,
                          "Index Finger": MouseMovement.MouseSingleClickLeft,
                          "Swipe Action": lambda: detector.RecordSwipe(self.img2, self.ExecutedFunction),
                          "No Action": self.NoAction,
                          "Spider-Man": lambda: detector.CheckLevel(config.VolumeUp, config.VolumeDown),
                          "OK": lambda: MouseMovement.Pause(self.img2),
                          "Telephone":detector.HoldMouse
                          }
        self.SwipeList = []
        for i in config.GestureDict:
            if config.GestureDict[i] == "Swipe":
                self.SwipeList.append(i)
        self.wScr, self.hScr = 1920.0, 1080.0
        self.Time = None
        self.cap = cap
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.p = "No Action"
        #self.window = window
        self.PreviousAction = "No Action"
        self.PreviouPrevioussAction = "No Action"
        self.ShowHands = True
        self.x1 = 640
        self.y1 = 360

    def NoAction(self):
        mouse.release(Button.left)
        config.OKTime = None

    #@jit
    def run(self):
        #self.canvas = Canvas(self.window, width=1280, height=720, bg="black")
        #self.canvas.grid(row=0, column=0)
        num_frames = 0
        start_time = time.time()
        while self.cap.isOpened():
            success, img = self.cap.read()
            num_frames += 1
            elapsed_time = time.time() - start_time
            fps = num_frames / elapsed_time
            fps_text = "FPS: {:.2f}".format(fps)

            # Display the framerate on the top right corner of the window
            
            (h, w) = img.shape[:2]
            r = 480 / float(h)
            
            img = detector.Landmarks(img)
            lmList = detector.findLm(img)
            self.img2 = cv.flip(img, 1)
            #self.img2 = cv.cvtColor(self.img2, cv.COLOR_BGR2RGB)
            self.ExecutedFunction = "No Action"
            if lmList is not None:
                self.x1, self.y1 = detector.NewLoc(self.wScr, self.hScr)
                self.PreviouPrevioussAction = self.PreviousAction
                self.PreviousAction = self.p
                self.p = detector.CheckAction(self.img2, MouseMovement.PauseOrNot)
                if self.p == self.PreviousAction == self.PreviouPrevioussAction:
                    self.ExecutedFunction = self.p
                else:
                    self.ExecutedFunction = self.PreviouPrevioussAction
                if not MouseMovement.PauseOrNot:
                    # self.MouseDict["Swipe Action"]()
                    self.MouseDict[self.ExecutedFunction]()
                elif MouseMovement.PauseOrNot and self.ExecutedFunction == "OK":
                    self.MouseDict[self.ExecutedFunction]()
                else:
                    config.OKTime = None

                detector.ChangeLoc()
            if MouseMovement.PauseOrNot is False:
                cv.putText(self.img2, self.ExecutedFunction, (10, 450), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3,
                           cv.LINE_AA)
                cv.putText(self.img2, self.ExecutedFunction, (10, 450), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2,
                           cv.LINE_AA)
            else:
                cv.putText(self.img2, "Paused", (10, 450), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3, cv.LINE_AA)
                cv.putText(self.img2, "Paused", (10, 450), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2, cv.LINE_AA)
            if time.time() - config.SwipeTime < 2:
                cv.putText(self.img2, str(round(time.time() - config.SwipeTime, 1)), (10, 100), cv.FONT_HERSHEY_SIMPLEX, 3,
                           (0, 0, 0),
                           3, cv.LINE_AA)
                cv.putText(self.img2, str(round(time.time() - config.SwipeTime, 1)), (10, 100), cv.FONT_HERSHEY_SIMPLEX, 3,
                           (255, 255, 255),
                           2, cv.LINE_AA)
            self.Image()
            cv.putText(self.ImageShown, fps_text, (1280 - 250, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv.LINE_AA)
            #print(len(self.ImageShown[0]))
            ret, buffer = cv.imencode('.jpg', self.ImageShown)

            frame = buffer.tobytes()
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

    def ChangeView(self):
        self.ShowHands = not self.ShowHands

    def Exit(self):
        self.cap.release()
        #self.window.destroy()
        config.Exit = True

    #@jit
    def Image(self):
        if not MouseMovement.PauseOrNot:
            detector.RecordSwipe(self.img2, self.ExecutedFunction)
            detector.DrawSwipe(self.img2)
        grayImage = cv.cvtColor(self.img2, cv.COLOR_BGR2GRAY)
        (thresh, self.blackAndWhiteImage) = cv.threshold(grayImage, 255, 255, cv.THRESH_BINARY)

        cv.circle(self.blackAndWhiteImage, (1280 - self.x1 + 20, self.y1), 5, (255, 255, 255), -1)
        
        self.ImageShown = self.img2
        #print(len(self.ImageShown))
        #self.image = Image.fromarray(self.ImageShown)
        #self.image = ImageTk.PhotoImage(self.image)

        
if __name__ == "__main__":
    feed = MainWindow(cv.VideoCapture(0))
    feed.run()