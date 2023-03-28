#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:yanshee_pose_imitate_demo.py
# Created:2021/5/25 下午16:01
# Author:zzj
# CopyRight 2021-2021 Ubtech Robotics Corp. All rights reserved.
# Description:yanshee姿态模仿演示入口
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

sys.path.append('..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common.ui.loading.load import Load
from common.ui.commonDialog.BaseDialog import BaseDialogView
from common.ui.commonDialog.AlertDialog import AlertDialogView
from common.utility.common_utility import CommonUtil
from common.utility.configure_string_single import ConfigureStringSingle
from view.pose_net_view import PoseNetView

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.init_font()
        self.show_load()
        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()

        self.close_dialog = None
        self.exit_dialog = None
        self.loss_dialog = None

        self.view = PoseNetView(self)
        self.model = None
        self.presenter = None

        self.handle()
        self.view.signal_show_full.connect(self.enterPlayMode)

    def show_load(self):
        self.load = Load()

    def dismiss_load(self):
        self.load.dismiss()

    def handle(self):
        self.thread = MThread(self.model)
        self.thread.trigger.connect(self.show_main)
        self.thread.start()

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
        self.presenter.load_model()

    def show_main(self, model):
        self.model = model
        from presenter.pose_net_presenter import PoseNetPresenter
        self.presenter = PoseNetPresenter(self.model, self.view, self.handle_error, self.show_devices_loss_dialog)
        self.dismiss_load()

    def init_font(self):
        if ("Source Han Sans CN" not in QFontDatabase().families()) and (
                "思源黑体 CN" not in QFontDatabase().families()):
            QFontDatabase.addApplicationFont("resource/SourceHanSansCN-Bold.otf")
            QFontDatabase.addApplicationFont("resource/SourceHanSansCN-Regular.otf")

    def show_devices_loss_dialog(self):
        if self.loss_dialog is None:
            title = self.common_cfg.get_value_for_key("ubt_yanshee_pose_devices_loss_alert")
            txt = self.common_cfg.get_value_for_key("ubt_know")
            self.loss_dialog = AlertDialogView(title=title, button_txt=txt, parent=self)
        self.view.dialog.close()
        self.loss_dialog.show()

    def show_exit(self):
        if self.exit_dialog is None:
            self.exit_dialog = BaseDialogView(sure_button_action=self.do_exit, parent=self)
        self.exit_dialog.show()

    def do_exit(self):
        self.close()
        if self.presenter is not None:
            self.presenter.release()
        sys.exit(0)
        # qApp.quit()

    def showEvent(self, e) -> None:
        CommonUtil.contol_cpu_wake(True)

    def closeEvent(self, e) -> None:
        CommonUtil.contol_cpu_wake(False)

    def changeEvent(self, e: QtCore.QEvent) -> None:
        if self.isActiveWindow():
            CommonUtil.contol_cpu_wake(True)
        else:
            CommonUtil.contol_cpu_wake(False)

    def enterPlayMode(self):
        self.presenter.setFullCamera(self.view.dialog_ui.lb_camera_full)
        import tkinter
        win = tkinter.Tk()
        winWidth = win.winfo_screenwidth()
        winHeight = win.winfo_screenheight()
        print(f'enterPlayMode winWidth = {winWidth}, winHeight = {winHeight}')
        self.view.dialog_ui.widget.resize(winWidth, winHeight)
        self.view.dialog_ui.lb_camera_full.resize(winWidth, winHeight)
        # self.view.dialog.resize(winWidth, winHeight)
        self.showFullScreen()
        self.view.dialog.showFullScreen()
        self.view.dialog.exec()


class MThread(QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self, model):
        super(MThread, self).__init__()
        self.model = model

    def run(self):
        from model.pose_net_model import PoseNetModel
        self.model = PoseNetModel()
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
