#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame


class RotateIcon(QFrame):

    def __init__(self, img, width, height, direction=1, speed=30, step=10):

        super(RotateIcon, self).__init__()

        self.setFixedSize(width, height)

        self.img = img  # 图片

        self.x_pos = width  # x坐标

        self.y_pos = height  # y坐标

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

        pix = QtGui.QPixmap(self.img)

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

