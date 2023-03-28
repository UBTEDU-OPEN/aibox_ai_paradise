#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_camera.py
# Created   : 2021/7/12 13:55
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import os

from PyQt5.QtGui import QPainter, QColor, QPen, QBitmap, QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize, QPoint
import threading


class ScaleView(QWidget):
    def __init__(self, parent=None):
        super(ScaleView, self).__init__(parent)

        self.setStyleSheet("QWidget{background-color:transparent}")
        self.icon = ScaleIcon(self)
        self.icon.show()

    def updateFrame(self, ww, hh):
        w, h = 320, 320
        self.setFixedSize(ww, hh)
        self.icon.updateFrame(w, h)
        self.icon.move((ww - w) / 2, hh - h)

    def setImage(self, pixmap):
        # self.icon.initial_image = pixmap
        self.icon.setImage(pixmap)
        pass


LeftTop, RightTop, LeftBottom, RightBottom = range(4)
MINIMUN_WIDTH, MINIMUN_HEIGHT = 160, 160


class ScaleIcon(QLabel):
    Margins = 20
    Capturing = False

    def __init__(self, parent=None):
        super(ScaleIcon, self).__init__(parent)

        self.Direction = None

        self._lock = threading.Lock()
        self._move_drag = False
        self._pressed = False
        self.initial_image = None
        # icon_press_path = os.path.join(os.path.dirname(__file__), "resource/images", "abc123456.png")
        # self.initial_image = QPixmap(icon_press_path)
        self.Capturing = False

        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QWidget{background-color:transparent}")

        self._init_scale_btn()

    def _init_scale_btn(self):

        self.move_btn = QLabel(self)
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_move.png")
        self.move_btn.setPixmap(QPixmap(icon_path))
        self.move_btn.hide()

        self.left_top = QLabel(self)
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_left_big.png")
        self.left_top.setPixmap(QPixmap(icon_path))
        self.left_top.hide()

        self.left_bottom = QLabel(self)
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_right_big.png")
        self.left_bottom.setPixmap(QPixmap(icon_path))
        self.left_bottom.hide()

        self.right_top = QLabel(self)
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_right_big.png")
        self.right_top.setPixmap(QPixmap(icon_path))
        self.right_top.hide()

        self.right_bottom = QLabel(self)
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_left_big.png")
        self.right_bottom.setPixmap(QPixmap(icon_path))
        self.right_bottom.hide()

    def updateFrame(self, ww, hh):
        self.setFixedSize(ww, hh)
        w, h = 40, 40
        self.move_btn.setFixedSize(w, h)
        self.left_top.setFixedSize(w, h)
        self.left_bottom.setFixedSize(w, h)
        self.right_top.setFixedSize(w, h)
        self.right_bottom.setFixedSize(w, h)

        self.move_btn.move((ww - w) / 2, (hh - h) / 2)
        self.left_top.move(-w / 2, -h / 2)
        self.left_bottom.move(-w / 2, hh - h / 2)
        self.right_top.move(ww - w / 2, -h / 2)
        self.right_bottom.move(ww - w / 2, hh - h / 2)

        if self._pressed:
            if self._move_drag:
                self.move_btn.show()

                self.left_top.hide()
                self.left_bottom.hide()
                self.right_top.hide()
                self.right_bottom.hide()
            else:
                self.move_btn.hide()

                self.left_top.hide()
                self.left_bottom.hide()
                self.right_top.hide()
                self.right_bottom.hide()

                if self.Direction == LeftTop:  # 左上角
                    self.left_top.show()
                elif self.Direction == RightBottom:  # 右下角
                    self.right_bottom.show()
                elif self.Direction == RightTop:  # 右上角
                    self.right_top.show()
                elif self.Direction == LeftBottom:  # 左下角
                    self.left_bottom.show()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        w, h = self.width(), self.height()
        size = QSize(w, h)
        # mask = QBitmap(size)
        painter = QPainter(self)

        if self.initial_image is not None:
            newImage = self.initial_image.scaled(size, Qt.KeepAspectRatio)
            painter.drawPixmap(0, 0, size.width(), size.height(), newImage)
            # newImage.setMask(mask)

        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # painter.fillRect(0, 0, size.width(), size.height(), Qt.white)
        # painter.setBrush(QColor(0, 0, 0))
        if not self.Capturing:
            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            painter.drawRoundedRect(0, 0, size.width(), size.height(), 16, 16, Qt.AbsoluteSize)

        painter.end()

    def setImage(self, pixmap):
        self.initial_image = pixmap
        # newImage = self.initial_image.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        # self.setPixmap(newImage)
        self.repaint()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if (a0.button() == Qt.LeftButton):
            self._pressed = True
            self._mpos = a0.pos()
            pos = a0.pos()
            xPos, yPos = pos.x(), pos.y()
            wm, hm = self.width() - self.Margins, self.height() - self.Margins

            self._move_drag = False

            if xPos < self.Margins and yPos < self.Margins:
                # 左上角
                self.Direction = LeftTop
            elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
                # 右下角
                self.Direction = RightBottom
            elif wm <= xPos and yPos <= self.Margins:
                # 右上角
                self.Direction = RightTop
            elif xPos <= self.Margins and hm <= yPos:
                # 左下角
                self.Direction = LeftBottom
            else:
                self.move_DragPosition = a0.globalPos() - self.pos()
                self._move_drag = True

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self._pressed:
            if self._move_drag:
                pos = a0.globalPos() - self.move_DragPosition
                geometry = self.geometry()
                x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
                limited_margin_x = w / 3
                limited_maargin_y = h / 3
                ww, hh = self.parent().geometry().width(), self.parent().geometry().height()
                xx = min(ww - w + limited_margin_x, max(-limited_margin_x, pos.x()))
                yy = min(hh - h + limited_maargin_y, max(-limited_maargin_y, pos.y()))
                self.move(xx, yy)
                self.show()
            else:
                self._resizeWidget(a0.pos())
                pass
        else:
            self.updateDisplay(a0.pos())
            pass

    def _resizeWidget(self, pos):
        if self.Direction == None:
            return

        self._lock.acquire()

        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        ww, hh = self.parent().geometry().width(), self.parent().geometry().height()
        limited_margin = 0


        desti_width = 0

        if self.Direction == LeftTop:  # 左上角

            xPos = max(xPos, yPos)
            yPos = max(xPos, yPos)
            if w - xPos > MINIMUN_WIDTH and x + xPos >= limited_margin:
                x += xPos
                w -= xPos
            if h - yPos > MINIMUN_HEIGHT and y + yPos >= limited_margin:
                y += yPos
                h -= yPos
            d = max(MINIMUN_WIDTH,min(w,h))
            self.setFixedSize(d, d)
            self.move(x, y)
            desti_width = d

        elif self.Direction == RightBottom:  # 右下角
            dest_w,dest_h = 0,0
            if w + xPos >= MINIMUN_WIDTH and x + w + xPos <= ww - limited_margin:
                dest_w = w + xPos
                self._mpos.setX(pos.x())
            else:
                print('rb x error')
            if h + yPos >= MINIMUN_HEIGHT and y + h + yPos <= hh - limited_margin:
                dest_h = h + yPos
                self._mpos.setY(pos.y())
            else:
                print('rb y error')

            # 最终拉伸后的最小宽高
            dest = max(MINIMUN_WIDTH,min(dest_w, dest_h))

            # self._mpos.setX(xPos - (w + xPos - dest))
            # self._mpos.setY(yPos - (h + yPos - dest))
            # self._mpos = QPoint(xPos - (w + xPos - dest), yPos - (h + yPos - dest))
            self.setFixedSize(dest, dest)
            self.move(x, y)
            desti_width = dest

        elif self.Direction == RightTop:  # 右上角
            dest_w, dest_h = 0, 0
            if h - yPos >= MINIMUN_HEIGHT and y + yPos >= limited_margin:
                # y += yPos
                # h -= yPos
                dest_h = h - yPos
            if w + xPos >= MINIMUN_WIDTH and x + w + xPos <= ww - limited_margin:
                # w += xPos
                dest_w = w + xPos
                self._mpos.setX(pos.x())
            dest = max(MINIMUN_HEIGHT,min(dest_w, dest_h))
            self.setFixedSize(dest, dest)
            self.move(x,y+h-dest)
            desti_width = dest

        elif self.Direction == LeftBottom:  # 左下角
            dest_w, dest_h = 0, 0
            if w - xPos >= MINIMUN_WIDTH and x + xPos >= limited_margin:
                # x += xPos
                # w -= xPos
                dest_w = w - xPos
            else:
                print('x error')
            if h + yPos >= MINIMUN_HEIGHT and y + h + yPos <= hh - limited_margin:
                # h += yPos
                dest_h = h + yPos
                # self._mpos.setY(pos.y())
            else:
                print('y error')

            # 最终拉伸后的最小宽高
            dest = max(MINIMUN_HEIGHT,min(dest_w, dest_h))
            self.setFixedSize(dest, dest)
            self.move(x+w-dest, y)
            self._mpos.setX(xPos - (w + xPos - dest))
            self._mpos.setY(pos.y())

            desti_width = dest

        # print(xPos, yPos)
        w1, h1 = 40, 40
        self.move_btn.move((desti_width - w1) / 2, (desti_width - h1) / 2)
        self.left_top.move(-w1 / 2, -h1 / 2)
        self.left_bottom.move(-w1 / 2, desti_width - h1 / 2)
        self.right_top.move(desti_width - w1 / 2, -h1 / 2)
        self.right_bottom.move(desti_width - w1 / 2, desti_width - h1 / 2)
        self._lock.release()

        # self.move(x,y)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:

        # if self._move_drag:
        #     pass
        # else:
        #     self._resizeWidget(a0.pos())

        self._move_drag = False
        self._pressed = False
        self.Direction = None

    def updateDisplay(self, pos):
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins

        self.move_btn.hide()
        self.left_top.hide()
        self.left_bottom.hide()
        self.right_top.hide()
        self.right_bottom.hide()

        if xPos < self.Margins and yPos < self.Margins:
            # 左上角
            self.left_top.show()
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.right_bottom.show()
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.right_top.show()
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.left_bottom.show()
        else:
            self.move_btn.show()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.move_btn.hide()
        self.left_top.hide()
        self.left_bottom.hide()
        self.right_top.hide()
        self.right_bottom.hide()

    def beginCapture(self):
        self.Capturing = True
        self.repaint()

    def endCapture(self):
        self.Capturing = False
        self.repaint()
