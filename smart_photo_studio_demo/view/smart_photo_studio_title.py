#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_title.py
# Created   : 2021/7/7 11:07 上午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import os
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QFont,QPixmap,QColor
from clickable_label import UClickableLabel

class SmartPhotoStudioTitle(QWidget):
    closeSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setMaximumHeight(200)
        # self.setMaximumWidth(700)
        self.setAutoFillBackground(True)
        self._setup_layout()
        self.setStyleSheet("QWidget{background-color:transparent}")
        # self.setStyleSheet("QWidget{background-color:blue}")

    def config_string(self, conf):
        self.titleLabel.setText(conf.get_value_for_key("k_title"))
        self.tipLabel.setText(conf.get_value_for_key("k_title_desc"))

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

    def _setup_layout(self):

        self.icon = self._init_logo()
        self.titleLabel = self._init_title()
        self.tipLabel = self._init_tip()
        self.tipLabel.setFixedWidth(840)
        self.closeBtn = self._init_close_btn()

        """设置layout"""
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 34, 0, 20)
        """设置 self"""
        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.insertWidget(0, self.icon, 0, Qt.AlignLeft)
        layout1.addStretch()

        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.addWidget(self.titleLabel, 0, Qt.AlignTop | Qt.AlignLeft)
        layout2.addSpacing(20)
        layout2.addWidget(self.tipLabel, 0, Qt.AlignTop | Qt.AlignLeft)
        # layout2.addStretch()

        layout3 = QVBoxLayout()
        layout3.insertWidget(0, self.closeBtn, 0, Qt.AlignTop | Qt.AlignRight)

        # vlayout.addSpacing(25)
        contentLayout.addLayout(layout1)
        contentLayout.addSpacing(80)
        contentLayout.addLayout(layout2)
        contentLayout.addStretch()
        contentLayout.addLayout(layout3)

        import tkinter
        win = tkinter.Tk()
        if win.winfo_screenwidth() < 1920:
            contentLayout.addSpacing(1920 - win.winfo_screenwidth())
        else:
            contentLayout.addSpacing(90)
        # contentLayout.addSpacing(90)
        # vlayout.addSpacing(25)
        self.setLayout(contentLayout)

    def _init_logo(self):

        icon = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "img_logo_take_picture.png")
        pix = QPixmap(icon_path)
        icon.setPixmap(pix)
        icon.resize(pix.width(), pix.height())
        return icon

    def _init_title(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(36)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)

        label = QLabel()
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        palette = QtGui.QPalette()
        palette.setColor(label.foregroundRole(), QColor(255, 255, 255))
        label.setAutoFillBackground(True)
        label.setPalette(palette)
        return label

    def _init_tip(self):
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Normal)

        label = QLabel()
        label.setFont(font)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeading)
        palette = QtGui.QPalette()
        palette.setColor(label.foregroundRole(), QColor(120, 122, 147))
        label.setAutoFillBackground(True)
        label.setPalette(palette)
        return label

    def _init_close_btn(self):

        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_close.png")
        icon_press_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_close_press.png")

        btn = UClickableLabel(normal_pixmap=QPixmap(icon_path), pressed_pixmap=QPixmap(icon_press_path))
        btn.resize(44, 44)
        btn.clicked.connect(self._click_close_btn)
        return btn

    def _click_close_btn(self):
        self.closeSignal.emit()
