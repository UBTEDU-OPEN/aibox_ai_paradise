#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget


class IndicatorWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(IndicatorWidget, self).__init__(*args, **kwargs)
        self.highlightindex = 0
        self.count = 4

    def setHighlight(self, index):
        self.highlightindex = index
        self.update()

    def paintEvent(self, event):
        super(IndicatorWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        color = QColor(255, 255, 255)
        color = color.toRgb()
        for i in range(self.count):
            if i == self.highlightindex:
                color.setAlphaF(1)
            else:
                color.setAlphaF(0.15)
            painter.setBrush(color)
            painter.drawEllipse(14 * i, 0, 6, 6)
