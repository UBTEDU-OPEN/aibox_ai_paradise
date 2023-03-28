#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import PyQt5.QtCore as QtCore

from R import R


class DeviceItem(QWidget):
    def __init__(self):
        super().__init__()
        # draw device_icon
        self.item_icon = QLabel(self)
        self.item_icon.setGeometry(0, 0, 60, 60)
        self.item_icon.setPixmap(QPixmap(R.imgs_img_yanshee_default))

        # draw device_sn
        self.item_name = QLabel(self)
        self.item_name.setObjectName('device_item_sn')
        self.item_name.setGeometry(0, 66, 60, 18)
        self.item_name.setAlignment(QtCore.Qt.AlignCenter)
        self.item_name.hide()

    def update_widget(self, name):
        self.item_icon.setPixmap(QPixmap(R.imgs_img_yanshee_link))

        self.item_name.show()
        self.item_name.setText(name[-4:])

    def show_default(self):
        self.item_icon.setPixmap(QPixmap(R.imgs_img_yanshee_default))
        self.item_name.hide()
