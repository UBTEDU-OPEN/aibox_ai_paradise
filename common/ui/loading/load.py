#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:load.py
# Created:2020/6/3 下午7:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:loadView
import os
import sys
import time
import random

from PyQt5.QtGui import QPalette, QBrush, QPixmap

from common.utility.configure_string_single import ConfigureStringSingle

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect
from PyQt5.QtWidgets import QWidget
from common.ui.loading.loading import Ui_Load


class Load(QWidget, Ui_Load):

    def __init__(self, timeout=30 * 1000, parent=None):
        # parent = QWidget()
        self.m_time_out = timeout
        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()
        self.parent = parent
        super().__init__(self.parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        self.widget = Ui_Load()
        self.widget.setupUi(self)
        self.init_ui()
        self.init_timeout()

        self.index = 0

        self.thread = LoadThread()
        self.thread.trigger.connect(self.show_load)
        self.thread.start()
        print('show load', time.time())

    def init_timeout(self):
        self.timer = QTimer()
        self.timer.setInterval(self.m_time_out)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.dismiss(str(self.m_time_out) + 'ms timeout'))
        self.timer.start()
        # QTimer.singleShot(self.m_time_out, self.dismiss)

    def show_load(self):
        icon = self.widget.load_icon
        if self.index < 10:
            icon.setPixmap(QPixmap(
                os.path.join(os.path.dirname(__file__), "resource/images/launch_animation_0000" + str(self.index) + ".png")))
        else:
            icon.setPixmap(QPixmap(
                os.path.join(os.path.dirname(__file__), "resource/images/launch_animation_000" + str(self.index) + ".png")))
        self.index += 1
        if self.index == 90:
            self.index = 0

    def init_ui(self):
        qssFile = os.path.join(os.path.dirname(__file__) + '/resource/qss/style.qss')
        with open(qssFile) as fp:
            qss = fp.read()
            self.setStyleSheet(qss)

        bg_path = os.path.join(os.path.dirname(__file__), "resource/images/img_bg.png")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(bg_path)))
        self.setPalette(palette)
        self.widget.load_icon.setPixmap(QPixmap(
                os.path.join(os.path.dirname(__file__), "resource/images/launch_animation_00001.png")))
        # self.widget.text.setMinimumHeight(68)
        # l, t, r, b = self.widget.text.getContentsMargins()
        # self.widget.text.setContentsMargins(l, t, r, b + 2)
        self.widget.text.setText(self.common_cfg.get_value_for_key("ubt_loading"))
        self.init_tip(self.widget.tip)
        self.move(0, 0)
        import tkinter
        win = tkinter.Tk()
        self.resize(win.winfo_screenwidth(), win.winfo_screenheight())
        self.showFullScreen()

    def init_tip(self, label):
        cfg = ConfigureStringSingle.get_common_string_cfg()
        idx = random.randint(1, 30)
        print(idx)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)
        label.setText(cfg.get_value_for_key(f'ubt_loading_tip{idx}'))
        label.adjustSize()
        label.setScaledContents(True)

    def dismiss(self, reason=''):
        print('load Dismiss', reason)
        self.timer.stop()
        self.close()
        self.thread.flag = False


class LoadThread(QThread):
    trigger = pyqtSignal()

    def __init__(self):
        super(LoadThread, self).__init__()
        self.flag = True

    def run(self):
        while self.flag:
            time.sleep(0.04)
            self.trigger.emit()
