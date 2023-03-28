#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:goods_item.py
# Created:2020/5/28 上午10:58
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:group goods
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import PyQt5.QtCore as QtCore

from view.goods_item import GoodsItem
from R import R
from config.object_config_util import ConfigUtils


class SelectItem(QWidget):
    icons = [R.imgs_img_bg_purple, R.imgs_img_bg_green, R.imgs_img_bg_yellow]

    def __init__(self):
        super().__init__()
        self.flag = ''
        self.item_check = QLabel(self)
        self.item_check.setGeometry(0, 0, 110, 110)
        self.item_check.setPixmap(QPixmap(R.imgs_img_pandian_quesheng))

        # draw goods_icon
        self.item_icon = QLabel(self)
        self.item_icon.setGeometry(19, 19, 72, 72)

        # draw goods_name
        self.item_name = QLabel(self)
        self.item_name.setObjectName('select_item_name')
        self.item_name.setGeometry(0, 110, 110, 26)
        self.item_name.setAlignment(QtCore.Qt.AlignCenter)

        # draw goods_count
        self.item_count = QLabel(self)
        self.item_count.setObjectName('select_item_name')
        self.item_count.setGeometry(0, 130, 110, 22)
        self.item_count.setAlignment(QtCore.Qt.AlignCenter)

    def update_widget(self, goodsItem: GoodsItem):
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(self.icons[goodsItem.check_icon])))
        # self.setPalette(palette)

        self.item_check.setGeometry(0, 0, 110, 156)
        self.item_check.setPixmap(QPixmap(self.icons[goodsItem.check_icon]))

        self.flag = goodsItem.flag
        self.item_icon.show()
        self.item_icon.setPixmap(QPixmap(os.path.join(os.path.dirname(os.path.dirname(__file__)), ConfigUtils().getImgValue(goodsItem.flag))))

        self.item_name.show()
        self.item_name.setText(goodsItem.name)

        self.item_count.show()
        self.item_count.setText('0')

    def update_widget_count(self, keys):
        self.item_count.setText(str(keys.count(self.flag)))

    def show_default(self):
        self.item_check.setGeometry(0, 0, 110, 110)
        self.item_check.setPixmap(QPixmap(R.imgs_img_pandian_quesheng))
        self.item_name.hide()
        self.item_count.hide()
        self.item_icon.hide()
