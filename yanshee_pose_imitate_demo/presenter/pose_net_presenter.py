#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import cv2

import threading

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtGui import QImage
from oneai.posenet_solver import PosenetDetectResult

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from view.pose_net_view import PoseNetView
from presenter.udpbrocaster import StartdiscoveryDevice
from model.pose_net_model import PoseNetModel
from common.utility.common_utility import CommonUtil
from functools import wraps
from time import sleep

def send_interceptor(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        o = args[0]
        print('interceptor_devices', o.view.latest_devices)
        if not len(o.view.latest_devices) == 0:
            return func(*args, **kwargs)
    return wrap


class PoseNetPresenter(QObject):

    def __init__(self, model: PoseNetModel, view: PoseNetView, handle_error, show_devices_loss_dialog):
        super().__init__()
        self.model = model
        self.view = view
        self.handle_error = handle_error
        self.view.setSingal(self.initial, self.reset, self.do_send_stop, self.do_send_start1, self.do_send_start2, show_devices_loss_dialog)
        self.camera_img = view.widget.camera
        self.camera_img_full = None
        self.load_thread = None
        self.thread = None
        self.discovery = None
        self.has_show = False
        self.find_device()
        import tkinter
        # 全屏展示
        win = tkinter.Tk()
        self.winWidth = win.winfo_screenwidth()
        self.winHeight = win.winfo_screenheight()
        print(f'PoseNetPresenter winWidth = {self.winWidth}, winHeight = {self.winHeight}')

    def find_device(self):
        self.discovery = StartdiscoveryDevice(self.call_back)

    def call_back(self, data):
        print(f'yanshee_device:{data}')
        self.view.update_device_list(data.keys())

    def initial(self):
        self.load_model()

    def load_model(self):
        self.load_thread = LoadModelThread(self.model)
        self.load_thread.trigger.connect(self.load_finish)
        self.load_thread.start()

    def load_finish(self):
        # self.view.widget.motion_stack.setCurrentIndex(1)
        # self.view.start_timer()
        self.thread = CameraHandleThread(self.model)
        self.thread.trigger.connect(self.show_img)
        self.thread.camera_error_signal.connect(self.error)
        self.thread.start()

    def reset(self):
        pass

    @send_interceptor
    def do_send_stop(self):
        self.discovery.udp_send_start('stop')

    @send_interceptor
    def do_send_start1(self):
        self.discovery.udp_send_start('start1')

    def do_send_start2(self):
        self.discovery.udp_send_start('start2')

    def send_data_yanshee(self, result):
        # print(f'result_data:{result.result_data}')
        camera = self.thread.cap
        result_new = []
        max_result = 0
        k = -1
        ll = len(result.result_data)
        if ll > 0:
            for i in range(ll):
                if (result.result_data[i][0][1][0] > camera.get(3) / 3) and (
                        result.result_data[i][0][1][0] < 2 * camera.get(3) / 3):
                    if (result.result_data[i][0][5][0] > 0) and (result.result_data[i][0][2][0] > 0):
                        if abs(result.result_data[i][0][5][0] - result.result_data[i][0][2][0]) > camera.get(3) / 8:
                            if abs(result.result_data[i][0][5][0] - result.result_data[i][0][2][0]) > max_result:
                                max_result = int(abs(result.result_data[i][0][5][0] - result.result_data[i][0][2][0]))
                                k = i
            if k != -1:
                print(result.result_data[k][0])
                result_new.append(result.result_data[k])
                ok = result.result_data[k][0]
                data = sum(ok, [])
                str_data = str(data).strip("[]")
                if len(str_data) > 0:
                    self.discovery.udp_send_posture_data(str_data)
        return result_new

    def show_img(self, result):
        # image = result.make_image()
        if not self.has_show:
            self.has_show = True
            # self.view.widget.motion_stack.setCurrentIndex(1)
            self.view.start_timer()

        result_new = self.send_data_yanshee(result)
        no = PosenetDetectResult(result_new, result.image)
        image = no.make_image()
        # 小窗展示
        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show_img = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.camera_img.setPixmap(QtGui.QPixmap.fromImage(show_img))
        show_full = cv2.resize(image, (self.winWidth, self.winHeight))
        show_full = cv2.cvtColor(show_full, cv2.COLOR_BGR2RGB)
        show_img_full = QImage(show_full.data, show_full.shape[1], show_full.shape[0], QImage.Format_RGB888)
        if self.camera_img_full is not None:
            self.camera_img_full.setPixmap(QtGui.QPixmap.fromImage(show_img_full))

    def error(self):
        print("camera error")
        self.handle_error()

    def release(self):
        """
        释放模型-》kill掉服务进程
        """
        if self.view.stopTimer() is True:
            sleep(3)
        if self.discovery is not None:
            self.do_send_stop()
            self.discovery.udp_close()
        if self.thread is not None:
            self.thread.flag = False
        threading.Thread(target=self.do_release).start()

    def do_release(self):
        if self.model is not None:
            self.model.unload()
            print('model release')

    def setFullCamera(self, camera_lable):
        self.camera_img_full = camera_lable


class LoadModelThread(QThread):
    trigger = QtCore.pyqtSignal()

    def __init__(self, model):
        super(LoadModelThread, self).__init__()
        self.model = model

    def run(self):
        if self.model.load():
            self.trigger.emit()


class CameraHandleThread(QThread):
    trigger = QtCore.pyqtSignal(object)
    camera_error_signal = QtCore.pyqtSignal()

    def __init__(self, model):
        super(CameraHandleThread, self).__init__()
        self.model = model
        self.threshold = 0.4
        self.CAM_NUM = 0
        self.cap = CommonUtil.get_camera()
        if self.cap.isOpened():
            print("camera can open")
            flag = True
            if not flag:
                print("camera open fail")
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
                result = self.model.detect_pose(frame)
                self.trigger.emit(result)
            else:
                self.camera_error_signal.emit()
                self.cap.release()
                cv2.destroyAllWindows()
                break

