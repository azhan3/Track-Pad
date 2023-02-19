"""
+------------------------------------------------------------------------------------+
| This file contains the bulk of the actual machine learning sections of the program |
| It also contains the majority of basic mouse controls,                             |
| File IO for the machine learning models,                                           |
| Records information of previous frames,                                            |
| Normalizes current information to improve gesture detection capabilities           |
+------------------------------------------------------------------------------------+
"""

# Import necessary packages and modules

import time
import cv2 as cv
import mediapipe as mp
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from pynput.mouse import Button
import pyautogui
import warnings
import pickle
import csv
import json
import src.config as config
from src.Levels import ChangeLevel
from src.config import mouse

# Set the width and height of the camera, and the frame rate

CamWidth, CamHeight = 1920, 1080
smooth = 7
FrameRate = 30

# Ignore all warnings

warnings.filterwarnings('ignore')

# Set the feature range to (0, 1) and create a MinMaxScaler object

scalar = MinMaxScaler(feature_range=(0, 1))


# Define a function that appends the input action to the input list and writes the list to a CSV file

def AddtoCSV(lmListML, action):
    lmListML.append(action)
    with open('train.csv', 'a+', newline='') as write_obj:
        writer = csv.writer(write_obj)
        writer.writerow(lmListML)


# Define a function that reads the CSV file and trains a k-nearest neighbors classifier using the data

def trainModel(Nearest_Neighbors=10):

    # Read in the CSV file as a pandas dataframe

    data = pd.read_csv("train.csv", sep=",", header=0)
    data.head()

    # Extract the action labels from the last column of the dataframe

    y = data.iloc[:, -1]

    # Extract the landmark coordinates from the other columns of the dataframe

    X = data.iloc[:, :21]

    # Rescale the landmark coordinates to the range (0, 1)

    rescaledX = scalar.fit_transform(X)

    # Create a k-nearest neighbors classifier with the specified number of neighbors

    a = KNeighborsClassifier(n_neighbors=Nearest_Neighbors)

    # Train the classifier using the rescaled landmark coordinates and the action labels

    a.fit(rescaledX, y)

    # Return the trained classifier

    return a

# classifier = trainModel()


# Save current trained KNN model as a .pkl file for easy and faster imports

def save_model():
    with open('src/models/knn.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    with open('src/models/scaler.pkl', 'wb') as f:
        pickle.dump(scalar, f)


# Load the trained classifier and scaler from pickle files

def import_models():
    with open('src/models/knn.pkl', 'rb') as f:
        classifier = pickle.load(f)
    with open("src/models/scaler.pkl", "rb") as file:
        scalar = pickle.load(file)
    return classifier, scalar


# Set the trained classifier and scaler

classifier, scalar = import_models()

# Define a function that returns the most frequent element in a list


def FindMostFrequent(List):
    return max(set(List), key=List.count)

# Define the main class for the entire backend of the program


class HandControl(ChangeLevel):
    def __init__(self):
        super().__init__()

        # Create a Mediapipe Hands object

        self.mpHands = mp.solutions.hands

        # Set the distance threshold for recognizing swipes

        self.DistancePixels = 50

        # Set the maximum number of hands to detect

        self.maxHands = 1

        # Create a Mediapipe drawing utilities object

        self.mpDraw = mp.solutions.drawing_utils

        # Set the drawing style for the landmarks

        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Create a Hands object

        self.hands = self.mpHands.Hands(self.maxHands)

        # Initialize variables to store previous and current locations of the hand and index finger

        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.cIndexFingerLocX, self.cIndexFingerLocY = 0, 0
        self.pIndexFingerLocX, self.pIndexFingerLocY = 0, 0

        # Initialize lists to store previous locations of the hand, landmarks and landmarks' distances from a reference point

        self.PreviousLocList = []
        self.lmList = []
        self.lmListML = []

    def Landmarks(self, img):

        # Convert the image to RGB format and process it with Mediapipe's Hand module

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # If hands are detected, draw landmarks and connections on the image

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLMS, self.mpHands.HAND_CONNECTIONS)
        return img


    def findLm(self, img):

        # Initialize empty lists for landmark coordinates, landmark distances from a reference point and x,y coordinates of landmarks

        self.lmList = []
        self.lmListML = []
        xList = []
        yList = []

        # Check if there are any detected hands in the image
        
        if self.results.multi_hand_landmarks:

            # Select the first detected hand

            handLMS = self.results.multi_hand_landmarks[0]

            # Loop over all landmarks in the selected hand

            for id, lm in enumerate(handLMS.landmark):

                # Get the height, width, and channel count of the image

                h, w, c = img.shape

                # Get the (x, y) pixel coordinates of the current landmark
                
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Append the coordinates to their respective lists

                xList.append(cx)
                yList.append(cy)

                # Append the (x, y) pixel coordinates to the lmList

                self.lmList.append([cx, cy])

                # Calculate the Euclidean distance between the current landmark and the first landmark in the lmList

                self.lmListML.append(
                    math.sqrt(
                        math.pow(cx - self.lmList[0][0], 2) + math.pow(cy - self.lmList[0][1], 2))
                )

            # Get the minimum and maximum (x, y) coordinates from the their respective lists
            
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)

            # Draw a rectangle around the detected hand with a 20 pixel buffer

            cv.rectangle(img, (xmin - 20, ymin - 20),
                         (xmax + 20, ymax + 20), (255, 255, 255), 2)
            
            # Return the lmList containing the (x, y) pixel coordinates of all landmarks in the detected hand

            return self.lmList


    def DrawSwipe(self, img):

        # Check if a swipe is currently detected

        if self.isSwipe:

            # Draw "Swipe" text with a black outline

            cv.putText(img, "Swipe", (10, 250),
                       cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3, cv.LINE_AA)
            
            # Draw "Swipe" text with a white fill

            cv.putText(img, "Swipe", (10, 250), cv.FONT_HERSHEY_SIMPLEX,
                       3, (255, 255, 255), 2, cv.LINE_AA)
            
            # Draw lines connecting each point in the swipe path

            for i in range(len(self.Swipes) - 1):

                # Reverse the x-coordinate to mirror the image

                cv.line(img, (1280 - self.Swipes[i][0], self.Swipes[i][1]), (1280 -
                        self.Swipes[i + 1][0], self.Swipes[i + 1][1]), (255, 255, 255), 5)


    # Moves the mouse based on the hand movement

    def MoveMouse(self):
        # Release the mouse left button
        mouse.release(Button.left)
        # Move the mouse in the opposite direction of hand movement with a factor of 3 times the factor
        # determined by the distance between the thumb and index finger
        mouse.move(- 3 * self.Factor * (self.clocX - self.plocX),
                   3 * self.Factor * (self.clocY - self.plocY))
        config.OKTime = None  # Set the OKTime to None


    # Holds the mouse button down based on the hand movement

    def HoldMouse(self):

        # Hold the left mouse button down

        pyautogui.mouseDown(button='left')

        # Move the mouse in the opposite direction of hand movement with a factor of 2 times the distance factor

        mouse.move(- 2 * self.Factor * (self.clocX - self.plocX),
                   2 * self.Factor * (self.clocY - self.plocY))
        
        # Set the OKTime to None

        config.OKTime = None  


    # Check the predicted hand gesture and execute the corresponding action
    def CheckAction(self, img, PauseOrNot):
        try:
            
            # Calculate the factor based on the distance between the thumb and index finger

            self.Factor = self.DistancePixels / self.lmListML[1]
        except ZeroDivisionError:
            self.Factor = 1.0

        # Scale the hand landmarks based on the calculated factor

        NewList = [i * self.Factor for i in self.lmListML]

        # Use the trained KNN classifier to predict the hand gesture

        y_pred = classifier.predict(scalar.transform([NewList]))

        # Return the corresponding action based on the predicted gesture

        return config.ActionList[y_pred[0]]


    def NewLoc(self, wScr, hScr):

        # Get current and previous x, y coordinates of the tip of the index finger

        x1, y1 = self.lmList[9][0:]
        x2, y2 = self.lmList[8][0:]

        # Map the coordinates of the tip of the index finger to the screen size

        x3 = np.interp(x1, (FrameRate, CamWidth - FrameRate), (0, wScr))
        y3 = np.interp(y1, (FrameRate, CamHeight - FrameRate), (0, hScr))
        x4 = np.interp(x2, (FrameRate, CamWidth - FrameRate), (0, wScr))
        y4 = np.interp(y2, (FrameRate, CamHeight - FrameRate), (0, hScr))

        # Smooth the values of the index finger tip and the cursor location to reduce noise

        self.clocX = round(self.plocX + (x3 - self.plocX) / smooth)
        self.clocY = round(self.plocY + (y3 - self.plocY) / smooth)
        self.cIndexFingerLocX = round(
            self.pIndexFingerLocX + (x4 - self.pIndexFingerLocX) / smooth)
        self.cIndexFingerLocY = round(
            self.pIndexFingerLocY + (y4 - self.pIndexFingerLocY) / smooth)

        # Return the current x and y coordinates of the tip of the index finger

        return x1, y1


    def ChangeLoc(self):

        # Update the previous x and y coordinates of the cursor location and the index finger tip

        self.plocX, self.plocY = self.clocX, self.clocY
        self.pIndexFingerLocX, self.pIndexFingerLocY = self.cIndexFingerLocX, self.cIndexFingerLocY


class MouseMovement:
    def __init__(self):
        
        # Initialize the current time for left-click

        self.currentTimeLeft = time.time()

        # Initialize the current time for right-click

        self.currentTimeRight = time.time()

    def MouseSingleClickLeft(self):

        # Release the left mouse button
        
        mouse.release(Button.left)

        # If the time elapsed since last click is more than 1 second

        if (time.time() - self.currentTimeLeft) > 1:

            # Single click the left mouse button

            mouse.click(Button.left)
            mouse.release(Button.left)

            # Set the current time to the time of the click

            self.currentTimeLeft = time.time()
        config.OKTime = None

    def Pause(self, img):
        
        # Release the left mouse button
        
        mouse.release(Button.left)

        # If the pause time is not set

        if config.OKTime is None:

            # Set the OK time to the current time

            config.OKTime = time.time()

        # If 2 seconds have elapsed since the OK time

        elif config.OKTime + 2 <= time.time():

            # Open the configuration file for reading

            with open('./src/config.json', 'r') as file:

                # Load the configuration data

                config_p = json.load(file)

            # Toggle the pause setting

            config_p['control']['pause'] = not config_p['control']['pause']

            # Open the configuration file for writing

            with open('./src/config.json', 'w') as file:

                # Write the updated configuration data
                json.dump(config_p, file)

            # Reset the OK time

            config.OKTime = None
        else:

            # Display the time elapsed since the OK time on the screen

            cv.putText(img, str(round(time.time() - config.OKTime, 1)), (260, 100), cv.FONT_HERSHEY_SIMPLEX, 3,
                       (0, 0, 0), 3, cv.LINE_AA)
            cv.putText(img, str(round(time.time() - config.OKTime, 1)), (260, 100), cv.FONT_HERSHEY_SIMPLEX, 3,
                       (255, 255, 255), 2, cv.LINE_AA)

    def MouseSingleClickRight(self):

        # Release the left mouse button

        mouse.release(Button.left)

        # If the time elapsed since last click is more than 1 second

        if (time.time() - self.currentTimeRight) > 1:

            # Single click the right mouse button

            mouse.click(Button.right)
            mouse.release(Button.right)

            # Set the current time to the time of the click

            self.currentTimeRight = time.time()
        config.OKTime = None

    def ReleaseMouse(self):

        # Release the left mouse button

        mouse.release(Button.left)

    def ScrollDown(self):

        # Scroll down

        mouse.scroll(0, -.5)

    def ScrollUp(self):

        # Scroll up

        mouse.scroll(0, .5)
