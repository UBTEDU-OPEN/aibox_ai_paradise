#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:canvas.py
# Created:2020/9/15 下午5:25
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
import sys
import os
import math
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt

from R import R

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtGui import QPixmap, QColor, QPainter, QCursor, QPainterPath
from PyQt5.QtWidgets import QLabel


class Canvas(QLabel):
    change_signal = QtCore.pyqtSignal()

    def __init__(self, icon):
        super().__init__()
        self.setFixedSize(QSize(640, 480))
        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000')
        self.tracks = []
        self.last_track = None

        self.curr_icon = os.path.join(os.path.dirname(os.path.dirname(__file__)), icon)
        canvas = QPixmap(self.curr_icon)
        canvas = canvas.scaled(640, 480)
        self.setPixmap(canvas)

        # add mask
        mask = QLabel(self)
        pix = QPixmap(R.imgs_ic_bottom_round_border)
        mask.setPixmap(pix)

        self.can_draw = True

    def set_can_draw(self, flag):
        self.can_draw = flag

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def select(self, resId):
        self.curr_icon = os.path.join(os.path.dirname(os.path.dirname(__file__)), resId)
        canvas = QPixmap(self.curr_icon)
        canvas = canvas.scaled(640, 480)
        self.setPixmap(canvas)
        self.notify()
        self.tracks.clear()
        self.change_signal.emit()

    def can_revoke(self):
        if self.tracks:
            return True
        else:
            return False

    def revoke(self):
        canvas = QPixmap(self.curr_icon)
        canvas = canvas.scaled(640, 480)
        self.setPixmap(canvas)
        if self.tracks:
            self.tracks.pop()
            for track in self.tracks:
                if track is not None:
                    for pos in track:
                        self.do_draw_paint(pos[0], pos[1])
            self.notify()

    def enterEvent(self, ev):
        if self.can_draw:
            # self.setCursor(Qt.CrossCursor)
            self.setCursor(QCursor(QPixmap(R.imgs_img_pen), -1, -1))
        else:
            self.setCursor(Qt.ArrowCursor)
    # def mousePressEvent(self, event):
    #     self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, *args, **kwargs):
        """
        松开鼠标事件
        """
        self.last_x, self.last_y = None, None
        self.tracks.append(self.last_track)
        self.last_track = None
        self.change_signal.emit()
        # self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, e):
        """
        移动鼠标事件
        """
        if not self.can_draw:
            return
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            self.last_track = []
            return

        self.do_draw_paint(self.pen_color, (self.last_x, self.last_y, e.x(), e.y()))
        self.notify()

        if self.last_track is not None:
            self.last_track.append((self.pen_color, (self.last_x, self.last_y, e.x(), e.y())))

        # update the origin for next time
        self.last_x = e.x()
        self.last_y = e.y()

    def do_draw_paint(self, pen_color, pt):
        """
        绘图
        """
        painter = QPainter(self.pixmap())
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = painter.pen()
        pen.setWidth(9)
        pen.setColor(pen_color)
        painter.setBrush(pen_color)
        painter.setPen(pen)

        # drawLine
        # painter.drawLine(pt[0], pt[1], pt[2], pt[3])

        # drawCircle
        # pen.setWidth(9)
        # painter.setPen(pen)
        # painter.drawEllipse(pt[0] - 6, pt[1] - 6, 12, 12)
        # painter.drawEllipse(pt[2] - 6, pt[3] - 6, 12, 12)
        x1 = pt[0]
        y1 = pt[1]
        x2 = pt[2]
        y2 = pt[3]
        p_list = self.get_dot_list(x1, y1, (x1 + x2) / 2, (y1 + y2) / 2, x2, y2)
        # 轨迹上画连续的实心圆
        for p in p_list:
            painter.drawEllipse(p[0] - 10, p[1] - 10, 20, 20)

        # drawRoundedRect
        # w = abs(pt[2] - pt[0])
        # h = abs(pt[3] - pt[1])
        # x_off = 5 if pt[2] > pt[0] else -5
        # y_off = 10 if pt[3] > pt[1] else -10
        # painter.drawRoundedRect(pt[0] - x_off, pt[1] - y_off, w + 20, h + 25, 99, 99)
        
        # painter.drawRoundedRect(pt[0] - 5, pt[1] - 10, pt[2] - pt[0], pt[3] - pt[1], 99, 99)

        # draw quad
        # path = QPainterPath()
        # pen.setWidth(15)
        # painter.setPen(pen)
        # x1 = pt[0]
        # y1 = pt[1]
        # x2 = pt[2]
        # y2 = pt[3]
        # path.moveTo(x1, y1)
        # # path.quadTo(pt[0], pt[1], (pt[2] + pt[0]) / 2, (pt[3] + pt[1]) / 2)
        # # draw cubic
        # path.cubicTo((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, x2, y2)
        # painter.drawPath(path)

        painter.end()

    def get_dot_list(self, x1, y1, x2, y2, x3, y3):
        """
        获取目标点的轨迹，返回轨迹点的坐标集合
        """
        dist = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
        if dist <= 30:
            dots_num = 5
        elif dist >= 100:
            dots_num = 30
        else:
            dots_num = int(dist / 3)
        p_list = []
        x_dots12 = np.linspace(x1, x2, dots_num)
        y_dots12 = np.linspace(y1, y2, dots_num)
        x_dots23 = np.linspace(x2, x3, dots_num)
        y_dots23 = np.linspace(y2, y3, dots_num)
        for i in range(dots_num):
            x = x_dots12[i] + (x_dots23[i] - x_dots12[i]) * i / (dots_num - 1)
            y = y_dots12[i] + (y_dots23[i] - y_dots12[i]) * i / (dots_num - 1)
            p_list.append((int(x), int(y)))
        return p_list

    def notify(self):
        self.update()
        self.change_signal.emit()
