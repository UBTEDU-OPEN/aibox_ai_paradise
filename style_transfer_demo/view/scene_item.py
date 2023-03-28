#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:scene_item.py
# Created:2020/9/16 下午17:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:group goods
import os

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from R import R


class SceneItem(QWidget):
    updateSelectSignal = QtCore.pyqtSignal(object)

    def __init__(self, name, icon, show_mask):
        super().__init__()
        self.name = name
        self.show_mask = show_mask
        self.resid = os.path.join(os.path.dirname(os.path.dirname(__file__)), icon)
        self.setFixedSize(119, 90)
        self.item_check = QLabel(self)
        pm = QPixmap(self.resid)
        pm = pm.scaled(119, 90)
        self.item_check.setPixmap(pm)
        self.item_check.setAlignment(Qt.AlignCenter)

        if show_mask:
            # add rounder corner
            border = QLabel(self.item_check)
            pix = QPixmap(R.imgs_ic_round_border)
            border.setPixmap(pix)

            # add mask border
            self.mask = QLabel(self.item_check)
            pix = QPixmap(R.imgs_ic_white_border)
            self.mask.setPixmap(pix)
            self.mask.setHidden(True)

    def update(self, icon):
        if self.show_mask:
            self.mask.setHidden(not self.resid.endswith(icon))

    def paintEvent(self, a0) -> None:
        pass

    def mousePressEvent(self, event):
        self.updateSelectSignal.emit(self)
        # self.item_check.setStyleSheet("border: 2px solid #FFFFFF;")
        # self.item_check.setStyleSheet("QWidget{background:#4F5A7E;border-top-left-radius:8px;border-top-right-radius:8px}")
