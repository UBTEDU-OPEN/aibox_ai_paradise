#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_view.py
# Created   : 2021/7/5 4:18 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import sys,os
import cv2

from PIL.ImageQt import ImageQt

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QPixmapCache
from smart_photo_studio_title import SmartPhotoStudioTitle
from smart_photo_studio_select import SmartPhotoStudioSelect
from smart_photo_studio_camera import SmartPhotoStudioCamera
from clickable_label import UClickableLabel

sys.path.append('..')
sys.path.append('..')
from common.utility.configure_string_single import ConfigureStringSingle
from common.ui.commonDialog.BaseDialog import BaseDialogView
from PIL import Image
from functools import wraps

def opera_interceptor(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        o = args[0]
        # print('state', o.produce_result_state)
        if not o.produce_result_state == 1:
            return func(*args, **kwargs)

    return wrap

class SmartPhotoStudioContainer(QWidget):
    closeSignal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.produce_result_state = 2
        self.parent = parent

        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()
        configure_file_path = os.path.join(os.path.dirname(__file__), "../", "config/locale")
        self.conf = ConfigureStringSingle(configure_file_path, 'smart_photo_studio_lang')

        self.setAutoFillBackground(True)
        self._set_backgroundImage()
        self._setup_layout()

        self.config_strings()

    def config_strings(self):
        # self.counterWidget.config_string(self.conf)
        self.titleWidget.config_string(self.conf)
        self.selectWidget.config_string(self.conf)

    def _set_backgroundImage(self):
        palette = QPalette()
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "img_bg.png")
        pixmap = QPixmap(icon_path)
        # fitPixmap = pixmap.scaled(1920, 1080, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(self.backgroundRole(), QBrush(pixmap))
        self.setPalette(palette)

    def _setup_layout(self):
        contentLayout = QVBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        # 顶部布局
        topLayout = QHBoxLayout()

        self.titleWidget = SmartPhotoStudioTitle()
        self.titleWidget.closeSignal.connect(self._close_action)
        topLayout.addWidget(self.titleWidget, 1, Qt.AlignTop)

        # 中部布局

        middleLayout = QHBoxLayout()
        self.selectWidget = SmartPhotoStudioSelect()
        self.selectWidget.setFixedHeight(106)
        self.selectWidget.selectImageSignal.connect(self._select_image)
        self.selectWidget.saveSignal.connect(self._click_save)

        middleLayout.addWidget(self.selectWidget, 1, Qt.AlignTop)
        #
        # 底部布局
        self.cameraWidget = self._setup_camera_widget()
        bottomLayout = QVBoxLayout()
        bottomLayout.addWidget(self.cameraWidget, 1, Qt.AlignHCenter)
        bottomLayout.addSpacing(20)
        self.captureBtn = self._init_capture_btn()
        bottomLayout.addWidget(self.captureBtn, 1, Qt.AlignHCenter)

        #
        # # layout
        # self.bottomLayout.addSpacing(70)
        contentLayout.addLayout(topLayout)
        contentLayout.addSpacing(40)
        contentLayout.addLayout(middleLayout)
        contentLayout.addSpacing(20)
        contentLayout.addLayout(bottomLayout)
        contentLayout.addStretch()

        self.setLayout(contentLayout)

        # 全部初始化完成之后，设置默认图片
        self.selectWidget.selectDefaultIndex()

    def _init_capture_btn(self):
        icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_take_picture.png")
        icon_press_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_take_picture.png")
        icon_disable_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_take_picture_disable.png")

        btn = UClickableLabel(normal_pixmap=QPixmap(icon_path), pressed_pixmap=QPixmap(icon_press_path),disable_pixmap=QPixmap(icon_disable_path))
        btn.setFixedSize(100, 100)
        btn.clicked.connect(self._click_capture_btn)
        return btn

    def _click_capture_btn(self):
        self.cameraWidget.show_preview()

    def _select_image(self, image):
        self.cameraWidget.update_bg(image)


    def _setup_camera_widget(self):

        cameraWidget = SmartPhotoStudioCamera()
        cameraWidget.captureStatusChangeSignal.connect(self._notify_preview)
        return cameraWidget

    def _notify_preview(self, ret):
        self.captureBtn.setEnabled(ret)
        enable = not ret
        self.selectWidget.saveBtn.setEnabled(enable)

    def update_detected_results(self, result):

        pixmap = self.img2pixmap(result)
        QPixmapCache.clear()
        self.cameraWidget.update_camera(pixmap)


    def img2pixmap(self, image):

        result = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))
        qtimage = ImageQt(result)
        result_image = QPixmap.fromImage(qtimage)
        pixmap = QPixmap(result_image)

        return pixmap

    def _close_action(self):
        title = self.conf.get_value_for_key("k_quit_title")
        cancel_txt = self.conf.get_value_for_key("k_cancel")
        ok_txt = self.conf.get_value_for_key("k_quit")

        dialog = BaseDialogView(title=title,ok_txt=ok_txt,cancel_txt=cancel_txt,sure_button_action = self.emit_close,parent=self)
        dialog.show()

    def emit_close(self):
        self.closeSignal.emit()

    def _click_save(self):
        print('save---')
        self.save()

    @opera_interceptor
    def save(self, filepath='/home/oneai/smart_photo'):
        if not self.produce_result_state == 2:
            print('saving in progress')
            return
        self.produce_result_state = 1
        import numpy as np
        title = self.conf.get_value_for_key("k_title")
        file_name = f'{title}.jpg'

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        target_file = self.get_file_name(filepath, file_name)

        file, suffix = QFileDialog.getSaveFileName(self, self.common_cfg.get_value_for_key('ubt_style_file_save'),
                                                   target_file[:-4], '.jpg;;.png')
        self.produce_result_state = 2
        result = file + suffix
        if not len(result) == 0:

            #截屏时候，隐藏按钮
            self.titleWidget.closeBtn.hide()
            self.titleWidget.icon.hide()
            self.selectWidget.hide()
            self.cameraWidget.preview.closeBtn.hide()
            self.captureBtn.hide()
            # threading.Thread(target=self.real).start()
            self.grab().save(result)

            data = np.array(Image.open(result))
            print(data.shape)
            data[200:883, :, :] = data[350:1033, :, :]
            im = Image.fromarray(data[0:883, :, :])
            im.save(result)

            self.titleWidget.closeBtn.show()
            self.titleWidget.icon.show()
            self.selectWidget.show()
            self.cameraWidget.preview.closeBtn.show()
            self.captureBtn.show()

            self.cameraWidget.show_preview()
            self.selectWidget.saveBtn.setEnabled(False)
        else:
            #点击取消
            self.cameraWidget.show_preview()
            self.selectWidget.saveBtn.setEnabled(False)


    def get_file_name(self, file_path, file_name):
        str_copy = self.common_cfg.get_value_for_key('ubt_style_copy')
        f = os.path.join(file_path, file_name)
        num = -1
        try:
            if os.path.exists(f):
                files = os.listdir(file_path)
                for sf in files:
                    if file_name[:-4] in sf:
                        left = sf[:-4].replace(file_name[:-4], "")
                        if left == "":
                            if num == -1:
                                num = 0
                        else:
                            tmp = int(left[len(str_copy) + 1:])
                            if tmp > num:
                                num = tmp
        except:
            pass
        finally:
            if num == -1:
                return f
            else:
                str_list = list(f)
                content = f'-{str_copy}{str(num + 1)}'
                str_list.insert(-4, content)
                return "".join(str_list)
