#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:style_presenter.py
# Created:2020/9/23 下午3:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:风格迁移Presenter
import os
import sys

# import cv2
import threading

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtGui import QImage

# import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from view.style_transfer_view import StyleTransferView
from model.style_model import StyleModel


class StylePresenter(QObject):

    def __init__(self, model: StyleModel, view: StyleTransferView):
        super().__init__()
        self.model = model
        self.view = view
        self.view.setSingal(self.produce, self.release, )
        # self.view.produceSignal.connect(self.produce)
        self.product_img = view.widget.img_result
        # self.has_load = False
        self.thread = None
        self.model_sid_state = (-1, True)

    def produce(self, sid, img_path):
        """
        生成-》开线程初始化服务，加载并推理
        """
        need_reload_flag = True
        if sid == self.model_sid_state[0]:
            need_reload_flag = self.model_sid_state[1]
        self.thread = StyleThread(self.model, sid, img_path, need_reload_flag)
        self.thread.load_start_signal.connect(self.load_start)
        self.thread.show_signal.connect(self.show_view)
        self.thread.load_signal.connect(self.load_state)
        self.thread.start()

    def load_start(self):
        print('load_start')
        self.view.load_model()

    def load_state(self, sid):
        print("load_state_finish", sid)
        self.model_sid_state = (sid, False)
        self.view.load_model_finish()

    def show_view(self, show_img):
        print("show_view", show_img)
        self.view.show_result(show_img)

    def release(self):
        """
        释放模型-》kill掉服务进程
        """
        threading.Thread(target=self.do_release).start()

    def do_release(self):
        if self.model is not None:
            self.model.unload()
            print('model release')
            # self.has_load = False


class StyleThread(QThread):
    show_signal = QtCore.pyqtSignal(object)
    load_signal = QtCore.pyqtSignal(object)
    load_start_signal = QtCore.pyqtSignal()

    def __init__(self, model: StyleModel, sid, img_path, first_load):
        super(StyleThread, self).__init__()
        self.model = model
        self.sid = sid
        self.img_path = img_path
        self.first_load = first_load
        self.finish = False

    def run(self):
        print('load_flag', self.first_load)
        if self.first_load:
            self.load_start_signal.emit()
            # self.model.unload()
            self.model.load(style_id=self.sid)
            self.load_signal.emit(self.sid)
        out = self.model.transfer(self.img_path)
        if out is None:
            return
        show_img = QImage(out.data, out.shape[1], out.shape[0], QImage.Format_RGB888)
        self.show_signal.emit(show_img)
        self.finish = True
