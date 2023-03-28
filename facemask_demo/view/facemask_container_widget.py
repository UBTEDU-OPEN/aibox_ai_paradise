#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_container_widget.py
# Created   : 2020/5/27 10:33 上午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QFont,QColor,QPixmapCache,QImage
from PyQt5.QtCore import pyqtSignal,Qt

from facemask_counter_widget import FacemaskCounterWidget
from facemask_title_widget import  FacemaskTitleWidget
from facemask_confidence_widget import FacemaskConfidenceWidget
from clickable_label import UClickableLabel
from facemask_unware_list_widget import FacemaskUnwareListWidget
from facemask_camera_widget import FacemaskCameraWidget

sys.path.append('..')
from module.inference.face_mask_inference import *
sys.path.append('..')
from common.utility.configure_string_single import ConfigureStringSingle
from common.ui.commonDialog.BaseDialog import BaseDialogView
import cv2
import numpy as np
import time


from facemask_config import FacemaskConfig

class FacemaskContainerWidget(QWidget):

    voiceSignal = pyqtSignal(bool)
    closeSignal = pyqtSignal()
    confidenceLevelSignal = pyqtSignal(int)
    unwareCountSignal = pyqtSignal(int)
    listCacheSignal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.voiceOn = False
        self.loaded = False
        self.last_update_time = 0
        self.last_unware_count = 0
        # self.setMinimumSize(1920, 1080)

        configure_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../config/locale"
        self.conf = ConfigureStringSingle(configure_file_path, 'facemask')

        self.setAutoFillBackground(True)
        self._set_backgroundImage()
        self._setup_layout()

        self.config_strings()

    def config_strings(self):
        self.counterWidget.config_string(self.conf)
        self.titleWidget.config_string(self.conf)

    # Public
    def update_warecount(self, count):
        self.counterWidget.update_warecount(count)

    def update_unwarecount(self, count):
        self.counterWidget.update_unwarecount(count)
        self.unwareCountSignal.emit(count)

    def update_confidence(self, level):
        self.face_mask_prop.confidence_set(level)

    def _set_backgroundImage(self):
        palette = QPalette()
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "img_bg.png")
        pixmap = QPixmap(icon_path)
        # fitPixmap = pixmap.scaled(1920, 1080, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(self.backgroundRole(), QBrush(pixmap))
        self.setPalette(palette)

    def _setup_layout(self):

        contentLayout = QVBoxLayout()
        contentLayout.setContentsMargins(0,0,0,0)
        # 顶部布局
        topLayout = QHBoxLayout()

        self.titleWidget = FacemaskTitleWidget()
        self.titleWidget.closeSignal.connect(self._close_action)
        topLayout.addWidget(self.titleWidget, 1, Qt.AlignTop)

        # 中部布局
        self.middleLayout= self._setup_middle_layout()

        # 底部布局
        self.bottomLayout = self._setup_bottom_layout()

        # layout
        self.bottomLayout.addSpacing(70)
        contentLayout.addLayout(topLayout)
        # contentLayout.addSpacing(40)
        contentLayout.addLayout(self.middleLayout)
        contentLayout.addLayout(self.bottomLayout)
        contentLayout.addStretch()

        self.setLayout(contentLayout)

    def _setup_bottom_layout(self):
        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(180,44,0,0)
        layout1 = QVBoxLayout()

        layout11 = QHBoxLayout()
        title = QLabel()
        font = QFont()
        font.setBold(True)
        font.setPixelSize(20)
        font.setFamily('Source Han Sans CN')
        font.setWeight(QFont.Bold)
        title.setFont(font)
        title.setText(self.conf.get_value_for_key("k_unware_record"))
        palette = QPalette()
        palette.setColor(title.foregroundRole(), QColor(255, 255, 255))
        title.setPalette(palette)
        title.setContentsMargins(0, 0, 0, 2)

        self.unwareListWidget = FacemaskUnwareListWidget()
        # self.unwareListWidget.setMinimumWidth(1000)
        self.unwareListWidget.setFixedWidth(780)
        layout11.addWidget(title, 0, Qt.AlignLeft | Qt.AlignTop)
        layout1.addLayout(layout11)
        layout1.addSpacing(18)
        layout1.addWidget(self.unwareListWidget, 0, Qt.AlignLeft | Qt.AlignTop)

        layout2 = QVBoxLayout()
        self.voiceBtn = self._init_voice_btn()
        layout2.addWidget(self.voiceBtn, 0, Qt.AlignRight | Qt.AlignBottom)

        bottomLayout.addLayout(layout1)
        bottomLayout.addLayout(layout2)

        import tkinter
        win = tkinter.Tk()
        if win.winfo_screenwidth() < 1920:
            bottomLayout.addSpacing(90)

        return bottomLayout

    def _init_voice_btn(self):

        label = UClickableLabel()
        self.voiceOnPath = os.path.join(os.path.dirname(__file__), "resource/images", "ic_yuyinbobao.png")
        self.voiceOffPath = os.path.join(os.path.dirname(__file__), "resource/images", "ic_yuyinbobao_close.png")
        pix = QPixmap(self.voiceOffPath)
        label.setPixmap(pix)
        label.resize(120,120)
        label.clicked.connect(self._click_voice_btn)
        return label

    def _setup_middle_layout(self):

        # 中部布局
        middleLayout = QHBoxLayout()

        # camera area
        self._setup_camera_widget()

        # line
        self.line = QWidget()
        self.line.setFixedWidth(1)
        self.line.setFixedHeight(self.cameraWidget.height())

        palette = QPalette()
        palette.setColor(self.line.backgroundRole(), QColor(120, 132, 147, 70))
        self.line.setAutoFillBackground(True)
        self.line.setPalette(palette)

        # function area
        functionArea = QWidget()
        # 置信度设置区域
        self.confidenceWidget = FacemaskConfidenceWidget(self.parent)
        self.confidenceWidget.confidenceSignal.connect(self._notify_slider_value_changed)
        # 口罩数量显示区域
        self.counterWidget = FacemaskCounterWidget()

        middleVLayout = QVBoxLayout()
        middleVLayout.setContentsMargins(0,0,0,0)
        middleVLayout.addWidget(self.confidenceWidget, 1)
        middleVLayout.addWidget(self.counterWidget, 1)
        functionArea.setLayout(middleVLayout)

        # layout
        middleLayout.addSpacing(180)
        middleLayout.addWidget(self.cameraWidget, 1)
        middleLayout.addSpacing(50)
        middleLayout.addWidget(self.line, 1)
        middleLayout.addSpacing(50)
        middleLayout.addWidget(functionArea, 1)
        middleLayout.addSpacing(320)
        middleLayout.addStretch()

        return middleLayout

    def _setup_camera_widget(self):

        self.cameraWidget = FacemaskCameraWidget()
        self.cameraWidget.setFixedSize(640, 480)
        # self._loop_dect_image()

        path = os.path.join(os.path.dirname(__file__), "resource/images")
        common_path = os.path.join(os.path.dirname(__file__), "../../common/resource/font")

        title1 = self.conf.get_value_for_key("k_ware_title")
        title2 = self.conf.get_value_for_key("k_unware_title")

        self.face_mask_prop = FaceMaskProp(FacemaskConfig.DEFAULT_CONFIDENCE_LEVEL, (title1, title2), path = path, common_path = common_path)

    def update_detected_results(self, img_raw, result):

        self.face_mask_prop.fill_data(img_raw, result.result_data)
        # 实时图片
        image = self.face_mask_prop.make_img()

        pixmap = self.img2pixmap(image)
        QPixmapCache.clear()
        self.cameraWidget.icon.setPixmap(pixmap)
        # 统计人脸
        face_mask, face_nomask = self.face_mask_prop.face_static()
        self.update_warecount(face_mask)
        self.update_unwarecount(face_nomask)

        # 未戴口罩列表
        result = self.face_mask_prop.pics_get()
        currentTime = time.time()
        if self.last_unware_count == face_nomask:
            return

        if currentTime - self.last_update_time < 1:
            return

        self.last_update_time = currentTime
        self.last_unware_count = face_nomask
        self.listCacheSignal.emit(result)

    def update_unware_list(self, result):
        self.unwareListWidget.refresh(result)

    def img2pixmap(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0],
                          QImage.Format_RGB888)
        qt_image = QPixmap.fromImage(qt_image)
        pixmap = QPixmap(qt_image)
        return pixmap

    def _notify_slider_value_changed(self, value):
        self.confidenceLevelSignal.emit(value)

    def _click_voice_btn(self):
        self.voiceOn = not self.voiceOn
        if self.voiceOn:
            pix = QPixmap(self.voiceOnPath)
            self.voiceBtn.setPixmap(pix)
        else:
            pix = QPixmap(self.voiceOffPath)
            self.voiceBtn.setPixmap(pix)
        self.voiceSignal.emit(self.voiceOn)

    def _close_action(self):
        title = self.conf.get_value_for_key("k_quit_title")
        cancel_txt = self.conf.get_value_for_key("k_cancel")
        ok_txt = self.conf.get_value_for_key("k_quit")

        dialog = BaseDialogView(title=title,ok_txt=ok_txt,cancel_txt=cancel_txt,sure_button_action = self.emit_close,parent=self)
        dialog.show()

    def emit_close(self):
        self.closeSignal.emit()

