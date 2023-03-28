#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:object_presenter.py
# Created:2020/5/26 下午7:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:智能盘点Presenter
import os
import sys

import cv2
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtGui import QImage

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from view.object_view import ObView
from common.utility.common_utility import CommonUtil


class ObPresenter(QObject):
    camera_error_signal = QtCore.pyqtSignal()

    def __init__(self, model, view: ObView, fun, show_img):
        self.model = model
        self.view = view
        self.setSignal()
        # self.view.updateGoodsSelectSignal.connect(self.update_select)
        # self.view.updateThreSholdSignal.connect(self.update_threshold)
        self.camera_img = view.widget.camera

        self.thread = CameraHandleThread(model)
        self.thread.trigger.connect(show_img)
        self.thread.camera_error_signal.connect(fun)
        self.thread.start()

    def setSignal(self):
        self.view.set_select_control(self.update_select, self.update_threshold)

    def update_select(self, goods):
        list = []
        for item in goods:
            list.append((item.flag, item.check_icon))
        # print(list)
        if self.model is not None:
            self.model.setobjects(list)

    def update_threshold(self, value):
        if value == 0:
            value = 0.1
        self.thread.threshold = value

    def show_img(self, image, keys):
        # print('show_img thread', threading.get_ident())
        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImg = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.camera_img.setPixmap(QtGui.QPixmap.fromImage(showImg))
        # print("size ",self.camera_img.size())
        self.view.update_goods_count(keys)

    def release(self):
        self.thread.flag = False

    def check_run(self):
        self.thread.check_loop()


class CameraHandleThread(QThread):
    trigger = QtCore.pyqtSignal(object, object)
    camera_error_signal = QtCore.pyqtSignal()

    def __init__(self, model):
        super(CameraHandleThread, self).__init__()
        self.model = model
        self.threshold = 0.4
        self.CAM_NUM = 0
        self.cap = CommonUtil.get_camera()
        if self.cap.isOpened():
            print("camera can open")
            # flag = self.cap.open(self.CAM_NUM)
            flag = True
            if not flag:
                print("camera open fail")
                # msg = QMessageBox.Warning(self, '相机打开异常', buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)
                self.flag = False
            else:
                print("camera open success")
                self.flag = True
        else:
            print("camera can't open")
            self.flag = False

    def run(self):
        while True:
            if self.flag:
                ret, frame = self.cap.read()
                if not ret:
                    print("camera read error")
                    self.camera_error_signal.emit()
                    break
                image, keys = self.model.detect(frame, self.threshold)
                self.trigger.emit(image, keys)
            else:
                self.camera_error_signal.emit()
                self.cap.release()
                cv2.destroyAllWindows()
                break

    def check_loop(self):
        self.cap = CommonUtil.get_camera()
        self.flag = self.cap.isOpened()
        print(f"camera check_loop:{self.flag}, run:{self.isRunning()}, finish:{self.isFinished()}")
        self.start()
