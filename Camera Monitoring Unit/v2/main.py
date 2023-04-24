from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout, QTabWidget
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


# MY LIB
from VideoThread import VideoThread
from ImageProcessor import BallTracker, ImageProcessor
from Track import BallState

# MY WIDGET
from Widget.FrameControl import FrameControl
from Widget.RoiControl import RoiControl
from Widget.BallControl import BallControl
from Widget.GameControl import GameControl

class LaunchParameters():
    def __init__(self, launchSpeed, spin, launchDirection):
        self.launchSpeed = launchSpeed
        self.spin = spin
        self.launchDirection = launchDirection
    def getParams(self):
        return '{self.launchSpeed}, {self.spin}, {self.launchDirection}'.format(self=self)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pingpong Robot Manager")
        self.setFixedSize(1200,900)

        # OBJECT

        # VIDEO DISPLAY
        self.image_label = QLabel(self)
        self.imageProcessor = BallTracker()
        self.videoThread = VideoThread(self.imageProcessor, file = "Video/1.mp4")
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        self.videoThread.start()

        # FRAME CONTROL
        self.frameControl = FrameControl(self.videoThread)

        # SETTING TAB
        self.roiControl = RoiControl(self.videoThread)
        self.ballControl = BallControl(self.videoThread)
        
        

        self.settingTab = QTabWidget()
        self.settingTab.addTab(self.roiControl, "Roi")
        self.settingTab.addTab(self.ballControl, "Ball")


        # RESULT
        resultLayout = QVBoxLayout()

        testQueue = []
        testQueue.append(LaunchParameters("fast", "top-spin", "mid").getParams())
        testQueue.append(LaunchParameters("slow", "back-spin", "mid").getParams())
        testQueue.append(LaunchParameters("fast", "top-spin", "mid").getParams())
        testQueue.append(LaunchParameters("slow", "back-spin", "mid").getParams())

        resultLayout.addWidget(QLabel("Launch Queue:"))
        self.queue = QLabel(str(testQueue))
        self.queue.setStyleSheet("font-size: 10px")
        resultLayout.addWidget(self.queue)
        
        resultLayout.addWidget(QLabel("Ball speed in pixel size:"))
        self.speed = QLabel("_")
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.speed.setFixedHeight(80)
        resultLayout.addWidget(self.speed)

        resultLayout.addWidget(QLabel("Ball direction:"))
        self.direction = QLabel("_")
        self.direction.setAlignment(Qt.AlignCenter)
        self.direction.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.direction.setFixedHeight(60)
        resultLayout.addWidget(self.direction)

        # CONTROL PANEL
        controlPanelLayout = QVBoxLayout()
        controlPanelLayout.addWidget(self.frameControl)
        controlPanelLayout.addWidget(self.settingTab)
        controlPanelLayout.addLayout(resultLayout)
        controlPanelLayout.addWidget(QWidget())

        self.controlPanel = QWidget()
        self.controlPanel.setLayout(controlPanelLayout)
        self.controlPanel.setFixedWidth(300)

        # MAIN LAYOUT
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.image_label)
        mainLayout.addWidget(self.controlPanel)

        self.setLayout(mainLayout)


    def closeEvent(self, event):
        self.videoThread.stop()
        event.accept()

    # FUNCTION

    def updateSpeed(self):
        if len(self.imageProcessor.tracks.history) > 0:
            sp = self.imageProcessor.tracks.getLastTrack().speed
            self.speed.setText(str(sp))

    def updateDirection(self):
        if len(self.imageProcessor.tracks.history) > 1:
            print(self.imageProcessor.tracks.getLastTrack().speed[0])
            if self.imageProcessor.tracks.getLastTrack().speed[0] > 0:
                print("a")
                self.direction.setText("Towards launcher")
                self.direction.setStyleSheet("background-color: green; font-weight: bold; font-size: 12px;")
            elif self.imageProcessor.tracks.getLastTrack().speed[0] <= 0:
                self.direction.setText("Towards player") 
                self.direction.setStyleSheet("background-color: red; font-weight: bold; font-size: 12px;")
            else:
                self.direction.setText("Unknown")


    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # print(self.image_label.width(), self.image_label.height)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    # SLOT
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

        self.updateSpeed()
        self.updateDirection()
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
