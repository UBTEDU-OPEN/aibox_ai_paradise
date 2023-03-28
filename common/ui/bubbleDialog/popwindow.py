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
from PyQt5.QtGui import QCursor, QPixmap
from common.utility.configure_string_single import ConfigureStringSingle

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from layout import Ui_Bubble

BUBBLE_POSITION = (782, 114)
BUBBLE_SIZE = (640, 109)
DEFAULT_TXT = ConfigureStringSingle.get_common_string_cfg().get_value_for_key('ubt_confidence_tip')


class PopWindow(QWidget, Ui_Bubble):

    def __init__(self, anchor: QLabel, content=DEFAULT_TXT, size=BUBBLE_SIZE, parent=None):
        super(PopWindow, self).__init__(parent)
        self.setupUi(self)
        self.anchor = anchor
        self.size = size
        self.pos = BUBBLE_POSITION
        self.anchor.clicked.connect(self.show_pop)
        self.isShow = False
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        # self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.init_ui(content)

        # self.pop.setGeometry(777, 117, *size)
        # self.show()
        self.hide()
        self.pop.setStyleSheet("QWidget{background-color:transparent}")
        self.installEventFilter(self)

    def get_pos(self):
        pass
        # import tkinter
        # win = tkinter.Tk()
        # print('screenwidth', win.winfo_screenwidth())
        # print('screenheight', win.winfo_screenheight())
        # bz_w = 1920
        # bz_h = 1080
        # return (782 - (bz_w - win.winfo_screenwidth()) / 5.2, 114 - (bz_h - win.winfo_screenheight()) / 2.5)

    # def conf(self):
    #     # pass
    #     self.setMask(QBitmap("resource/images/img_bg.png"))
    #     self.verticalWidget.setFixedSize(1080, 720)

    # def resizeEvent(self, a0: QtGui.QResizeEvent):
    #     bitmap = QBitmap(self.width(), self.height())
    #     painter = QPainter(bitmap)
    #     self.painter = painter
    #     painter.setPen(QColor(255, 0, 0))
    #     painter.drawRect(0, 0, 100, 100)
    #     painter.setPen(QColor(0, 255, 0))
    #     self.drawTextOnWin(painter)
    #     self.setBackgroundRole(QPalette.ColorRole(Qt.red))
    # self.setMask(bitmap)

    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #     painter = QPainter(self)
    #     painter.setPen(QColor(Qt.red))
    #     self.drawTextOnWin(painter)

    # def drawTextOnWin(self, painter: QPainter):
    #     painter.setFont(QFont(self.font().family(), 15))
    #     painter.drawText((self.width() - 300) / 2, 0, 300, 50, Qt.AlignHCenter, "Now you can see me!")

    def init_ui(self, content):
        content = content.replace("\\n", "\n")
        self.content.setText(content)
        # self.content.setAlignment(Qt.AlignCenter)
        # self.content.adjustSize()
        # self.content.setWordWrap(True)
        self.arrow.setStyleSheet("QLabel{background-color:transparent}")
        self.arrow.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "resource/images", "ic_arrow_bubble.png")))

        qssFile = os.path.join(os.path.dirname(__file__) + '/resource/qss/style.qss')
        with open(qssFile) as fp:
            qss = fp.read()
            self.setStyleSheet(qss)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        anchor_pos = self.anchor.mapToGlobal(QtCore.QPoint(0, 0))
        self.pop.setGeometry(anchor_pos.x() - self.size[0] / 2 + self.anchor.width() / 2,
                             anchor_pos.y() - self.size[1] - self.anchor.height() / 2, *self.size)
        # self.pop.setGeometry(*self.pos, *self.size)

    def show_pop(self):
        # self.pop.move(777, 117)
        # print('show_pop', self.isShow)
        # x_offset = QCursor.pos().x()
        # y_offset = QCursor.pos().y()
        # self.setGeometry(x_offset - self.size[0] / 2, y_offset - self.size[1] - 13, *self.size)
        # x_offset = self.anchor.x()
        # y_offset = self.anchor.y()
        # self.setGeometry(x_offset - self.size[0] / 2 + self.anchor.width() / 2, y_offset - self.size[1] + self.anchor.height(), *self.size)
        # g_anc = self.mapToParent(self.anchor.pos())
        # print(self.anchor.pos())
        # print(g_anc)
        # self.setGeometry(g_anc.x(), g_anc.y(), *self.size)
        # self.show()
        if self.isShow:
            self.hide()
            self.isShow = False
        else:
            x_offset = QCursor.pos().x()
            y_offset = QCursor.pos().y()
            # self.setGeometry(x_offset - self.size[0] / 2, y_offset - self.size[1] - 13, *self.size)
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

    # def eventFilter(self, ob: QtCore.QObject, event: QtCore.QEvent):
    #     print('eventFilter', ob==self, event.type())
    #     if ob == self:
    #         if event.type() == QtCore.QEvent.MouseButtonPress:
    #             self.hide()
    #             # print('eventFilter', self.isShow)
    #             # self.isShow = False
    #             event.accept()
    #             return True
    #
    #     return QWidget.eventFilter(self, ob, event)

    # def mousePressEvent(self, a0: QtGui.QMouseEvent):
    #     if not self.geometry().contains(a0.globalPos()):
    #         self.hide()
    #     else:
    #         QDialog.mousePressEvent(self, a0)
