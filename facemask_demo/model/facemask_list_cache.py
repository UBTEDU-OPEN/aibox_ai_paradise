#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_list_cache.py
# Created   : 2020/10/27 2:16 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 未戴口罩列表缓存，保证异常后不清空列表

import os
from PyQt5.QtGui import QPixmap
from PIL import ImageQt

class FacemaskListCache(object):

    def __init__(self):

        self.label_num = 5
        self.label_pics = []
        self.ui_path = os.path.dirname(os.path.realpath(__file__)) + '/../view/resource/images/img_weidaikouzhao.png'
        pic = QPixmap(self.ui_path)

        for i in range(self.label_num):
            self.label_pics.append(pic)


    def set_pic(self, pics):
        """设置lable图片

        Args:
            pics (list): 图片
        """
        for item in pics:

            rgb_image = item
            height, width, channel = rgb_image.height, rgb_image.width, 3
            qt_image = ImageQt.ImageQt(rgb_image)
            qt_image = QPixmap.fromImage(qt_image)
            self.label_pics.insert(0, qt_image)
            self.label_pics.pop()