# -*-coding:utf-8 -*-
from name_input_dialog_ui import Ui_Dialog
from name_input_dialog_presenter import NameInputDialogPresenter
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal as Signal

import logging


class NameInputDialogView(QtWidgets.QDialog, Ui_Dialog):

    input_confirmed = Signal(str)
    ok_clicked = Signal()
    cancel_clicked = Signal()
    text_changed = Signal(str)

    def __init__(self, parent=None, placeholder_text=None, cancel_title=None, ok_title=None):
        super(NameInputDialogView, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        self.presenter = NameInputDialogPresenter(self)
        self.pb_ok.clicked.connect(self.ok_clicked)
        self.pb_cancel.clicked.connect(self.cancel_clicked)
        self.le_name_input.textChanged.connect(self.text_changed)

        self.le_name_input.setPlaceholderText(placeholder_text)
        self.pb_cancel.setText(cancel_title)
        self.pb_ok.setText(ok_title)

        # 禁用录入按钮
        self.enable_ok_button(False)

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

    def notify_input(self, name):
        """ 发布输入结果, 输入不合法时, 返回空string

        :param name: 输入框内容.
        """
        self.input_confirmed.emit(name)

    def get_input_text(self):
        """ 返回输入框内容

        :return: 输入框内容
        """
        name = self.le_name_input.text()
        return name

    def enable_ok_button(self, enabled):
        """ 启用/禁用确认按钮

        :param enabled: (bool)  True 启用， False 禁用
        """
        self.pb_ok.setEnabled(enabled)

    def text_max_len(self):
        """ 获取输入框的最大限制长度

        :return: (int) 文本最大长度
        """
        return self.le_name_input.maxLength()

    def backspace(self):
        """ 回退一个字符

        """
        self.le_name_input.backspace()

    def become_first_focus(self):
        self.le_name_input.setFocus()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Escape:
            self.cancel_clicked.emit()
            a0.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = NameInputDialogView()
    dialog.show()

    sys.exit(app.exec_())





