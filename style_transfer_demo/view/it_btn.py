#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:it_btn.py
# Created:2020/9/16 下午2:50
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout


class IconAndTextButton(QPushButton):
    clicked = pyqtSignal()

    def __init__(self, text, icon):
        super().__init__()
        self.setFixedSize(120, 50)
        self.setStyleSheet("background-color:#9189FE;color: #FFFFFF;border-radius: 8px;font-size: 18px;")
        # label1 = QLabel()
        # label1.setStyleSheet("background-color:transparent;")
        # label1.setText(text)
        # label2 = QLabel()
        # label2.setStyleSheet("background-color:transparent;")
        # label2.setPixmap(QPixmap(icon))
        #
        # layout = QHBoxLayout()
        # layout.addSpacing(10)
        # layout.addWidget(label2)
        # layout.addSpacing(10)
        # layout.addWidget(label1)
        # layout.addSpacing(10)
        # layout.addStretch()
        # self.setLayout(layout)

        self.setText(" " + text)
        self.setIcon(QIcon(icon))

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(1)
        self.setGraphicsEffect(self.op)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.op.setOpacity(0.5)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.op.setOpacity(1)
        self.clicked.emit()

    def set_click_enable(self, enabled):
        self.setEnabled(enabled)
        self.op.setOpacity(1) if enabled else self.op.setOpacity(0.3)
