from abc import abstractmethod
from sklearn import linear_model
import numpy as np
import cv2
import imutils
import time
import matplotlib.pyplot as plt
from track import Track, Tracks
from kalmanFilter import KalmanFilter


class ImageProcessor():
    @abstractmethod
    def calculate(self):
        pass

class ColorThreshold():
    def __init__(self, h_min=0, h_max=179, s_min=0, s_max=52, v_min=163, v_max=255):
        self.h_min = h_min
        self.h_max = h_max
        self.s_min = s_min
        self.s_max = s_max
        self.v_min = v_min
        self.v_max = v_max

    def getMinValue(self):
        return (self.h_min, self.s_min, self.v_min)

    def getMaxValue(self):
        return (self.h_max, self.s_max, self.v_max)

class GameParameter():
    def __init__(self, opponentZone=20, robotZone=5, numPredictFrame=2, perspective=0):
        self.opponentZone = opponentZone
        self.robotZone = robotZone
        self.numPredictFrame = numPredictFrame
        self.perspective = perspective

        self.imageHeight = 0

    def getPlayerZone(self, imageHeight=None):
        if imageHeight is not None:
            self.imageHeight = imageHeight
        yOpponent = self.imageHeight * float(self.opponentZone)/100
        yRobot = self.imageHeight * (1 - float(self.robotZone)/100)
        return yOpponent, yRobot

class BallTracker(ImageProcessor):
    def __init__(self, data):
        self.roi = [0,0,1,1]
        self.data = data

        if self.data == "dark":
            self.colorThreshold = ColorThreshold(0, 179, 0, 71, 49, 255)
        else:
            self.colorThreshold = ColorThreshold(0, 179, 0, 52, 163, 255)
        
        self.gameParameter = GameParameter()
        self.tracks = Tracks(self.gameParameter)
        self.transformationMatrix = None
        self.width = 10
        self.height = 10
        
        self.frameCount = 0
        self.predArr = []
        self.kf = KalmanFilter()
        self.predicted = self.kf.predict(0,0)
        self.predStore = []
        self.ballState = " "

        
    def calculate(self, frame):
        
        self.height, self.width, c  = frame.shape
        if self.transformationMatrix is None:
            self.updatePerspectiveCorrection()
        frame = cv2.warpPerspective(frame, self.transformationMatrix, (self.width, self.height))
        blurred = cv2.GaussianBlur(frame, (13, 13), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.colorThreshold.getMinValue(), self.colorThreshold.getMaxValue())

        self.frameCount = self.frameCount + 1
        print(self.frameCount)
        if self.frameCount == 1:
            self.firstMask = mask
            time.sleep(0.2)
            
        elif self.frameCount > 2:
            mask = cv2.subtract(mask, self.firstMask)
        
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

         

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            thisTrack = Track( [x,y], radius, 0, 0 )

            self.posX = x
            self.posY = y
            self.tracks.append(thisTrack)
        else: 
            self.posX = 1
            self.posY = 1

        self.predict(frame)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

        return True, frame, mask
    
    def updatePerspectiveCorrection(self):
        v1 = float(self.gameParameter.perspective) / 100 * self.width
        pts1 = np.float32([[0,0],[self.width, 0],[-v1,self.height],[self.width+v1,self.height]])    # current 
        pts2 = np.float32([[0,0],[self.width, 0],[0,self.height],[self.width,self.height]])    # target
        self.transformationMatrix = cv2.getPerspectiveTransform(pts1,pts2)

    def setRoi(self, top, left, bottom, right):
        self.roi = [top, left, bottom, right]

    def setColorThreshold(self, h_min=None, h_max=None, s_min=None, s_max=None, v_min=None, v_max=None):
        if h_min is not None:
            self.colorThreshold.h_min = h_min
        if h_max is not None:
            self.colorThreshold.h_max = h_max
        if s_min is not None:
            self.colorThreshold.s_min = s_min
        if s_max is not None:
            self.colorThreshold.s_max = s_max
        if v_min is not None:
            self.colorThreshold.v_min = v_min
        if v_max is not None:
            self.colorThreshold.v_max = v_max

    def predict(self, frame):
        

        if self.data == "50fps":
            fps50 = [18, 67, 112, 157]
            forward = 10
            offsets = [15, 16, forward+13, forward+7]
            circle = 4
        elif self.data == "dark" or self.data == "lit":
            fps50 = [18, 67, 112, 157]
            forward = 10
            offsets = [15, 16, forward+13, forward+7]
            circle = 4
        elif self.data == "25fps":
            fps50 = [9, 33, 56, 79]
            forward = 5
            offsets = [8, 9, forward+9, forward+5]
            circle = 4
        elif self.data == "10fps":
            fps50 = [3, 13, 22, 32]
            forward = 5
            offsets = [3, 4, forward+1, forward]
            circle = 4
        elif self.data == "720res":
            fps50 = [2, 27, 49, 71]
            forward = 5
            offsets = [10, 11, forward+10, forward+6]
            circle = 4
        elif self.data == "480res":
            fps50 = [2, 27, 49, 71]
            forward = 5
            offsets = [10, 11, forward+10, forward+6]
            circle = 3
        elif self.data == "360res":
            fps50 = [2, 27, 49, 71]
            forward = 5
            offsets = [10, 11, forward+10, forward+6]
            circle = 2


        if self.tracks.getTrackAt(-1) != None and self.frameCount >=fps50[0] and self.frameCount <=(fps50[0]+offsets[0]):
            #self.recordFrames(self.frameCount-71)
            print(self.frameCount)
            print("X: {}, Y: {}".format(self.posX, self.posY))

            self.predicted = self.kf.predict(self.posX, self.posY)
            cv2.circle(frame, (self.predicted[0], self.predicted[1]), 20, (255,0,0), circle)
            print(self.predicted)
        elif self.frameCount == (fps50[0]+offsets[1]):
            self.predictAfter(frame, forward, circle)
        elif self.frameCount > (fps50[0]+offsets[1]) and self.frameCount < (fps50[0]+offsets[2]):
            errorRateX = (self.posX - self.predStore[self.frameCount - (fps50[0]+offsets[3])][0])/self.posX*100
            errorRateY = (self.posY - self.predStore[self.frameCount - (fps50[0]+offsets[3])][1])/self.posY*100
            print("{}, {}".format(errorRateX, errorRateY))
            if abs(errorRateX) > 15 or abs(errorRateY) > 15:
                self.ballState = "HIT"
            else:
                self.ballState = "MISS"
        
        if self.tracks.getTrackAt(-1) != None and self.frameCount >=fps50[1] and self.frameCount <=(fps50[1]+offsets[0]):
            #self.recordFrames(self.frameCount-71)
            print(self.frameCount)
            print("X: {}, Y: {}".format(self.posX, self.posY))

            self.predicted = self.kf.predict(self.posX, self.posY)
            cv2.circle(frame, (self.predicted[0], self.predicted[1]), 20, (255,0,0), circle)
            print(self.predicted)
        elif self.frameCount == (fps50[1]+offsets[1]):
            self.predictAfter(frame, forward, circle)
        elif self.frameCount > (fps50[1]+offsets[1]) and self.frameCount < (fps50[1]+offsets[2]):
            errorRateX = (self.posX - self.predStore[self.frameCount - (fps50[1]+offsets[3])][0])/self.posX*100
            errorRateY = (self.posY - self.predStore[self.frameCount - (fps50[1]+offsets[3])][1])/self.posY*100
            print("{}, {}".format(errorRateX, errorRateY))
            if abs(errorRateX) > 15 or abs(errorRateY) > 15:
                self.ballState = "HIT"
            else:
                self.ballState = "MISS"
        
        if self.tracks.getTrackAt(-1) != None and self.frameCount >=fps50[2] and self.frameCount <=(fps50[2]+offsets[0]):
            #self.recordFrames(self.frameCount-71)
            print(self.frameCount)
            print("X: {}, Y: {}".format(self.posX, self.posY))

            self.predicted = self.kf.predict(self.posX, self.posY)
            cv2.circle(frame, (self.predicted[0], self.predicted[1]), 20, (255,0,0), circle)
            print(self.predicted)
        elif self.frameCount == (fps50[2]+offsets[1]):
            self.predictAfter(frame, forward, circle)
        elif self.frameCount > (fps50[2]+offsets[1]) and self.frameCount < (fps50[2]+offsets[2]):
            errorRateX = (self.posX - self.predStore[self.frameCount - (fps50[2]+offsets[3])][0])/self.posX*100
            errorRateY = (self.posY - self.predStore[self.frameCount - (fps50[2]+offsets[3])][1])/self.posY*100
            print("{}, {}".format(errorRateX, errorRateY))
            if abs(errorRateX) > 15 or abs(errorRateY) > 15:
                self.ballState = "HIT"
            else:
                self.ballState = "MISS"
        
        if self.tracks.getTrackAt(-1) != None and self.frameCount >=fps50[3] and self.frameCount <=(fps50[3]+offsets[0]):
            #self.recordFrames(self.frameCount-71)
            print(self.frameCount)
            print("X: {}, Y: {}".format(self.posX, self.posY))

            self.predicted = self.kf.predict(self.posX, self.posY)
            cv2.circle(frame, (self.predicted[0], self.predicted[1]), 20, (255,0,0), circle)
            print(self.predicted)
        elif self.frameCount == (fps50[3]+offsets[1]):
            self.predictAfter(frame, forward, circle)
        elif self.frameCount > (fps50[3]+offsets[1]) and self.frameCount < (fps50[3]+offsets[2]):
            errorRateX = (self.posX - self.predStore[self.frameCount - (fps50[3]+offsets[3])][0])/self.posX*100
            errorRateY = (self.posY - self.predStore[self.frameCount - (fps50[3]+offsets[3])][1])/self.posY*100
            print("{}, {}".format(errorRateX, errorRateY))
            if abs(errorRateX) > 15 or abs(errorRateY) > 15:
                self.ballState = "HIT"
            else:
                self.ballState = "MISS"
    
    def predictAfter(self, frame, forward, circle):
        for i in range(forward):
            self.predicted = self.kf.predict(self.predicted[0], self.predicted[1])
            self.predStore.append(self.predicted)
            cv2.circle(frame, (self.predicted[0], self.predicted[1]), 20, (0,255,0), circle)
        print(self.predStore)


  

        

        
        