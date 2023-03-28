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

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from common.ui.commonDialog.base_dialog import Ui_alert_win
from common.utility.configure_string_single import ConfigureStringSingle

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')

from PyQt5 import QtWidgets, QtGui


class BaseDialogView(QWidget, Ui_alert_win):
    common_cfg = ConfigureStringSingle.get_common_string_cfg()

    def __init__(self, title=common_cfg.get_value_for_key('ubt_quit_title'),
                 ok_txt=common_cfg.get_value_for_key('ubt_quit'), cancel_txt=common_cfg.get_value_for_key('ubt_cancel'), sure_button_action=None,
                 cancel_btn_action=None,
                 parent=None):
        super(BaseDialogView, self).__init__(parent)
        self.setupUi(self)
        self.title.setWordWrap(True)

        self.sure_button_action = sure_button_action
        self.cancel_btn_action = cancel_btn_action

        l, t, r, b = self.title.getContentsMargins()
        self.title.setContentsMargins(l, t, r, b + 2)
        self.title.setText(title)
        self.pb_cancel.setText(cancel_txt)
        self.pb_ok.setText(ok_txt)

        self.pb_cancel.clicked.connect(self.negative_action)
        self.pb_ok.clicked.connect(self.sure_action)

        self.hide()

        import tkinter
        win = tkinter.Tk()
        self.resize(win.winfo_screenwidth(), win.winfo_screenheight())

    def negative_action(self):
        self.close()
        if self.cancel_btn_action is not None:
            self.cancel_btn_action()

    def sure_action(self):
        self.close()
        if self.sure_button_action is not None:
            self.sure_button_action()

    def paintEvent(self, event):
        """

        :param event:
        :return:
        """
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        p = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, p)
        p.end()
