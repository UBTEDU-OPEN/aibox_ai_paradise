#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:popwindow.py
# Created:2020/6/2 上午10:43
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from gallery import Ui_Gallery

BUBBLE_POSITION = (782, 114)
BUBBLE_SIZE = (273, 298)


class GalleryWindow(QWidget, Ui_Gallery):

    def __init__(self, anchor: QLabel, size=BUBBLE_SIZE, parent=None):
        super(GalleryWindow, self).__init__(parent)
        self.setupUi(self)
        self.anchor = anchor
        self.size = size
        self.pos = BUBBLE_POSITION
        # self.anchor.clicked.connect(self.show_pop)
        self.isShow = False
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        # self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.init_ui()

        # self.pop.setGeometry(777, 117, *size)
        # self.show()
        self.hide()
        self.pop.setStyleSheet("QWidget{background-color:transparent}")
        self.installEventFilter(self)

    def init_ui(self):
        # self.content.setStyleSheet()
        self.arrow.setStyleSheet("QLabel{background-color:transparent}")
        self.arrow.setPixmap(
            QPixmap(os.path.join(os.path.dirname(__file__), "resource/images", "ic_arrow_up_bubble.png")))

        qssFile = os.path.join(os.path.dirname(__file__) + '/resource/qss/style.qss')
        with open(qssFile) as fp:
            qss = fp.read()
            self.setStyleSheet(qss)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        anchor_pos = self.anchor.mapToGlobal(QtCore.QPoint(0, 0))

        self.pop.setGeometry(anchor_pos.x() - self.size[0] / 2 + self.anchor.width() / 2,
                             anchor_pos.y() + self.anchor.height(), *self.size)

    def show_pop(self):
        if self.isShow:
            self.hide()
            self.isShow = False
        else:
            self.show()
            self.isShow = True

    def eventFilter(self, ob: QtCore.QObject, event: QtCore.QEvent):
        if ob == self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.hide()
                self.isShow = False
                event.accept()
                return True

        return QWidget.eventFilter(self, ob, event)
