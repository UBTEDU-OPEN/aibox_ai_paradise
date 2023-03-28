#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:test.py
# Created:2020/6/3 下午7:57
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QFontMetrics, QMovie, QMoveEvent
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton


class LoadingMask(QMainWindow):
    def __init__(self, parent, gif=None, tip=None):
        super(LoadingMask, self).__init__(parent)

        parent.installEventFilter(self)

        self.label = QLabel()

        if not tip is None:
            self.label.setText(tip)
            font = QFont('Microsoft YaHei', 10, QFont.Normal)
            font_metrics = QFontMetrics(font)
            self.label.setFont(font)
            self.label.setFixedSize(font_metrics.width(tip, len(tip)) + 10, font_metrics.height() + 5)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setStyleSheet(
                'QLabel{background-color: rgba(0,0,0,70%);border-radius: 4px; color: white; padding: 5px;}')

        if not gif is None:
            self.movie = QMovie(gif)
            self.label.setMovie(self.movie)
            self.label.setFixedSize(QSize(160, 160))
            self.label.setScaledContents(True)
            self.movie.start()

        layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(self.label)

        self.setCentralWidget(widget)
        self.setWindowOpacity(0.8)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.hide()

    def eventFilter(self, widget, event):
        if widget == self.parent() and type(event) == QMoveEvent:
            self.moveWithParent()
            return True
        return super(LoadingMask, self).eventFilter(widget, event)

    def moveWithParent(self):
        if self.isVisible():
            self.move(self.parent().geometry().x(), self.parent().geometry().y())
            self.setFixedSize(QSize(self.parent().geometry().width(), self.parent().geometry().height()))

    @staticmethod
    def showToast(window, tip='加载中...', duration=500):
        mask = LoadingMask(window, tip=tip)
        mask.show()
        # 一段时间后移除组件
        QTimer().singleShot(duration, lambda: mask.deleteLater())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    widget = QWidget()
    widget.setFixedSize(1920, 1080)
    widget.setStyleSheet('QWidget{background-color:white;}')

    button = QPushButton('button')
    layout = QHBoxLayout()
    layout.addWidget(button)
    widget.setLayout(layout)

    loading_mask = LoadingMask(widget, 'resource/images/img_bg.png')
    loading_mask.show()
    widget.installEventFilter(loading_mask)
    widget.show()

    sys.exit(app.exec_())
