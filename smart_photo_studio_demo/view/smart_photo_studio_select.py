#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_select.py
# Created   : 2021/7/7 15:09
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPixmap, QColor, QBitmap, QPainter, QFont


ITEM_WIDTH = 119
ITEM_HEIGHT = 90



class SmartPhotoStudioSelect(QWidget):
    selectImageSignal = pyqtSignal(object)
    saveSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self._setup_layout()
        self.setStyleSheet("QWidget{background-color:transparent}")

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

    def config_string(self, conf):
        self.saveBtn.label.setText(conf.get_value_for_key("k_save"))

    def _setup_layout(self):
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)

        self._init_list()

        self.saveBtn = SaveButton(self)
        self.saveBtn.updateFrame(180, 106)
        self.saveBtn.clickSaveSignal.connect(self._click_save)
        self.saveBtn.move(1422, 0)
        self.saveBtn.show()

    def _init_list(self):

        self.listBg = QWidget(self)
        self.listBg.setFixedSize(1240, 106)
        self.listBg.setStyleSheet(
            "QWidget{background:rgba(91,105,149,0.6);border-top-left-radius:8px;border-bottom-left-radius:8px}")
        self.listBg.move(180, 0)
        self.listBg.show()

        x, w, h, margin, top = 30, ITEM_WIDTH, ITEM_HEIGHT, 10, 8
        self.images = []
        self.items = []
        dir = os.path.join(os.path.dirname(__file__), "resource/images")
        for i in range(5):
            imageName = 'bg_0' + str(i + 1) + '.png'
            pic = QPixmap(dir + '/' + imageName)

            item = ListItemWidget(self.listBg)
            item.setFixedSize(w, h)
            item.move(x + margin + i * (w + margin), top)
            item.show()
            item.setImage(pic)
            item.tag = i
            item.selectImageSignal.connect(self.select_image)

            self.images.append(pic)
            self.items.append(item)

    def _click_save(self):
        self.saveSignal.emit()

    def selectDefaultIndex(self):
        self.select_image(0)

    def select_image(self, index):
        if index >= 0 and index < len(self.images):
            image = self.images[index]
            self.selectImageSignal.emit(image)

            for item in self.items:
                item.setSelected(item.tag == index)


class ListItemWidget(QWidget):
    tag = -1
    selected = True
    selectImageSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ListItemWidget, self).__init__(parent)
        self.icon = QLabel(self)
        self.icon.setFixedSize(115, 86)
        self.icon.move(2, 2)
        self.setStyleSheet("QWidget{border-radius:10px;}")

        self.unselect_mask = QLabel(self)
        self.unselect_mask.setFixedSize(ITEM_WIDTH, ITEM_HEIGHT)
        self.unselect_mask.move(0, 0)
        self.unselect_mask.setStyleSheet("QWidget{border-radius:10px;background-color:rgba(20,26,48,0.5)}")

        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_bg_reset.png")
        self.selectIcon = self._create_icon(icon_path)

        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_bg_mouse_move.png")
        self.slippIcon = self._create_icon(icon_path)

    def _create_icon(self, icon_path):
        icon = QLabel(self)
        icon.setFixedSize(ITEM_WIDTH, ITEM_HEIGHT)
        icon.move(0, 0)
        pix = QPixmap(icon_path)
        icon.setPixmap(pix)
        icon.resize(pix.width(), pix.height())
        icon.hide()
        icon.setStyleSheet("QWidget{background-color:transparent}")
        return icon

    def setImage(self, image):

        w, h = self.icon.width(), self.icon.height()
        size = QSize(w, h)
        mask = QBitmap(size)
        painter = QPainter(mask)
        painter.begin(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.fillRect(0, 0, size.width(), size.height(), Qt.white)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRoundedRect(0.5, 0.5, size.width(), size.height(), 8, 8, Qt.AbsoluteSize)
        painter.end()
        newImage = image.scaled(size)
        newImage.setMask(mask)
        self.icon.setPixmap(newImage)
        # self.icon.setPixmap(image)

    def setSelected(self, selected):
        self.selected = selected
        if self.selected:
            self.selectIcon.show()
            self.unselect_mask.hide()
            self.slippIcon.hide()
        else:
            self.selectIcon.hide()
            self.unselect_mask.show()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.selectImageSignal.emit(self.tag)

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if not self.selected:
            self.slippIcon.show()

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.slippIcon.hide()


class SaveButton(QWidget):
    enabled = False
    clickSaveSignal = pyqtSignal()
    def __init__(self, parent=None):
        super(SaveButton, self).__init__(parent)

        bg = QWidget(self)
        bg.show()
        self.btn_bg = bg

        icon = QLabel(bg)
        icon.show()
        icon.setStyleSheet("QWidget{background-color:transparent}")
        self.saveIcon = icon

        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(20)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)

        label = QLabel(bg)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setColor(label.foregroundRole(), QColor(255, 255, 255, 255 * 0.6))
        label.setPalette(palette)
        label.setStyleSheet("QWidget{background-color:transparent}")
        self.label = label
        self.label.setText("ssss")

        self.setStyleSheet(
            "QWidget{background-color:rgba(91,105,149,0.6);border-top-right-radius:8px;border-bottom-right-radius:8px}")

    def updateFrame(self, width, height):
        self.setFixedSize(width, height)
        w, h = 120, 50
        self.btn_bg.setFixedSize(w, h)
        self.btn_bg.move((width - w) / 2, (height - h) / 2)

        icon_x, icon_w = 20, 24
        self.saveIcon.setFixedSize(icon_w, icon_w)
        self.saveIcon.move(icon_x, (h - icon_w) / 2)

        self.label.setFixedSize(w - icon_x - icon_w, h)
        self.label.move(icon_x + icon_w, 0)

        self.setEnabled(False)

    def setEnabled(self, enabled):
        self.enabled = enabled

        palette = QtGui.QPalette()
        # icon_path = ''
        if self.enabled:
            self.btn_bg.setStyleSheet("QWidget{background:rgba(145,137,254,1);border-radius:8px;}")
            palette.setColor(self.label.foregroundRole(), QColor(255, 255, 255))
            icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_save.png")
        else:
            self.btn_bg.setStyleSheet("QWidget{background:rgba(145,137,254,0.6);border-radius:8px;}")
            palette.setColor(self.label.foregroundRole(), QColor(255, 255, 255, 255 * 0.6))
            icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_save_disable.png")

        self.label.setPalette(palette)

        pix = QPixmap(icon_path)
        self.saveIcon.setPixmap(pix)
        self.saveIcon.resize(pix.width(), pix.height())

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        pos = a0.pos()

        if self.enabled:
            self.clickSaveSignal.emit()

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)
