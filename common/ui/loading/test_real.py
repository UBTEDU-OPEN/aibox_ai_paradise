import sys
import threading
import time
from multiprocessing.pool import ThreadPool

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

from common.ui.loading.load import Load
from PyQt5 import QtCore


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        root = QHBoxLayout()
        self.btn = QPushButton('click')
        self.btn.setFixedSize(50, 50)

        root.addWidget(self.btn)

        self.setLayout(root)

        self.show_load()
        self.load_model()

    def load_model(self):
        self.thread = MThread()
        self.thread.trigger.connect(self.show_main)
        self.thread.start()

    def show_load(self):
        self.load = Load()

    def dismiss_load(self):
        self.load.dismiss('主动')

    def show_main(self):
        self.dismiss_load()
        # self.show()

class MThread(QThread):
    trigger = QtCore.pyqtSignal()

    def __init__(self):
        super(MThread, self).__init__()

    def run(self):
        time.sleep(1)  # 加载数据
        self.trigger.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.resize(1920, 1080)
    app.processEvents()
    window.show()
    sys.exit(app.exec_())
