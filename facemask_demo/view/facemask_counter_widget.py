#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_counter_widget.py
# Created   : 2020/5/25 11:00 上午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QFont,QColor

class FacemaskCounterWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tipWidget = TipWidget()
        self.countWidget = CountWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.tipWidget)
        layout.addWidget(self.countWidget)
        self.setLayout(layout)

        self.setMaximumHeight(220)

    def config_string(self, conf):
        self.tipWidget.coutlab.setText(conf.get_value_for_key("k_count_title"))
        self.tipWidget.attlab.setText(conf.get_value_for_key("k_count_desc"))

        self.countWidget.onlab.setText(conf.get_value_for_key("k_count_ware"))
        self.countWidget.offlab.setText(conf.get_value_for_key("k_count_unware"))

        # Public
    def update_warecount(self, count):
        self.countWidget.update_warecount(count)

    def update_unwarecount(self, count):
        self.countWidget.update_unwarecount(count)

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

class TipWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(60)
        self.setStyleSheet("QWidget{background:#4F5A7E;border-top-left-radius:8px;border-top-right-radius:8px}")


        """设置 label"""
        self.coutlab = QLabel()
        self.coutlab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        palette = QtGui.QPalette()
        palette.setColor(self.coutlab.foregroundRole(), QColor(255, 255, 255))
        self.coutlab.setPalette(palette)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(24)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)
        self.coutlab.setFont(font)

        self.attlab = QLabel()
        self.attlab.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        palette = QtGui.QPalette()
        palette.setColor(self.attlab.foregroundRole(), QColor(168, 172, 188))
        self.attlab.setPalette(palette)

        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Normal)

        self.attlab.setFont(font)

        """设置 self"""
        layout = QHBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.coutlab)
        layout.addSpacing(10)
        layout.addWidget(self.attlab)
        layout.addStretch()
        self.setLayout(layout)


    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

class CountWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("QWidget{background:#3C4668;border-bottom-left-radius:8px;border-bottom-right-radius:8px}")
        self.setMaximumHeight(160)

        """设置 label"""
        self.onlab = self._init_tip_label()

        self.offlab = self._init_tip_label()

        self.onnum = self._init_number_label()
        self.onnum.setStyleSheet('QLabel{border-radius:18px;background-color: rgb(134, 208, 106);}')

        self.offnum = self._init_number_label()
        self.offnum.setStyleSheet('QLabel{border-radius:18px;background-color: rgb(255, 125, 104);}')

        """设置layout"""
        vlayout = QHBoxLayout()

        """设置 self"""
        layout1 = QVBoxLayout()
        # layout1.addSpacing(20)
        layout1.insertWidget(0, self.onlab, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout1.insertWidget(1, self.onnum, 0, Qt.AlignLeft | Qt.AlignVCenter)
        # layout1.addSpacing(20)

        layout2 = QVBoxLayout()
        # layout2.addSpacing(20)
        layout2.insertWidget(0, self.offlab, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout2.insertWidget(1, self.offnum, 0, Qt.AlignLeft | Qt.AlignVCenter)
        # layout2.addSpacing(20)

        vlayout.addSpacing(20)
        vlayout.addLayout(layout1)
        vlayout.addSpacing(0)
        vlayout.addLayout(layout2)
        # vlayout.addSpacing(25)
        self.setLayout(vlayout)

        # Public
    def update_warecount(self, count):
        if count <= 0:
            self.onnum.setText('0')
        else:
            self.onnum.setText(str(count))

    def update_unwarecount(self, count):
        if count <= 0:
            self.offnum.setText('0')
        else:
            self.offnum.setText(str(count))

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

    def _init_number_label(self):
        label = QLabel('0')
        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(26)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(label.foregroundRole(), QColor(255, 255, 255))
        label.setAutoFillBackground(True)
        label.setPalette(palette)
        label.setMinimumSize(100, 36)
        return label

    def _init_tip_label(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(20)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)

        label = QLabel('已戴口罩的人脸数量')
        label.setAlignment(Qt.AlignLeft)
        palette = QtGui.QPalette()
        palette.setColor(label.foregroundRole(), QColor(255, 255, 255))
        label.setPalette(palette)
        label.setFont(font)
        label.setMinimumWidth(220)
        #适配英文
        label.setWordWrap(True)
        return label