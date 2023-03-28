import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from common.ui.loading.loading_rotate import RotateIcon
from style_transfer_demo.R import R

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')

from PyQt5 import QtWidgets, QtGui, QtCore


class LoadingActiving(QWidget):
    def __init__(self, title=None, parent=None):
        super(LoadingActiving, self).__init__(parent)

        self.setGeometry(0, 0, parent.width(), parent.height())

        self.init_ui()

        self.title_label.setText(title)

        self.hide()

    def init_ui(self):
        bg_widget = QWidget(self)
        bg_widget.setGeometry(0, 0, self.width(), self.height())
        bg_widget.setObjectName("bg_widget")
        bg_widget.setStyleSheet("QWidget#bg_widget{background-color:rgba(79, 90, 126, 1); border-radius: 8px}")

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        rotate = RotateIcon(R.imgs_img_loading, 46, 46)
        layout.addWidget(rotate, 1, Qt.AlignCenter)
        # layout.addChildWidget(rotate)



        rotate.setParent(self)

        self.title_label = QLabel(self)
        # self.title_label.setFixedWidth(680)
        # self.title_label.setFixedHeight(40)
        self.title_label.setGeometry((self.width() - 680) / 2, 266, 680, 40)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")

        title_label_font = QFont("Source Han Sans CN")
        title_label_font.setWeight(QFont.Normal)
        title_label_font.setPixelSize(14)
        self.title_label.setFont(title_label_font)
        self.title_label.setStyleSheet("QLabel{color:#ffffff;}")

        # layout.addWidget(self.title_label, 5, Qt.AlignCenter)

        self.setLayout(layout)




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

