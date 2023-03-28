import sys
import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')

from PyQt5 import QtWidgets, QtGui, QtCore


class CartoonFailDialog(QWidget):
    def __init__(self, title=None,
                 other_title="重拍",
                 cancel_btn_action=None,
                 other_btn_action=None,
                 parent=None):
        super(CartoonFailDialog, self).__init__(parent)

        self.setGeometry(0, 0, parent.width(), parent.height())

        self.init_ui()

        self.cancel_btn_action = cancel_btn_action
        self.other_btn_action = other_btn_action

        self.title_label.setText(title)
        self.other_btn.setText(other_title)

        self.cancel_btn.clicked.connect(self.cancel_action)
        self.other_btn.clicked.connect(self.sure_action)

        self.hide()

    def cancel_action(self):
        self.close()
        if self.cancel_btn_action is not None:
            self.cancel_btn_action()

    def sure_action(self):
        self.close()
        if self.other_btn_action is not None:
            self.other_btn_action()

    def init_ui(self):
        bg_widget = QWidget(self)
        bg_widget.setGeometry(0, 0, 1920, 1080)
        bg_widget.setObjectName("bg_widget")
        bg_widget.setStyleSheet("QWidget#bg_widget{background-color:rgba(20, 26, 48,0.8);}")

        alert_widget = QWidget(self)
        alert_widget.setGeometry((1920 - 680) / 2, (1080 - 240) / 2, 680, 240)
        # alert_widget.setGeometry(0, 0, 680, 240)
        alert_widget.setObjectName("alert_widget")
        alert_widget.setStyleSheet("QWidget#alert_widget{background-color:#ffffff;border-radius: 8px}")

        self.title_label = QLabel(alert_widget)
        self.title_label.setGeometry((alert_widget.width() - 680) / 2, 45, 680, 40)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")

        title_label_font = QFont("Source Han Sans CN")
        title_label_font.setWeight(QFont.Normal)
        title_label_font.setPixelSize(28)
        self.title_label.setFont(title_label_font)
        self.title_label.setStyleSheet("QLabel{color:#141A30;}")

        self.other_btn = QPushButton(alert_widget)
        self.other_btn.setGeometry((alert_widget.width() - 200) / 2, 130, 200, 80)
        self.other_btn.setText("重拍")
        self.other_btn.setObjectName("other_btn")
        self.other_btn.setStyleSheet("QPushButton#other_btn{background-color:#9189FE;border-radius:8px;color:#ffffff;}")

        other_btn_font = QFont("Source Han Sans CN")
        other_btn_font.setPixelSize(28)
        self.other_btn.setFont(other_btn_font)

        self.cancel_btn = QPushButton(alert_widget)
        self.cancel_btn.setGeometry(615, 7, 57, 57)
        self.cancel_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_close_blue.png)}")


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

