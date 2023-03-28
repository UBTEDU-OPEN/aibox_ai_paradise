#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_camera.py
# Created   : 2021/7/8 10:55
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#

import os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal,Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget,QLabel,QStackedLayout, QGridLayout
from clickable_label import UClickableLabel
from scale_view import ScaleView

CAMERA_WIDTH,CAMERA_HEIGHT=1024,576

class SmartPhotoStudioCamera(QWidget):

    captureStatusChangeSignal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setAutoFillBackground(True)
        self._setup_layout()
        self.setStyleSheet("QWidget{background-color:transparent}")

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

    def _setup_layout(self):

        self.contentLayout = QStackedLayout()


        self.setFixedSize(CAMERA_WIDTH, CAMERA_HEIGHT)

        self.camera = ScaleView()
        self.camera.updateFrame(CAMERA_WIDTH, CAMERA_HEIGHT)

        bg = QWidget()
        bg.setStyleSheet("QWidget{background-color:red}")
        bgLayout = QGridLayout()
        bgLayout.setContentsMargins(0,0,0,0)

        self.bgImage = QLabel()
        self.bgImage.setScaledContents(True)
        self.bgImage.setFixedSize(CAMERA_WIDTH, CAMERA_HEIGHT)
        self.bgImage.setStyleSheet("QWidget{background-color:green}")

        bgLayout.addWidget(self.bgImage, 0, 0, 1, 1)

        bgLayout.addWidget(self.camera, 0, 0, 1, 1)

        bgLayout.setContentsMargins(0,0,0,0)
        bg.setLayout(bgLayout)

        self.contentLayout.addWidget(bg)

        self.preview = PreviewView(self)
        # self.preview.setScaledContents(True)
        self.preview.updateFrame(CAMERA_WIDTH, CAMERA_HEIGHT)
        self.preview.closeSignal.connect(self.show_preview)

        self.contentLayout.addWidget(self.preview)

        self.setLayout(self.contentLayout)

    def update_camera(self, pixmap):
        # self.camera.setPixmap(pixmap)
        # self.camera.setImage(pixmap)
        # newImage = pixmap.scaled(CAMERA_WIDTH, CAMERA_HEIGHT, Qt.KeepAspectRatio)
        self.camera.setImage(pixmap)

    def update_bg(self, image):

        newImage = image.scaled(CAMERA_WIDTH,CAMERA_HEIGHT,Qt.KeepAspectRatio)
        self.bgImage.setPixmap(newImage)
        # self.preview.resize(image.width(), image.height())

    def show_preview(self):
        count = self.contentLayout.count()
        index = self.contentLayout.currentIndex()
        index = index + 1
        if index >= count:
            index = 0

        if index == 1:
            self.camera.icon.beginCapture()
            pixmap = self.grab(QRect(0,0, self.width(), self.height()))
            self.preview.setImage(pixmap)
        else:
            self.camera.icon.endCapture()


        self.contentLayout.setCurrentIndex(index)

        self.capture_enalbed = index == 0

        self.captureStatusChangeSignal.emit(self.capture_enalbed)

# 预览
class PreviewView(QWidget):

    closeSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(PreviewView, self).__init__(parent)

        self.icon = QLabel(self)

        self.icon.show()
        self.icon.setStyleSheet("QWidget{background-color:cyan}")

        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_close1.png")
        icon_press_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_close1.png")

        self.closeBtn = UClickableLabel(parent=self, normal_pixmap=QPixmap(icon_path), pressed_pixmap=QPixmap(icon_press_path))
        self.closeBtn.clicked.connect(self._click_close_btn)

        self.closeBtn.show()

        self.setStyleSheet("QWidget{background-color:transparent}")

    def updateFrame(self, ww, hh):
        self.setFixedSize(ww, hh)
        self.icon.setFixedSize(ww, hh)
        self.icon.move(0, 0)

        self.closeBtn.setFixedSize(40, 40)
        self.closeBtn.move(ww - 40 - 20, 20)

    def setImage(self, pixmap):
        self.icon.setPixmap(pixmap)

    def _click_close_btn(self):
        self.closeSignal.emit()


