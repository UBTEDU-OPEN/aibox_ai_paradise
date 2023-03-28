#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: facemask_unware_list.py
# Created: 2020-06-02 19:06:27
# Author: ChenglongXiong (chenglong.xiong@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:未戴口罩列表
###
import sys, time, os
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QListWidget, QScroller, QHBoxLayout, QListWidgetItem, QListView
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QThread
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage
from PyQt5 import QtCore
from PIL import Image, ImageDraw, ImageFont, ImageQt

from PIL import Image, ImageDraw, ImageFont
import time, os
import cv2
import numpy

class NoMaskLables(QWidget):
    """未戴口罩lables

    """    
    def __init__ (self, parent = None, lables = 5, path = '.'):
        """类初始化

        Args:
            parent (ob, optional): [description]. Defaults to None.
            lables (int, optional): [description]. Defaults to 7.
            path (str, optional): [description]. Defaults to '.'.
        """        
        super(NoMaskLables, self).__init__(parent)
        self.lable_layout = QHBoxLayout()
        self.lable_layout.setContentsMargins(0,0,0,0)
        self.lable_num = lables
        self.lable_nomasks = []
        self.lable_pics = []
        self.ui_lable = 'img_weidaikouzhao.png'
        self.ui_path = path
        pic = QPixmap(self.ui_path + '/' + self.ui_lable)
        for i in range(self.lable_num):
            self.lable_nomasks.append(QLabel())
            self.lable_nomasks[i].setPixmap(pic)
            self.lable_pics.append(pic)
            self.lable_layout.addWidget(self.lable_nomasks[i])

        self.setLayout(self.lable_layout)

    @pyqtSlot()
    def set_pic(self, pics):
        """设置lable图片

        Args:
            pics (list): 图片
        """        
        for item in pics:

            rgb_image = item
            height, width, channel = rgb_image.height, rgb_image.width, 3
            bytes_perline = 3 * width
            qt_image = ImageQt.ImageQt(rgb_image)
            qt_image = QPixmap.fromImage(qt_image)
            self.lable_pics.insert(0, qt_image)
            self.lable_pics.pop()

        for i in range(self.lable_num):
            self.lable_nomasks[i].setPixmap(self.lable_pics[i])


    def update_pic(self, pics):
        self.lable_pics = pics
        for i in range(self.lable_num):
            self.lable_nomasks[i].setPixmap(self.lable_pics[i])


class NoMaskList(QMainWindow):
    """未戴口罩列表

    """    
    def __init__ (self, path = '.'):
        """初始化
        """        
        super(NoMaskList, self).__init__()
        # Create QListWidget
        self.list_Widget = QListWidget()#QListWidget(self)
        self.list_Widget.setMovement(QListView.Free)
        self.list_Widget.setStyleSheet('background-color:transparent')
        QScroller.grabGesture(self.list_Widget, QScroller.LeftMouseButtonGesture)
        self.list_Widget.setFrameShape(QListWidget.NoFrame)
        self.list_Widget.horizontalScrollBar().setHidden(True)
        
        self.custom_Widget = NoMaskLables(path = path)

        item = QListWidgetItem(self.list_Widget)
        item.setSizeHint(self.custom_Widget.sizeHint())
        self.list_Widget.addItem(item)
        self.list_Widget.setItemWidget(item, self.custom_Widget)
        self.setCentralWidget(self.list_Widget)

    @pyqtSlot()
    def move_scroll_left(self, val):
        """左移

        Args:
            val (int): 保留
        """        
        lk = self.list_Widget.horizontalScrollBar()
        item = lk.maximum()//7
        lk.setValue(lk.value()+item)

    @pyqtSlot()
    def move_scroll_right(self, val):
        """右移

        Args:
            val (int): 保留
        """        
        lk = self.list_Widget.horizontalScrollBar()
        item = lk.maximum()//7
        lk.setValue(lk.value() - item)

class NoMaskButton(QLabel):
    """未戴口罩按钮

    """    
    def __init__(self, parent=None):
        """类初始化

        Args:
            parent (object, optional): Defaults to None.
        """        
        super (NoMaskButton, self).__init__ (parent)
        self.nomask_signal = NoMaskSignals()

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        # 左键按下
        if e.buttons () == QtCore.Qt.LeftButton:
            self.nomask_signal.mouse_left.emit(1)

class NoMaskSignals(QObject):
    """信号

    """
    #鼠标左键
    mouse_left = pyqtSignal(int)
    #lable图片有更新
    label_update = pyqtSignal(object)