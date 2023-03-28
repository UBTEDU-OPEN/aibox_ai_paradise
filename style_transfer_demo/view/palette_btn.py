#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:platte_btn.py
# Created:2020/9/16 上午11:35
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton


class PaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()

        self.color = color
        self._update_select(False)

    def update(self, c):
        if c == self.color:
            self._update_select(True)
        else:
            self._update_select(False)

    def _update_select(self, is_select):
        size = 46
        style = "border-radius: %dpx;background-color: %s" % (size / 2, self.color)
        if is_select:
            size = 56
            style = "border: 2px solid #FFFFFF;border-radius: %dpx;background-color: %s" % (size / 2, self.color)
        self.setFixedSize(size, size)
        self.setStyleSheet(style)