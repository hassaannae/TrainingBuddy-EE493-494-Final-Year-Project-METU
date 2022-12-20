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
    def __init__(self, frameRate):
        self.roi = [0,0,1,1]
        self.colorThreshold = ColorThreshold()
        self.gameParameter = GameParameter()
        self.tracks = Tracks(self.gameParameter)
        self.transformationMatrix = None
        self.width = 10
        self.height = 10
        self.frameCount = 0
        self.frameRate = frameRate
        self.kf = KalmanFilter()
        """self.testArr = np.random.randint(64, size=(4,3))"""
        self.predictPoly = np.ones((4, 3), dtype=float)
        
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

        self.drawPlayerZone(frame)    

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
            self.drawSpeedVector(frame)
            self.drawHitLine(frame)

        self.predict(frame)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

        return True, frame, mask
    
    def updatePerspectiveCorrection(self):
        v1 = float(self.gameParameter.perspective) / 100 * self.width
        pts1 = np.float32([[0,0],[self.width, 0],[-v1,self.height],[self.width+v1,self.height]])    # current 
        pts2 = np.float32([[0,0],[self.width, 0],[0,self.height],[self.width,self.height]])    # target
        self.transformationMatrix = cv2.getPerspectiveTransform(pts1,pts2)

    def drawHitLine(self, frame):
        lastTrack = self.tracks.getLastTrack()
        p = lastTrack.pos
        hitPoint = lastTrack.hitPoint
        cv2.line(frame, tuple(p.astype(int)), tuple(hitPoint.astype(int)), (255, 153, 51), 5)

    def drawSpeedVector(self, frame):
        lastTrack = self.tracks.getLastTrack()
        pos = lastTrack.pos
        speed = lastTrack.speed
        endPoint = np.add(pos, speed)
        cv2.line(frame, tuple(pos.astype(int)), tuple(endPoint.astype(int)), (255, 0, 0), 5)

    def drawPlayerZone(self, frame):
        h, w, c  = frame.shape
        yOpponent, yRobot = self.gameParameter.getPlayerZone(h)
        cv2.line(frame, (0, int(yOpponent)), (w, int(yOpponent)), (255, 0, 0), 3)
        cv2.line(frame, (0, int(yRobot)), (w, int(yRobot)), (255, 0, 0), 3)

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
        if self.tracks.getTrackAt(-1) != None and self.frameCount >=68 and self.frameCount <=80:
            #self.recordFrames(self.frameCount-71)
            print(self.frameCount)
            print("X: {}, Y: {}".format(self.posX, self.posY))
            """print(str(self.testArr[1][2]) + " " + str(self.testArr[3][2]) + " " + str(self.testArr[0][1]))
            print(self.testArr)"""
            predicted = self.kf.predict(self.posX, self.posY)
            cv2.circle(frame, (predicted[0], predicted[1]), 20, (255,0,0), 4)
            print(predicted)
  
        
        
    """def recordFrames(self, ind):
        self.predictPoly[ind-1][2] = self.posY
        self.predictPoly[ind-1][1] = self.posX
        self.predictPoly[ind-1][0] = ind
        #print(self.predictPoly[:, 1])
    def polyCoeff(self):
        self.predictX = np.polyfit(self.predictPoly[:, 0], self.predictPoly[:, 1], deg=1)
        self.predictY = np.polyfit(self.predictPoly[:, 0], self.predictPoly[:, 2], deg=2)

        print(self.predictX)
        print(self.predictY)
        
        self.polynX = np.poly1d(self.predictX)
        self.polynY = np.poly1d(self.predictY)
        x_ = np.linspace(1, 8, 8)
        plt.plot(x_, self.polynX(x_))
        plt.plot(x_, self.polynY(x_))
        print(self.polynX(x_))
        plt.show()
        
    def kalmanFilter(self):
        kf = KalmanFilter(dim_x=2, dim_z=2)
        ball_positions = [(self.predictPoly[:,1], self.predictPoly[:,2] )]
        KalmanFilter()"""

        

        
        