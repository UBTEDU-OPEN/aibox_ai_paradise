# -*-coding:utf-8 -*-
# from capture_dialog_ui import Ui_Dialog
import sys
import os

from PyQt5.QtCore import Qt

from face_recognize_demo.view.capture_dialog_ui import Ui_Dialog

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal as Signal
import logging


class CaptureDialogView(QtWidgets.QDialog, Ui_Dialog):

    captured = Signal()
    cancelled = Signal()

    def __init__(self, parent=None, tip=None, cancel_title=None, ok_title=None):
        super(CaptureDialogView, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        self.pb_cancel.clicked.connect(self.cancelled)
        self.pb_capture.clicked.connect(self.captured)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(tip)
        self.pb_cancel.setText(cancel_title)
        self.pb_capture.setText(ok_title)

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

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape:
            self.cancelled.emit()
            a0.accept()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CaptureDialogView()
    dialog.show()

    sys.exit(app.exec_())





