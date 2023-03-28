#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:style_transfer_demo.py
# Created:2020/9/14 下午16:18
# Author:zzj
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:风格迁移入口
import os
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

sys.path.append('..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common.ui.loading.load import Load
from common.ui.commonDialog.BaseDialog import BaseDialogView
from common.utility.common_utility import CommonUtil
from common.utility.configure_string_single import ConfigureStringSingle
from view.style_transfer_view import StyleTransferView

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

        self.view = StyleTransferView(self)
        self.model = None
        self.presenter = None

        self.handle()

    def show_load(self):
        self.load = Load()

    def dismiss_load(self):
        self.load.dismiss()

    def handle(self):
        self.thread = MThread(self.model)
        self.thread.trigger.connect(self.show_main)
        self.thread.start()

    def show_main(self, model):
        self.model = model
        from presenter.style_presenter import StylePresenter
        self.presenter = StylePresenter(self.model, self.view)
        self.dismiss_load()

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
        if self.presenter is not None:
            self.presenter.release()
        sys.exit(0)
        # qApp.quit()

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


class MThread(QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self, model):
        super(MThread, self).__init__()
        self.model = model

    def run(self):
        from model.style_model import StyleModel
        self.model = StyleModel()
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
