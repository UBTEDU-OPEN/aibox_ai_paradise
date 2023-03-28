#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : FacemarkCloseDialog.py
# Created   : 2020/6/3 5:51 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 

import sys
import os

from PyQt5.QtWidgets import QWidget

from common.ui.commonDialog.alert_dialog import Ui_alert_win

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')


class AlertDialogView(QWidget, Ui_alert_win):

    def __init__(self, title, button_txt, button_action=None, parent=None):
        super(AlertDialogView, self).__init__(parent)
        self.setupUi(self)

        self.button_action = button_action

        self.title.setText(title)
        self.title.setStyleSheet("font-family: Source Han Sans CN;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 20px;\n"
                                 "color: #141A30;\n"
                                 "padding-bottom: 3px;\n"
                                 "text-align: center;")
        self.pb_sure.setText(button_txt)

        self.pb_sure.clicked.connect(self.negative_action)

        self.hide()

    def negative_action(self):
        self.close()
        if self.button_action is not None:
            self.button_action()
