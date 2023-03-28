#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:goods_item.py
# Created:2020/5/28 上午10:58
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:group goods
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import PyQt5.QtCore as QtCore

from R import R
from config.object_config_util import ConfigUtils


class GoodsItem(QWidget):
    displaySignal = QtCore.pyqtSignal(bool)
    updateSelectSignal = QtCore.pyqtSignal(object)

    icons = [R.imgs_ic_gouxuan_purple, R.imgs_ic_gouxuan_green, R.imgs_ic_gouxuan_yellow]
    origin_res = [0, 1, 2]
    select_res = []

    def __init__(self, flag, name):
        super().__init__()
        # self.setMaximumWidth(198)
        # self.setMinimumWidth(168)
        self.flag = flag
        self.name = ConfigUtils().getValue(flag)
        self.checked = False
        self.item_check = QLabel(self)
        self.item_check.setGeometry(14, 12, 26, 26)
        self.item_check.setPixmap(QPixmap(R.imgs_ic_gouxuan_enable))
        self.check_icon = R.imgs_ic_gouxuan_enable

        self.item_name = QLabel(self.name, self)
        self.item_name.setObjectName('goods_item')
        self.item_name.setGeometry(55, 0, 152, 50)

    def update(self, disable):
        if self.checked:
            pass
        else:
            if disable:
                self.item_check.setPixmap(QPixmap(R.imgs_ic_gouxuan_disable))
                self.check_icon = R.imgs_ic_gouxuan_disable
                self.item_name.setStyleSheet("QLabel{color: #4CFFFFFF;background-color:transparent}")
            else:
                self.item_check.setPixmap(QPixmap(R.imgs_ic_gouxuan_enable))
                self.check_icon = R.imgs_ic_gouxuan_enable
                self.item_name.setStyleSheet("QLabel{color: #FFFFFFFF;background-color:transparent}")

    def mousePressEvent(self, event):
        if self.checked:
            self.checked = False
            self.select_res.remove(self.check_icon)
            self.item_check.setPixmap(QPixmap(R.imgs_ic_gouxuan_enable))
            self.check_icon = R.imgs_ic_gouxuan_enable
            self.displaySignal.emit(False)
            self.updateSelectSignal.emit(self)
        else:
            union_icons = list(set(self.origin_res) - set(self.select_res))
            print(union_icons)
            if union_icons:
                self.item_check.setPixmap(QPixmap(self.icons[union_icons[0]]))
                self.check_icon = union_icons[0]
                self.checked = True
                self.select_res.append(union_icons[0])
                self.displaySignal.emit(len(set(self.origin_res) - set(self.select_res)) == 0)
                self.updateSelectSignal.emit(self)
            else:
                pass
