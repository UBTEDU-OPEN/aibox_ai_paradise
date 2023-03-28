#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_presenter.py
# Created   : 2020/5/27 3:35 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
import cv2
import os
import logging
from view.facemask_container_widget import *
from voice_prompt_manager import VoicePromptManager
import sys
import time
from PyQt5.QtCore import QThread, QObject

class FacemaskPresenter(object):
    voicePromptManager = VoicePromptManager()
    modelLoadFinishSignal = pyqtSignal()

    def __init__(self, view, model, solver, camera_func, load_model_func, close_func, show_img, cache_func):
        self.model = model
        self.view = view
        self.solver = solver
        self.view.voiceSignal.connect(self._voice_action)
        self.view.closeSignal.connect(close_func)
        self.view.confidenceLevelSignal.connect(self._confidence_changed)
        self.view.unwareCountSignal.connect(self._update_unware_count)
        self.view.listCacheSignal.connect(cache_func)

        self.thread = CameraHandleThread(self.solver)
        self.thread.trigger.connect(show_img)
        self.thread.camera_error_signal.connect(camera_func)
        # self.thread.load_model_signal.connect(load_model_func)
        self.thread.start()

    def show_img(self, ret, img_raw, result):
        if ret:
            self.view.update_detected_results(img_raw, result)
            # 成功后，隐藏loading

    def _update_unware_count(self, count):
        self.voicePromptManager.set_change_count(count)

    def _voice_action(self, ret):
        logging.debug('receieved: _voice_action')
        logging.debug(ret)
        self.model.voiceMute = ret
        self.voicePromptManager.set_on(self.model.voiceMute)

    def release(self):
        self.voicePromptManager.set_on(False)
        self.thread.flag = False
        self.thread.release()

    def _confidence_changed(self, level):
        self.model.confidenceLevelSignal = level
        self.view.update_confidence(self.model.confidenceLevelSignal)


from PyQt5.QtCore import pyqtSignal, QThread


class CameraHandleThread(QThread):
    trigger = pyqtSignal(bool, object, object)
    camera_error_signal = pyqtSignal()
    # load_model_signal = pyqtSignal()

    def __init__(self, model):
        super(CameraHandleThread, self).__init__()
        self.model = model
        from common.utility.common_utility import CommonUtil

        logging.debug('open camera')
        self.camera = CommonUtil.get_camera()
        if self.camera.isOpened():
            logging.debug("camera can open")
            # flag = self.cap.open(self.CAM_NUM)
            flag = True
            if not flag:
                logging.debug("camera open fail")
                self.flag = False
            else:
                logging.debug("camera open success")
                self.flag = True
        else:
            logging.debug("camera can't open")
            self.flag = False

    def release(self):
        logging.debug('CameraHandleThread release')
        self.flag = False
        # self.camera.release()
        cv2.destroyAllWindows()
        self.model.unload()

    def run(self):

        while True:
            if self.flag:
                # camera_open = os.popen("ls -ltrh /dev/video*").read()
                # if camera_open is '':
                #     print('can not read camera device')
                #     self.camera_error_signal.emit()
                #     self.camera.release()
                #     self.flag = False
                #     cv2.destroyAllWindows()
                #     break
                ret, img_raw = self.camera.read()
                if ret and img_raw is not None:
                    result = self.model.detect_face_mask(img_raw)
                    self.trigger.emit(ret, img_raw, result)
                    # self.load_model_signal.emit()
                else:
                    logging.debug('camera error')
                    self.camera_error_signal.emit()
                    self.camera.release()
                    self.flag = False
                    cv2.destroyAllWindows()
                    break
            else:
                logging.debug('flag false handle')
                self.camera_error_signal.emit()
                self.camera.release()
                cv2.destroyAllWindows()
                break
        # self.camera.release()
        # self.model.unload()
