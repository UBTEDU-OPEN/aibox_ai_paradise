#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_confidence_widget.py
# Created   : 2020/6/1 2:27 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QFont,QPixmap,QColor
from PyQt5 import QtGui
from PyQt5 import QtWidgets
sys.path.append('..')
sys.path.append('..')
from common.ui.slider.slider import Slider
from common.ui.bubbleDialog.popwindow import PopWindow,BUBBLE_SIZE
from common.utility.configure_string_single import  ConfigureStringSingle

from facemask_config import FacemaskConfig
from clickable_label import UClickableLabel

class FacemaskConfidenceWidget(QWidget):

    confidenceSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)

        self.tipWidget = TopWidget(self.parent)
        self.bottomWidget = BottomWidget()

        self.bottomWidget.slider.value_changed.connect(self.change_confidence_level)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.tipWidget)
        layout.addWidget(self.bottomWidget)
        self.setLayout(layout)

        self.setMinimumHeight(250)

        # Public
    def change_confidence_level(self, value):
        self.confidenceSignal.emit(value)

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

class TopWidget(QWidget):

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.setStyleSheet("QWidget{background:#4F5A7E;border-top-left-radius:8px;border-top-right-radius:8px}")
        self.setFixedHeight(60)

        configure_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../config/locale"
        self.conf = ConfigureStringSingle(configure_file_path, 'facemask')

        """设置 label"""
        self.titleLabel = self._init_title_label()
        self.tipBtn = self._init_tip_btn()

        # str = self.conf.get_value_for_key("k_pop_text")
        # self.dialog = PopWindow(self.tipBtn, content = str,size=BUBBLE_SIZE,parent = self.parent)

        """设置 self"""
        layout = QHBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.titleLabel)
        layout.addSpacing(20)
        layout.addWidget(self.tipBtn)
        layout.addStretch()
        self.setLayout(layout)

        self.dialog = PopWindow(self.tipBtn, parent=self.parent)

    def _init_title_label(self):
        label = QLabel()
        label.setText(self.conf.get_value_for_key("k_confidence_title"))
        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(24)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)
        label.setFont(font)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        palette = QtGui.QPalette()
        palette.setColor(label.foregroundRole(), QColor(255, 255, 255))
        label.setPalette(palette)
        return label

    def _init_tip_btn(self):

        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_info.png")
        icon_press_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_info_press.png")

        btn = UClickableLabel(normal_pixmap=QPixmap(icon_path), pressed_pixmap=QPixmap(icon_press_path))
        btn.clicked.connect(self._click_tip_btn)
        return btn

    def _click_tip_btn(self):
        print('show tip hint')

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

class BottomWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QWidget{background:#3C4668;border-bottom-left-radius:8px;border-bottom-right-radius:8px}")

        """设置 self"""
        layout = QHBoxLayout()
        self.slider = Slider(FacemaskConfig.DEFAULT_CONFIDENCE_LEVEL, ConfigureStringSingle.get_common_string_cfg().get_value_for_key('ubt_default'))
        layout.addWidget(self.slider)
        layout.addSpacing(0)
        self.setLayout(layout)

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)
