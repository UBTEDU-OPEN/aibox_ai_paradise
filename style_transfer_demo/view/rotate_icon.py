#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: zhijun.zhou
Last edited: 2020.09.25
"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame


class RotateIcon(QFrame):

    def __init__(self, img, x_pos, y_pos, direction=1, speed=30, step=10):

        super(RotateIcon, self).__init__()

        self.setFixedSize(72, 72)

        self.img = img  # 图片

        self.x_pos = x_pos  # x坐标

        self.y_pos = y_pos  # y坐标

        self.direction = direction  # 转向

        self.speed = speed  # 转速

        self.step = 10  # 步长

        self.rotate = 0  # 角度

        self.timer = QtCore.QBasicTimer()  # 定时器

        self.timer.start(30, self)

    def play(self):

        # 播放

        self.timer.start(self.speed, self)

    def stop(self):

        # 停止

        self.timer.stop()

    def setDirection(self, arg):

        # 设置转向

        if arg <= 0:

            self.step = - abs(self.step)

        else:

            self.step = abs(self.step)

        self.timer.start(self.speed, self)

    def setSpeed(self, speed):

        # 设置转速

        self.speed = speed

        self.timer.start(speed, self)

    def setStep(self, arg):

        # 设置步长

        self.step = arg

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)

        pix = QtGui.QPixmap(self.img)
        pix.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        painter.translate(self.x_pos / 2, self.y_pos / 2)  # 使图片的中心作为旋转的中心

        painter.rotate(self.rotate)  # 顺时针旋转10°

        painter.translate(-self.x_pos / 2, -self.y_pos / 2)  # 将原点复位

        painter.drawPixmap(0, 0, self.x_pos, self.y_pos, pix)

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            self.rotate += self.step

            if self.rotate > 360:
                self.rotate = 0

            self.update()

        else:

            super(RotateIcon, self).timerEvent(event)

# if __name__ == '__main__':
#     import sys
#
#     app = QApplication(sys.argv)
#     frm = RotatePage("img_loading.png", 72, 72)
#     layout = QHBoxLayout()
#
#
#     wid = QWidget()
#     wid.setLayout(layout)
#     wid.layout().addWidget(frm)
#     wid.resize(300, 300)
#     wid.show()
#
#
#
#     # frm.show()
#
#     sys.exit(app.exec_())