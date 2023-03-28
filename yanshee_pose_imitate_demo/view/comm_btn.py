#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout


class CommonBtn(QPushButton):
    clicked = pyqtSignal()
    styleSheet = '''
    #CommonButton {
        background-color: #9189FE;
        color: #FFFFFF;
        border-radius: 8px;
        font-size: 16px;
        min-width: 120px;
        min-height: 50px;
        padding-left: 5px;
        padding-right: 5px;
    }
    #TMButton {
        background-color: #66000000;
        color: #FFFFFF;
        border-radius: 8px;
        font-size: 16px;
        min-width: 120px;
        min-height: 50px;
        border: 1px solid #EEECEC;
        padding-left: 5px;
        padding-right: 5px;
    }
    #IconButton {
        background-color: #9189FE;
        color: #FFFFFF;
        border-radius: 8px;
        font-size: 16px;
        min-width: 160px;
        min-height: 50px;
        padding-left: 5px;
        padding-right: 5px;
    }
    '''

    def __init__(self, text, icon=None, style=1):
        super().__init__()
        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(1)
        self.setGraphicsEffect(self.op)
        self.setStyleSheet(self.styleSheet)
        if style == 1:
            self.init_layout1(text)
        elif style == 2:
            self.init_layout2(text, icon)
        elif style == 3:
            self.init_layout3(text)

    def init_layout1(self, text):
        self.setContentsMargins(0, 0, 0, 0)
        self.setText(text)
        self.setObjectName("CommonButton")

    def init_layout2(self, text, icon):
        self.setObjectName("IconButton")

        self.setText(" " + text)
        self.setIcon(QIcon(icon))

        # layout = QHBoxLayout()
        # label1 = QLabel()
        # label1.setText(text)
        # label1.setStyleSheet("font-size: 16px;color: #FFFFFF;")
        # label2 = QLabel()
        # label2.setPixmap(QPixmap(icon))
        # layout.addSpacing(10)
        # layout.addWidget(label2)
        # layout.addSpacing(10)
        # layout.addWidget(label1, alignment=QtCore.Qt.AlignCenter)
        # layout.addStretch()
        # self.setLayout(layout)

    def init_layout3(self, text):
        self.setContentsMargins(0, 0, 0, 0)
        self.setText(text)
        self.setObjectName("TMButton")

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.op.setOpacity(0.5)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.op.setOpacity(1)
        self.clicked.emit()

    def set_click_enable(self, enabled):
        self.setEnabled(enabled)
        self.op.setOpacity(1) if enabled else self.op.setOpacity(0.3)
