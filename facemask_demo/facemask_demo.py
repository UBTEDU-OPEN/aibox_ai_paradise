#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_demo.py
# Created   : 2020/5/29 4:40 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtCore import pyqtSlot
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')
from common.ui.loading.load import Load
from common.utility.common_utility import CommonUtil
from common.utility.configure_string_single import ConfigureStringSingle

import logging
import logging.config

class Demo(QMainWindow):

    def __init__(self, parent = None):
        self.shownLoading = False
        super(Demo, self).__init__(parent)
        self.exit = False
        self.solver = None

        from view.facemask_container_widget import FacemaskContainerWidget
        self.view = FacemaskContainerWidget(self)
        self.setCentralWidget(self.view)
        # self.window = QMainWindow()

        from model.facemask_list_cache import FacemaskListCache
        self.list_cache = FacemaskListCache()

        self.show_load()

        configure_file_path = os.path.dirname(os.path.realpath(__file__)) + "/config/locale"
        self.conf = ConfigureStringSingle(configure_file_path, 'facemask')

        self.load_model()

        from PyQt5.QtGui import QFontDatabase

        if 'Source Han Sans CN' not in QFontDatabase().families() and '思源黑体 CN' not in QFontDatabase().families():
            logging.debug('no font')
            QFontDatabase.addApplicationFont("common/resource/font/SourceHanSansCN-Bold.otf")
            QFontDatabase.addApplicationFont("common/resource/font/SourceHanSansCN-Regular.otf")
        else:
            logging.debug('font exists')

    def _cache_func(self, result):
        self.list_cache.set_pic(result)
        self.view.update_unware_list(self.list_cache.label_pics)

    def show_load(self):
        logging.debug('show loading' + str(time.time()))
        self.shownLoading = False
        self.load = Load(40 * 1000)

    def load_model(self):
        self.thread = MThread(self.solver)
        self.thread.trigger.connect(self.show_main)
        self.thread.start()

    def show_img(self, ret, img_raw, result):
        if ret:

            self.presenter.show_img(ret, img_raw, result)
            self.load_model_finish()

    def show_main(self, solver):

        from presenter.facemask_presenter import FacemaskPresenter
        from model.facemask_model import FacemaskModel

        model = FacemaskModel()
        # create presenter
        if solver is None:
            logging.debug('----')
            self.handle_camera_error()
            return
        else:
            self.solver = solver
        self.presenter = FacemaskPresenter(self.view, model, self.solver, camera_func = self.handle_camera_error,
                                           load_model_func = self.load_model_finish, close_func = self._close_window, show_img = self.show_img, cache_func = self._cache_func)
        self.view.update_unware_list(self.list_cache.label_pics)
        # self.parent.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)

    @pyqtSlot()
    def handle_camera_error(self):

        from common.ui.commonDialog.BaseDialog import BaseDialogView

        if self.exit:
            logging.debug('application exit')
            return
        logging.debug('open_camera_failed')


        conf = ConfigureStringSingle.get_common_string_cfg()
        title = conf.get_value_for_key("ubt_load_error")
        cancel_txt = conf.get_value_for_key("ubt_quit")
        ok_txt = conf.get_value_for_key("ubt_reload")
        title = title.replace("\\n", "\n")
        dialog = BaseDialogView(title=title, ok_txt=ok_txt, cancel_txt=cancel_txt, sure_button_action=self.reload,cancel_btn_action=self._close_window,
                                parent=self)
        dialog.show()


        self.dismiss_load()
        # self.hide()

    def reload(self):
        self.show_load()
        self.load_model()

    def load_model_finish(self):
        self.dismiss_load()
        # self.presenter.thread.load_model_signal.disconnect(self.load_model_finish)
        # self.show()

    def _close_dialog(self):
        self.load.dismiss()
        self.close()

    def _close_window(self):
        logging.debug('close window')
        self.close()
        self.exit = True
        self.presenter.release()
        sys.exit(0)

    def dismiss_load(self):
        if not self.shownLoading:
            self.shownLoading = True
            self.load.dismiss()

    def closeMainWindow(self):
        logging.debug('closeMainWindow')

    def start_detect(self):
        self.presenter.start_detect()

    def showEvent(self, e) -> None:
        print('showEvent')
        CommonUtil.contol_cpu_wake(True)

    def closeEvent(self, e) -> None:
        print('closeEvent')
        CommonUtil.contol_cpu_wake(False)

    def changeEvent(self, e) -> None:
        if self.isActiveWindow():
            CommonUtil.contol_cpu_wake(True)
        else:
            CommonUtil.contol_cpu_wake(False)

from PyQt5.QtCore import QThread,pyqtSignal
from oneai.mask_detection_solver import MaskDetectionSolver
class MThread(QThread):
    trigger = pyqtSignal(object)

    def __init__(self, solver):
        super(MThread, self).__init__()
        self.solver = solver

    def run(self):
        if self.solver is None:
            try:
                logging.debug('load model')
                self.solver = MaskDetectionSolver()
                self.solver.load()
                logging.debug('load model finish')
            except:
                logging.debug('load model error')

        else:
            logging.debug('model already loaded')
            time.sleep(2)
        self.trigger.emit(self.solver)

def qapp():
    if QApplication.instance():
        _app = QApplication.instance()
    else:
        _app = QApplication(sys.argv)
    return _app


def start():
    from oneai.common.config.default_config import DeFaultConfig
    log_path = os.path.expanduser("~") + "/.cache/oneai/"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_name = log_path + "facemask_demo.log"
    DeFaultConfig.log_conf['handlers']['file']['filename'] = file_name
    logging.config.dictConfig(DeFaultConfig.log_conf)
    logging.debug('facemask demo start!')

    app = qapp()
    window = Demo()
    window.resize(1920, 1080)
    app.processEvents()
    window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start()
