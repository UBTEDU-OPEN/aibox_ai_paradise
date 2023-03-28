#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_camera_widget.py
# Created   : 2020/6/4 4:14 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

class FacemaskCameraWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setStyleSheet("QWidget{background:red}")
        # self.setAutoFillBackground(True)
        self.icon = CameraLabel()

        middleVLayout = QVBoxLayout()
        middleVLayout.addWidget(self.icon, 1)
        middleVLayout.setContentsMargins(0,0,0,0)
        self.setLayout(middleVLayout)

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

class CameraLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_corner.png")
        pix = QPixmap(icon_path)
        label.setPixmap(pix)
        label.resize(pix.width(), pix.height())

        middleVLayout = QVBoxLayout()
        middleVLayout.addWidget(label, 1)
        middleVLayout.setContentsMargins(0,0,0,0)
        self.setLayout(middleVLayout)

    # def paintEvent(self, event):
    #     opt = QtWidgets.QStyleOption()
    #     opt.init(self)
    #     painter = QtGui.QPainter(self)
    #     self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

# def qapp():
#     if QApplication.instance():
#         _app = QApplication.instance()
#     else:
#         _app = QApplication(sys.argv)
#     return _app
#
#
# if __name__ == "__main__":
#     app = qapp()
#     window = FacemaskCameraWidget()
#     window.resize(600, 600)
#     window.show()
#     app.exec_()