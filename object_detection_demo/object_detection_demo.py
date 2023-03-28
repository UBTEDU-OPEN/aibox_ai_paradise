#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:ObjectDetection.py
# Created:2020/5/26 下午7:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:智能盘点入口
import os
import sys
import threading

sys.path.append('..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common.ui.commonDialog.BaseDialog import BaseDialogView
from common.utility.common_utility import CommonUtil
from common.utility.configure_string_single import ConfigureStringSingle

import time

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget

from view.object_view import ObView
from common.ui.loading.load import Load
from PyQt5 import QtCore


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.init_font()
        self.show_load()
        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()

        self.close_dialog = None
        self.exit_dialog = None

        self.view = ObView(self)
        self.model = None
        self.presenter = None
        self.load_model()

    def show_load(self):
        self.load = Load()

    def dismiss_load(self):
        self.load.dismiss()

    def load_model(self):
        print('load_model', threading.get_ident())
        self.thread = MThread(self.model)
        self.thread.trigger.connect(self.show_main)
        self.thread.start()

    def show_main(self, model):
        # self.view = ObView(self)
        print('show_main', threading.get_ident())
        if model is None:
            self.handle_error()
            return
        else:
            self.model = model
        from presenter.object_presenter import ObPresenter
        if self.presenter is None:
            self.presenter = ObPresenter(self.model, self.view, self.handle_error, self.show_img)
        else:
            self.presenter.check_run()
        # self.presenter = ObPresenter(self.model, self.view, self.handle_error, self.show_img)
        # self.presenter.camera_error_signal.connect(self.handle_error)
        self.showFullScreen()
        self.dismiss_load()

    def show_img(self, image, keys):
        self.presenter.show_img(image, keys)

    def handle_error(self):
        # camera open failed
        print('handle_error')
        if self.close_dialog is None:
            title = self.common_cfg.get_value_for_key("ubt_load_error")
            left_txt = self.common_cfg.get_value_for_key("ubt_reload")
            right_txt = self.common_cfg.get_value_for_key("ubt_quit")
            title = title.replace("\\n", "\n")
            self.close_dialog = BaseDialogView(title, left_txt, right_txt, self.reload, self.do_exit,
                                               parent=self)
        self.close_dialog.show()
        self.dismiss_load()

    def reload(self):
        self.show_load()
        self.load_model()

    def init_font(self):
        if ("Source Han Sans CN" not in QFontDatabase().families()) and (
                "思源黑体 CN" not in QFontDatabase().families()):
            QFontDatabase.addApplicationFont("resource/SourceHanSansCN-Bold.otf")
            QFontDatabase.addApplicationFont("resource/SourceHanSansCN-Regular.otf")

    def show_exit(self):
        if self.exit_dialog is None:
            self.exit_dialog = BaseDialogView(sure_button_action=self.do_exit, parent=self)
        self.exit_dialog.show()

    def do_exit(self):
        self.close()
        self.presenter.release()
        self.model.unload()
        sys.exit(0)

    def showEvent(self, e) -> None:
        print('showEvent')
        CommonUtil.contol_cpu_wake(True)

    def closeEvent(self, e) -> None:
        print('closeEvent')
        CommonUtil.contol_cpu_wake(False)

    def changeEvent(self, e: QtCore.QEvent) -> None:
        if self.isActiveWindow():
            CommonUtil.contol_cpu_wake(True)
        else:
            CommonUtil.contol_cpu_wake(False)

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No,
    #                                  QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #         self.presenter.release()
    #     else:
    #         event.ignore()


class MThread(QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self, model):
        super(MThread, self).__init__()
        self.model = model

    def run(self):
        if self.model is None:
            from model.object_model import ObModel
            try:
                self.model = ObModel()
            except:
                print("load model error")
        else:
            time.sleep(2)
        self.trigger.emit(self.model)


def start():
    app = QApplication([])
    window = Window()
    window.resize(1920, 1080)
    app.processEvents()
    app.primaryScreen()
    window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start()