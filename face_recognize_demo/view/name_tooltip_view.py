#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:popwindow.py
# Created:2020/6/2 上午10:43
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
import os
import sys

from PyQt5.QtGui import QCursor, QPixmap

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from name_tooltip_ui import Ui_NameTooltip


_WIDGET_MAX_HEIGTH = 56


class NameTooltip(QWidget, Ui_NameTooltip):

    def __init__(self, content="", parent=None):
        super(NameTooltip, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.init_ui(content)
        self.installEventFilter(self)


    def init_ui(self, content):
        self.content.setText(content)
        self.content.adjustSize()
        self.setFixedSize(self.content.width(), _WIDGET_MAX_HEIGTH)
        self.arrow.setPixmap(QPixmap(":/resource/ic_arrow_name.png"))

    def eventFilter(self, ob: QtCore.QObject, event: QtCore.QEvent):
        if ob == self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.close()
                event.accept()
                return True

        return QWidget.eventFilter(self, ob, event)

