# -*-coding:utf-8 -*-
from failure_dialog_ui import Ui_Dialog
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5 import QtWidgets, QtCore, QtGui
import logging


class FailureDialogView(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None, title=None, btn_title=None):
        super(FailureDialogView, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.pb_ok.clicked.connect(lambda x: self.close())

        self.label.setText(title)
        self.pb_ok.setText(btn_title)

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
    dialog = FailureDialogView()
    dialog.show()

    sys.exit(app.exec_())





