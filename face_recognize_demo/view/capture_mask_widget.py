# This Python file uses the following encoding: utf-8
from PyQt5 import QtGui
from PyQt5.QtWidgets import  QWidget, QLabel,QStyle,QStyleOption
from PyQt5.QtGui import QFont,QPainter,QColor,QBrush,QGuiApplication
from PyQt5.QtCore import QTimer
from enum import Enum

from face_recognize_demo.com import ubt_device


class PhotoBackgroundWidget(QWidget):

    class Status(Enum):
        NO_FACE = 1
        KNOWN_FACE = 2
        UNKNOWN_FACE = 3

    def paintEvent(self, event):
        # print(self.status_label.width())


        painter = QPainter()
        painter.begin(self)

        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        painter.end()

    def __init__(self,parent):
        super(PhotoBackgroundWidget, self).__init__(parent)

        self.initUI()

        self.index = 0

        self.setAnimationBackground()

    def initUI(self):
        self.status_label = QLabel(self)
        self.status_label.setGeometry(96 * ubt_device.scale_width, 33 * ubt_device.scale_height, 455 * ubt_device.scale_width, 447 * ubt_device.scale_height)
        statu_pixmap = QtGui.QPixmap()
        self.status_label.setPixmap(statu_pixmap)
        self.status_label.setScaledContents(True)


    def setAnimationBackground(self):
        self.setObjectName("take_ptoto_widget")
        style = str("QWidget#take_ptoto_widget{border-image: url(:/resource/photo_bg_res/take_photo_0.png)}")
        self.setStyleSheet(style)

        self.timer = QTimer()
        self.timer.start(40)
        self.timer.timeout.connect(self.timeoutAciton)

    def timeoutAciton(self):
        url = ":/resource/photo_bg_res/take_photo_%s.png" % str(self.index)

        style = str("QWidget#take_ptoto_widget{border-radius: 8px;background-color:transparent;border-image: url(%s)}" % url)

        self.setStyleSheet(style)

        self.index = self.index + 1

        if self.index > 100:
            self.index = 0

    def setStatus(self, status):
        if self.Status.NO_FACE == status:
            status_pixmap = QtGui.QPixmap()
        elif self.Status.KNOWN_FACE == status:
            status_pixmap = QtGui.QPixmap(":/resource/img_photo_red.png")
        else:
            status_pixmap = QtGui.QPixmap(":/resource/img_photo_green.png")

        self.status_label.setPixmap(status_pixmap)


