import numpy as np
from enum import Enum
import math

DOWN_VECTOR = np.array([0, 1])
SPEED_DIRECTION_THRESHOLD = 25

class BallState(Enum):
    Launch = 1
    Bounce = 2
    Hit = 3
    Miss = 4

class Track():
    def __init__(self, pos, radius, speed=np.zeros(2), direction=DOWN_VECTOR, hitPoint=np.zeros(2), ballState=BallState.Launch):
        self.pos = np.array(pos)
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.hitPoint = hitPoint
        self.ballState = ballState

    def getPos(self):
        return self.pos

    def getRadius(self):
        return self.radius


class Tracks():
    Y_DIRECTION_THRESHOLD = 10  # in pixel

    def __init__(self, gameParameter, maxLength=200):
        self.history = []
        self.maxLength = maxLength
        self.gameParameter = gameParameter

    def append(self, newTrack):
        if len(self.history) > self.maxLength:
            self.history.pop(0)
        self.history.append(newTrack)

        # CALCULATION
        self.calculateCurrentSpeed()
        self.calculateBallDirection(self.gameParameter.numPredictFrame)

    def getTrackAt(self, index):
        if len(self.history) == 0:
            return None
        if index < -1 or index >= len(self.history):
            return None

        return self.history[index]

    def getLastTrack(self):
        return self.getTrackAt(-1)

    def isBallInGame(self, pos):
        yOpponent, yRobot = self.gameParameter.getPlayerZone()
        # ball in player zone
        if pos[1] < yOpponent or pos[1] > yRobot:
            return False

        # ball in game (table zone)
        # pos[1] >= yOpponent and y[1] <= yRobot
        return True

    def getBallState(self):
        if len(self.history) < 1:
            return BallState.Unknown

        return self.history[-1].ballState

    def getFrameToHit(self):
        if len(self.history) < 15:
            return -1

        pos = self.history[-1].pos

        # speed = latest known positive y speed
        speed = np.zeros(2)
        maxSeekFrame = 10
        foundPositiveYSpeed = False
        for i in range(maxSeekFrame):
            s = self.history[-1-i].speed
            if s[1] > 0:
                foundPositiveYSpeed = True
                speed = s.copy()
                break
        if not foundPositiveYSpeed:
            return -1        

        yOpponent, yRobot = self.gameParameter.getPlayerZone()
        time = (yRobot - pos[1]) / np.linalg.norm(speed)

        return time
    
    def getHitPoint(self):
        for i in range(len(self.history)-1, 0, -1):
            if self.history[i].hitPoint[0] != 0:
                return self.history[i].hitPoint

        return np.zeros(2)


    def calculateCurrentSpeed(self):
        if len(self.history) < 2:
            return np.zeros(2)

        t1 = self.history[-2].pos
        t2 = self.history[-1].pos
        speed = np.subtract(t2, t1) 
        self.history[-1].speed = speed

        return speed
        
    def calculateBallDirection(self, numFrames):
        if len(self.history) < numFrames:
            self.history[-1].direction = np.zeros(2)
            return 

        d = np.zeros(2)
        for i in range(numFrames):
            d += self.history[-1-i].speed
        
        # Unstable result when sum speed vector is smaller than threshold
        d_norm = np.linalg.norm(d)
        if d_norm < SPEED_DIRECTION_THRESHOLD*numFrames:
            self.history[-1].direction = np.copy(self.history[-2].direction)
            return
        
        d = d / d_norm
        diviation = np.dot(DOWN_VECTOR, d)

        # Up
        if diviation < 0:
            self.history[-1].direction = np.copy(self.history[-2].direction)

        # Down
        else:
            self.history[-1].direction = d

