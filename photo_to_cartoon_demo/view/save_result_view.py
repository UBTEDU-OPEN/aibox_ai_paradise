import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from common.utility.configure_string_single import ConfigureStringSingle

class SaveResultWidget(QWidget):
    def __init__(self, parent=None, configure=None):
        super(SaveResultWidget, self).__init__(parent)

        self.configure = configure

        self.init_ui()

    def set_cartoon_result(self, original_photo=None, cartoon_photo=None):
        if original_photo is not None:
            self.original_photo.setPixmap(original_photo)

        if cartoon_photo is not None:
            self.cartoon_photo.setPixmap(cartoon_photo)

    def init_ui(self):
        self.title_lab = QLabel(self)
        self.title_lab.setGeometry(270, 217, 640, 50)
        self.title_lab.setScaledContents(True)
        self.title_lab.setText(self.configure.get_value_for_key("k_title"))
        # self.title_lab.setText("<font color=%s>%s</font>" % ('#ffffff', "人物卡通化"))

        self.title_lab_desc = QLabel(self)
        self.title_lab_desc.setGeometry(270, 283, 640, 60)
        self.title_lab_desc.setScaledContents(True)
        self.title_lab_desc.setText(self.configure.get_value_for_key("k_title_desc"))

        title_font = QFont("Source Han Sans CN")
        title_font.setWeight(QFont.Bold)
        title_font.setPixelSize(36)
        self.title_lab.setFont(title_font)
        self.title_lab.setStyleSheet("QLabel{color:#ffffff;}")

        title_desc_font = QFont("Source Han Sans CN")
        title_desc_font.setWeight(QFont.Normal)
        title_desc_font.setPixelSize(18)

        self.title_lab_desc.setFont(title_desc_font)

        self.title_lab_desc.setStyleSheet("QLabel{color:#787A93;}")

        self.original_photo = QLabel(self)
        self.original_photo.setGeometry(270, 382, 640, 480)
        self.original_photo.setScaledContents(True)
        pixmap = QPixmap(":/resources/camera_mask.png")
        self.original_photo.setPixmap(pixmap)

        self.original_photo_mask = QLabel(self)
        self.original_photo_mask.setGeometry(270, 382, 640, 480)
        self.original_photo_mask.setScaledContents(True)
        pixmap = QPixmap(":/resources/camera_mask.png")
        self.original_photo_mask.setPixmap(pixmap)

        self.line = QLabel(self)
        self.line.setGeometry(959, 382, 1, 480)
        self.line.setScaledContents(True)
        self.line.setStyleSheet("QLabel{background-color:rgba(120, 132, 147,0.4);}")

        self.cartoon_photo = QLabel(self)
        self.cartoon_photo.setGeometry(1011, 382, 640, 480)
        self.cartoon_photo.setAlignment(Qt.AlignCenter)
        self.cartoon_photo.setStyleSheet("QLabel{background-color:#ffffff;border-radius:8px;}")

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.drawPixmap(0, 0, 1920, 1080, QPixmap(":/resources/backgroud.png"))
        painter.end()

def qapp():
    if QApplication.instance():
        _app = QApplication.instance()
    else:
        _app = QApplication(sys.argv)
    return _app

if __name__ == '__main__':
    app = qapp()
    window = SaveResultWidget()
    window.showFullScreen()
    sys.exit(app.exec_())