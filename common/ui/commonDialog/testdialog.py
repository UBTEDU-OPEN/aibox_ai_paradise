import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy

from common.ui.commonDialog.BaseDialog import BaseDialogView
from common.ui.commonDialog.AlertDialog import AlertDialogView


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.root = QHBoxLayout()

        btn1 = QPushButton('btn1', clicked=self.click1)
        btn2 = QPushButton('btn2', clicked=self.click2)


        self.root.addSpacerItem(QSpacerItem(200, 0))
        self.root.addWidget(btn1)
        self.root.addSpacerItem(QSpacerItem(200, 0))

        # self.root.addWidget(slider)
        self.root.addWidget(btn2)
        self.root.addSpacerItem(QSpacerItem(200, 0))

        self.setLayout(self.root)
        self.dialog = BaseDialogView(parent=self)

    def click1(self):
        self.dialog.show()
        print("click1")

    def click2(self):
        print("click2")


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.resize(1920, 1080)
    window.show()
    sys.exit(app.exec_())
