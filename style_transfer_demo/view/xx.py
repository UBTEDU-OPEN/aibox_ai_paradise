#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: semishigure
Website: zetcode.com
Last edited: 2018.03.09
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cgitb
import sys

cgitb.enable(format='text')  # 解决pyqt5异常只要进入事件循环,程序就崩溃,而没有任何提示


class Ball(QObject):
    def __init__(self, pm):
        super().__init__()
        pixmap = pm
        scaledPixmap = pixmap.scaled(72, 72)
        self.animation()

        self.pixmap_item = QGraphicsPixmapItem(scaledPixmap)
        self.pixmap_item.setTransformOriginPoint(36, 36)  # 设置中心为旋转
        self._set_pos(QPointF(72, 72))  # 设置图标的初始位置

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    def _set_rotation(self, angle):
        self.pixmap_item.setRotation(angle.x())  # 旋转度数

    def animation(self):
        self.anim = QPropertyAnimation(self, b'pos')
        self.anim.setDuration(0)
        self.anim.setStartValue(QPointF(70, 72))
        # self.anim.setKeyValueAt(0.3, QPointF(144, 30))
        # self.anim.setKeyValueAt(0.5, QPointF(54, 90))
        # self.anim.setKeyValueAt(0.8, QPointF(240, 250))
        self.anim.setEndValue(QPointF(72, 72))
        self.anim.start()

        self.anim2 = QPropertyAnimation(self, b'rotation')
        self.anim2.setDuration(1000)
        self.anim2.setLoopCount(1000)
        self.anim2.setStartValue(QPointF(0, 1))
        self.anim2.setEndValue(QPointF(360, 1))
        self.anim2.setEasingCurve(QEasingCurve.Linear)

    pos = pyqtProperty(QPointF, fset=_set_pos)
    rotation = pyqtProperty(QPointF, fset=_set_rotation)


class Myview(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setFixedSize(172, 172)
        self._set_color(QColor(255, 0, 0))
        self.iniAnimation()

    def _set_color(self, col):
        self.palette = QPalette()
        # self.palette.setColor(self.backgroundRole(), col)
        self.palette.setBrush(self.backgroundRole(), col)
        self.setPalette(self.palette)

    def iniAnimation(self):
        self.anim3 = QPropertyAnimation(self, b'color')
        self.anim3.setDuration(1000)
        # self.anim3.setStartValue(QColor(105, 105, 105))
        # self.anim3.setKeyValueAt(0.1, QColor(255, 255, 240))
        # self.anim3.setKeyValueAt(0.3, QColor(219, 225, 171))
        # self.anim3.setKeyValueAt(0.7, QColor(148, 214, 184))
        # self.anim3.setEndValue(QColor(86, 199, 170))

    color = pyqtProperty(QColor, fset=_set_color)


class RotateLabel(Myview):

    def __init__(self, pm):
        super().__init__()
        self.pm = pm
        self.initView()

    def initView(self):
        self.ball = Ball(self.pm)
        self.scene = QGraphicsScene(self)
        # self.scene.setSceneRect(0, 0, 72, 72)
        self.scene.addItem(self.ball.pixmap_item)
        self.setScene(self.scene)

        self.setRenderHint(QPainter.Antialiasing)
        self.setGeometry(0, 0, 72, 72)
        self.show()

    def runAnim(self):
        self.ball.anim2.start()
