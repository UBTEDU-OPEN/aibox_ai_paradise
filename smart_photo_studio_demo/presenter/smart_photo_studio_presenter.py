#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_presenter.py
# Created   : 2021/7/5 4:30 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 
import cv2
import logging
class SmartPhotoStudioPresenter(object):

    def __init__(self, view, solver, camera_func, load_model_func, close_func, show_img):
        self.view = view
        self.solver = solver
        self.view.closeSignal.connect(close_func)
        # self.view.confidenceLevelSignal.connect(self._confidence_changed)
        # self.view.unwareCountSignal.connect(self._update_unware_count)

        self.thread = CameraHandleThread(self.solver)
        self.thread.trigger.connect(show_img)
        self.thread.camera_error_signal.connect(camera_func)
        # self.thread.load_model_signal.connect(load_model_func)
        self.thread.start()

    def release(self):
        if self.thread is not None:
            self.thread.flag = False
            self.thread.release()

from PyQt5.QtCore import pyqtSignal, QThread


class CameraHandleThread(QThread):
    trigger = pyqtSignal(object)
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

    def make_image(self,mask, img_raw, back_image):

        # person = img_raw
        #
        # back_image = back_image[0:480, 0:480]
        #
        # person = person[0:480, 80:560]
        # mask = cv2.resize(mask, (480, 480))
        #
        # back_image = cv2.cvtColor(back_image, cv2.COLOR_RGB2GRAY)
        #
        # scenic_mask = ~mask
        # scenic_mask = scenic_mask / 255.0
        # back_image[:, :, 0] = back_image[:, :, 0] * scenic_mask
        # back_image[:, :, 1] = back_image[:, :, 1] * scenic_mask
        # back_image[:, :, 2] = back_image[:, :, 2] * scenic_mask
        #
        # mask = mask / 255.0
        # person[:, :, 0] = person[:, :, 0] * mask
        # person[:, :, 1] = person[:, :, 1] * mask
        # person[:, :, 2] = person[:, :, 2] * mask
        #
        # result = cv2.add(back_image, person)

        return back_image

    def run(self):

        import os
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

                # icon_path = os.path.join(os.path.dirname(__file__), "./", "abc123456.png")
                # blank = cv2.imread(icon_path,cv2.IMREAD_UNCHANGED)
                if ret and img_raw is not None:
                    self.model.segment_person(img_raw)
                    result = self.model.make_alpha_image()
                    self.trigger.emit(result)
                    # self.load_model_signal.emit()
                    pass
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