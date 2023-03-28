#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_close_dialog.py
# Created   : 2020/6/3 5:51 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 


import sys
import os

from PyQt5.QtCore import Qt

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')

from common.ui.commonDialog.common_dialog import Ui_Dialog

from PyQt5 import QtWidgets, QtCore, QtGui


class CommonDialogView(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, title='确定要退出吗？', ok_txt='退出', cancel_txt='取消', sure_button_action=None, cancel_btn_action=None,
                 parent=None):
        super(CommonDialogView, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        self.setWindowModality(Qt.ApplicationModal)

        self.sure_button_action = sure_button_action
        self.cancel_btn_action = cancel_btn_action

        self.label.setText(title)
        self.pb_cancel.setText(cancel_txt)
        self.pb_ok.setText(ok_txt)

        self.pb_cancel.clicked.connect(self.negative_action)
        self.pb_ok.clicked.connect(self.sure_action)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommonDialogView()
    dialog.show()

    sys.exit(app.exec_())
