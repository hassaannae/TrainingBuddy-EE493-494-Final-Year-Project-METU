from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout, QTabWidget, QComboBox
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

# MY LIB
from VideoThread import VideoThread
from ImageProcessor import BallTracker, ImageProcessor
from track import BallState

# MY WIDGET
from Widget.FrameControl import FrameControl
from Widget.RoiControl import RoiControl
from Widget.BallControl import BallControl
from Widget.GameControl import GameControl


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pingpong ball detection")
        self.setFixedSize(1440, 810)

        self.image_label = QLabel(self)
        self.imageProcessor = BallTracker("480res")
        self.videoThread = VideoThread(self.imageProcessor, file = "Video/res-test/480p-25fps.mp4")
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        self.videoThread.start()

        self.frameControl = FrameControl(self.videoThread)

        # SETTING TAB
        self.roiControl = RoiControl(self.videoThread)
        self.ballControl = BallControl(self.videoThread)
        self.gameControl = GameControl(self.videoThread)

        self.settingTab = QTabWidget()
        self.settingTab.addTab(self.gameControl, "Game")
        self.settingTab.addTab(self.roiControl, "Roi")
        self.settingTab.addTab(self.ballControl, "Ball")

        # RESULT
        resultLayout = QVBoxLayout()

        self.radAndPosTab = QLabel("Radius - Position")
        self.radAndPosTab.setAlignment(Qt.AlignLeft)
        self.radAndPosTab.setStyleSheet("font-weight: bold; font-size: 22px")
        resultLayout.addWidget(self.radAndPosTab)
        self.radiusAndPos = QLabel("-")
        self.radiusAndPos.setAlignment(Qt.AlignCenter)
        self.radiusAndPos.setStyleSheet("font-weight: bold; font-size: 18px")
        self.radiusAndPos.setFixedHeight(80)
        resultLayout.addWidget(self.radiusAndPos)

        """self.predTab = QLabel("Predicted Radius - Position")
        self.predTab.setAlignment(Qt.AlignLeft)
        self.predTab.setStyleSheet("font-weight: bold; font-size: 22px")
        resultLayout.addWidget(self.predTab)
        self.pred = QLabel("-")
        self.pred.setAlignment(Qt.AlignCenter)
        self.pred.setStyleSheet("font-weight: bold; font-size: 18px")
        self.pred.setFixedHeight(80)
        resultLayout.addWidget(self.pred)"""

        self.ballSpeedTab = QLabel("Ball Speed")
        self.ballSpeedTab.setAlignment(Qt.AlignLeft)
        self.ballSpeedTab.setStyleSheet("font-weight: bold; font-size: 22px")
        resultLayout.addWidget(self.ballSpeedTab)
        self.ballSpeed = QLabel("-")
        self.ballSpeed.setAlignment(Qt.AlignCenter)
        self.ballSpeed.setStyleSheet("font-weight: bold; font-size: 18px")
        self.ballSpeed.setFixedHeight(80)
        resultLayout.addWidget(self.ballSpeed)

        self.stateTab = QLabel("Ball State")
        self.stateTab.setAlignment(Qt.AlignCenter)
        self.stateTab.setStyleSheet("font-weight: bold; font-size: 22px")
        resultLayout.addWidget(self.stateTab)
        self.state = QLabel("-")
        self.state.setAlignment(Qt.AlignCenter)
        self.state.setFixedHeight(120)
        resultLayout.addWidget(self.state)

        # CONTROL PANEL
        controlPanelLayout = QVBoxLayout()
        controlPanelLayout.addWidget(self.frameControl)
        controlPanelLayout.addWidget(self.settingTab)
        controlPanelLayout.addLayout(resultLayout)
        controlPanelLayout.addWidget(QWidget())

        self.controlPanel = QWidget()
        self.controlPanel.setLayout(controlPanelLayout)
        self.controlPanel.setFixedWidth(500)

        # MAIN LAYOUT
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.image_label)
        mainLayout.addWidget(self.controlPanel)

        self.setLayout(mainLayout)

    def closeEvent(self, event):
        self.videoThread.stop()
        event.accept()

    # FUNCTION

    def updateRadiusAndPos(self):
        if self.imageProcessor.tracks.getLastTrack() == None:
            return None
        q = self.imageProcessor.tracks.getLastTrack().getPos()
        s = self.imageProcessor.tracks.getLastTrack().getRadius()
        self.radiusAndPos.setText("Radius: {:.2f} - Pos: {:.2f}, {:.2f}".format(s, q[0], q[1]))

    def updatePred(self):
        if len(self.imageProcessor.predArr) == 0:
            return None
        q = self.imageProcessor.predArr
        print(q)
        self.pred.setText("Pos: {:.2f}, {:.2f}".format(q[0][0], q[0][1]))

    def updateSpeed(self):
        if self.imageProcessor.tracks.getLastTrack() == None:
            return None
        self.ballSpeed.setText("Speed: {:.2f}, {:.2f}".format(self.imageProcessor.tracks.calculateCurrentSpeed()[0], self.imageProcessor.tracks.calculateCurrentSpeed()[1]))

    def updateState(self):
        s = self.imageProcessor.ballState
        if s == "HIT":
            color = "green"
        elif s == "MISS":
            color = "red"
        else:
            color = "transparent"
        
        self.state.setText(s)
        self.state.setStyleSheet(f'background-color: {color}')


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

        self.updateRadiusAndPos()
        self.updateSpeed()
        """self.updatePred()"""
        self.updateState()

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())