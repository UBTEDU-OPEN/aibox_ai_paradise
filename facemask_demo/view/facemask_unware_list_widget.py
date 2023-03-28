#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_unware_list_widget.py
# Created   : 2020/6/2 8:30 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from facemask_unware_list import NoMaskLables
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPalette,QBrush,QPixmap
from PyQt5.QtCore import Qt

class FacemaskUnwareListWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        dir = os.path.join(os.path.dirname(__file__), "resource/images")

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap(os.path.join(dir, "img_bg.png"))))
        self.setPalette(self.palette)

        self.window = NoMaskLables(path = dir)
        # self.label_left = NoMaskButton()
        # self.label_left.nomask_signal.mouse_left.connect(self.window.move_scroll_left)
        # self.label_left.setPixmap(QPixmap(os.path.join(dir, "ic_weidaikouzhao_left.png")))
        # self.label_right = NoMaskButton()
        # self.label_right.nomask_signal.mouse_left.connect(self.window.move_scroll_right)
        # self.label_right.setPixmap(QPixmap(os.path.join(dir, "ic_weidaikouzhao_right.png")))
        # # self.mask_thread = FaskMaskThread()
        # # self.mask_thread.mask_signal.label_update.connect(self.window.custom_Widget.set_pic)
        # # self.mask_thread.start()
        # # self.label_left.setFixedWidth(50)
        # # self.label_right.setFixedWidth(50)
        #
        # self.layout = QHBoxLayout()
        # self.layout.setContentsMargins(0,0,0,0)
        # layout1 = QVBoxLayout()
        # layout2 = QVBoxLayout()
        # layout3 = QVBoxLayout()
        #
        #
        # layout1.setContentsMargins(0, 18, 0, 0)
        # layout1.addWidget(self.label_left, 0, Qt.AlignTop)
        #
        # self.window.list_Widget.setFixedWidth(640)
        # layout2.addWidget(self.window.list_Widget, 0, Qt.AlignTop)
        #
        # layout3.setContentsMargins(0, 17, 0, 0)
        # layout3.addWidget(self.label_right, 0, Qt.AlignTop)
        #
        #
        # self.layout.addLayout(layout1)
        # self.layout.addSpacing(10)
        # self.layout.addLayout(layout2)
        # self.layout.addSpacing(20)
        # self.layout.addLayout(layout3)
        # self.layout.addStretch()





        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        layout2 = QVBoxLayout()
        self.window.setFixedWidth(640)
        layout2.addWidget(self.window, 0, Qt.AlignTop)
        self.layout.addLayout(layout2)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def refresh(self, result):
        self.window.update_pic(result)