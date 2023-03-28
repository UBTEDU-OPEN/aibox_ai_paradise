
from PyQt5.QtWidgets import QWidget, QStyle, QStyleOption, QLabel, QPushButton

from PyQt5.QtGui import QPixmap,QPainter

from face_recognize_demo.com import ubt_device


class VideoWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)

        painter.drawPixmap(0, 0, 640 * ubt_device.scale_width, 480 * ubt_device.scale_height, self.bg_pixmap)
        painter.end()

    def __init__(self, parent, cancel_capture=None):
        super(VideoWidget, self).__init__(parent)

        self.cancel_capture = cancel_capture


        self.bg_pixmap = QPixmap(":/resource/backgroud.png")

        mask = QLabel(self)
        mask.setGeometry(0, 0, 640 * ubt_device.scale_width, 480 * ubt_device.scale_height)
        mask.setScaledContents(True)
        pixmap = QPixmap(":/resources/camera_mask.png")
        mask.setPixmap(pixmap)

        self.capture_mask = QLabel(self)
        self.capture_mask.setGeometry(0, 0, 640 * ubt_device.scale_width, 480 * ubt_device.scale_height)
        self.capture_mask.setScaledContents(True)
        pixmap = QPixmap(":/resources/img_mask.png")
        self.capture_mask.setPixmap(pixmap)

        self.cancel_btn = QPushButton(self)
        self.cancel_btn.setGeometry(578, 18, 44, 44)
        self.cancel_btn.setObjectName("add_sample_button")
        self.cancel_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_trash_p.png)}")
        self.cancel_btn.clicked.connect(self.cancel_capture)
        self.cancel_btn.setHidden(True)

    def capture_mode(self, enter):
        if enter:
            self.cancel_btn.setHidden(False)
            self.capture_mask.setHidden(True)
        else:
            self.cancel_btn.setHidden(True)
            self.capture_mask.setHidden(False)

            self.enable_cancel_btn(True)

    def enable_cancel_btn(self, enable):
        if enable:
            self.cancel_btn.setEnabled(True)
            self.cancel_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_trash_p.png)}")
        else:
            self.cancel_btn.setEnabled(False)
            self.cancel_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_trash.png)}")
