
from PyQt5.QtWidgets import QWidget,QStyle,QStyleOption, QLabel

from PyQt5.QtGui import QPixmap,QPainter

from face_recognize_demo.com import ubt_device


class Camera_Widget(QWidget):
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)

        painter.drawPixmap(0, 0, 640 * ubt_device.scale_width, 480 * ubt_device.scale_height, self.bg_pixmap)
        # painter.drawPixmap(0, 0, 640, 480, self.bg_pixmap)
        painter.end()

    def __init__(self, parent):
        super(Camera_Widget, self).__init__(parent)

        self.bg_pixmap = QPixmap(":/resource/backgroud.png")

        mask = QLabel(self)
        mask.setGeometry(0, 0, 640 * ubt_device.scale_width, 480 * ubt_device.scale_height)
        mask.setScaledContents(True)
        pixmap = QPixmap(":/resource/video_mask.png")
        mask.setPixmap(pixmap)