#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : clickable_label.py
# Created   : 2020/6/2 8:18 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt,pyqtSignal

class UClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, normal_pixmap = None, pressed_pixmap = None):
        super().__init__(parent)

        self.normal_pixmap = normal_pixmap
        self.pressed_pixmap = pressed_pixmap

        if self.normal_pixmap:
            self.setPixmap(self.normal_pixmap)

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            if self.normal_pixmap:
                self.setPixmap(self.normal_pixmap)
            self.clicked.emit()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            if self.pressed_pixmap:
                self.setPixmap(self.pressed_pixmap)

