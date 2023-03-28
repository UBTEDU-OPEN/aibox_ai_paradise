import os
import sys

from PyQt5 import QtWidgets

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import *


class ButtonLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._init()

    def __init__(self, *__args):
        super().__init__(*__args)
        self._init()

    def _init(self):
        self.is_enabled = True
        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(1)
        self.setGraphicsEffect(self.op)

    def mousePressEvent(self, ev: QKeyEvent):
        # self.setStyleSheet('''background: rgba(255, 255, 255, 0.3);''')
        self.op.setOpacity(0.5)
        # if self.press_icon is not None:
        #     self.setPixmap(QPixmap(self.press_icon))

    def mouseReleaseEvent(self, ev: QKeyEvent):
        # self.setStyleSheet('''background: rgba(255, 255, 255, 0);''')
        if self.is_enabled:
            self.op.setOpacity(1)
        self.clicked.emit()
        # if self.press_icon is not None:
        #     self.setPixmap(QPixmap(self.normal_icon))

    def set_selector(self, normal, press):
        self.normal_icon = normal
        self.press_icon = press

    def set_click_enable(self, enabled):

        # if enabled:
        #     self.setPixmap(QPixmap(self.normal_icon))
        #     self.set_selector(self.normal_icon, self.press_icon)
        # else:
        #     self.setPixmap(QPixmap(self.press_icon))
        #     self.set_selector(self.press_icon, self.press_icon)
        self.is_enabled = enabled
        # self.setEnabled(enabled)
        self.op.setOpacity(1) if enabled else self.op.setOpacity(0.5)
        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(1) if enabled else op.setOpacity(0.5)
        # self.setGraphicsEffect(op)
        # self.setEnabled(enabled)
