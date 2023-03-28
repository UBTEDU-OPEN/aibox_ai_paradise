#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : smart_photo_studio_demo.py
# Created   : 2021/7/5 3:59 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtCore import pyqtSlot
import time,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')
from common.ui.loading.load import Load
from common.utility.configure_string_single import ConfigureStringSingle
# import logging
# import logging.config

class Demo(QMainWindow):

    def __init__(self, parent = None):
        self.showLoading = False
        super(Demo, self).__init__(parent)
        self.exit = False
        self.solver = None

        from view.smart_photo_studio_view import SmartPhotoStudioContainer
        self.view = SmartPhotoStudioContainer(self)
        print(self.view.frameSize())
        self.setCentralWidget(self.view)

        self.show_load()

        configure_file_path = os.path.join(os.path.dirname(__file__), "config/locale")
        self.conf = ConfigureStringSingle(configure_file_path, 'smart_photo_studio_lang')

        self.load_model()

        from PyQt5.QtGui import QFontDatabase

        if 'Source Han Sans CN' not in QFontDatabase().families() and '思源黑体 CN' not in QFontDatabase().families():
            print('no font')
            QFontDatabase.addApplicationFont("common/resource/font/SourceHanSansCN-Bold.otf")
            QFontDatabase.addApplicationFont("common/resource/font/SourceHanSansCN-Regular.otf")
        else:
            print('font exists')

    def show_load(self):
        print('show loading' + str(time.time()))
        self.shownLoading = False
        self.load = Load(30 * 1000)

    def load_model(self):
        self.thread = MThread(self.solver)
        self.thread.trigger.connect(self.show_main)
        self.thread.start()

    def show_img(self, result):
        self.view.update_detected_results(result)

    def show_main(self, solver):
        self.dismiss_load()

        from presenter.smart_photo_studio_presenter import SmartPhotoStudioPresenter
        # from model.facemask_model import FacemaskModel
        #
        # model = FacemaskModel()
        # create presenter
        if solver is None:
            # logging.debug('----')
            self.handle_camera_error()
            return
        else:
            self.solver = solver
        self.presenter = SmartPhotoStudioPresenter(self.view, self.solver, camera_func = self.handle_camera_error,
                                           load_model_func = self.load_model_finish, close_func = self._close_window, show_img = self.show_img)
        # self.view.update_unware_list(self.list_cache.label_pics)

    @pyqtSlot()
    def handle_camera_error(self):

        from common.ui.commonDialog.BaseDialog import BaseDialogView

        if self.exit:
            print('application exit')
            return
        print('open_camera_failed')

        conf = ConfigureStringSingle.get_common_string_cfg()
        title = conf.get_value_for_key("ubt_load_error")
        cancel_txt = conf.get_value_for_key("ubt_quit")
        ok_txt = conf.get_value_for_key("ubt_reload")
        title = title.replace("\\n", "\n")
        dialog = BaseDialogView(title=title, ok_txt=ok_txt, cancel_txt=cancel_txt, sure_button_action=self.reload,
                                cancel_btn_action=self._close_window,
                                parent=self)
        dialog.show()

        self.dismiss_load()

    def reload(self):
        self.show_load()
        self.load_model()

    def load_model_finish(self):
        self.dismiss_load()

    def _close_window(self):
        print('close window')
        self.close()
        self.exit = True
        self.presenter.release()
        sys.exit(0)

    def dismiss_load(self):
        if not self.shownLoading:
            self.shownLoading = True
            self.load.dismiss()

from PyQt5.QtCore import QThread,pyqtSignal
from oneai.person_segmentation_solver import SegmentationSolver
class MThread(QThread):
    trigger = pyqtSignal(object)

    def __init__(self, solver):
        super(MThread, self).__init__()
        self.solver = solver

    def run(self):
        if self.solver is None:
            try:
                print('load model')
                self.solver = SegmentationSolver()
                self.solver.load()
                print('load model finish')
            except:
                print('load model error')

        else:
            print('model already loaded')
            time.sleep(2)
        self.trigger.emit(self.solver)

def qapp():
    if QApplication.instance():
        _app = QApplication.instance()
    else:
        _app = QApplication(sys.argv)
    return _app

def start():
    # from oneai.common.config.default_config import DeFaultConfig
    # log_path = os.path.expanduser("~") + "/.cache/oneai/"
    # if not os.path.exists(log_path):
    #     os.makedirs(log_path)
    # file_name = log_path + "smart_photo_studio_demo.log"
    # DeFaultConfig.log_conf['handlers']['file']['filename'] = file_name
    # logging.config.dictConfig(DeFaultConfig.log_conf)
    # logging.debug('smart_photo_studio demo start!')
    print('smart_photo_studio demo start!')

    app = qapp()
    window = Demo()
    window.resize(1920, 1080)
    app.processEvents()
    window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start()


