import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, QPoint, Qt

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyQt5.QtGui import QKeyEvent, QPixmap, QPainter, QPalette, QColor
from PyQt5.QtWidgets import *


class RotateLabel(QGraphicsView):

    def __init__(self, pix):
        super().__init__()
        # self.pix = pix
        # self.setFixedSize(72, 72)
        self.setFixedSize(73, 110)
        self.setAlignment(Qt.AlignCenter)
        pixmap = pix
        scaledPixmap = pixmap.scaled(72, 72)
        self._set_color(QColor.fromRgb(0, 0, 0, 0))
        # self.setPixmap(scaledPixmap)
        # self.animation()

        self.pixmap_item = QGraphicsPixmapItem(scaledPixmap)
        # self.pixmap_item.setFlag(~QGraphicsItem.ItemIsMovable)
        self.pixmap_item.setTransformOriginPoint(36, 36)  # 设置中心为旋转pixmap = QPixmap("./img_loading.png")
        self.scene = QGraphicsScene(self)
        # self.scene.setSceneRect(0, 0, 72, 72)
        self.scene.addItem(self.pixmap_item)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 18, 18)
        # self.setStyleSheet("border: 2px solid #F00")
        # scaledPixmap = pixmap.scaled(72, 72)
        self.animation()

        # self.pixmap_item = QGraphicsPixmapItem(scaledPixmap)
        # self.pixmap_item.setTransformOriginPoint(36, 36)  # 设置中心为旋转
        # self.anim2.start()

    def _set_color(self, col):
        self.palette = QPalette()
        # self.palette.setColor(self.backgroundRole(), col)
        self.palette.setBrush(self.backgroundRole(), col)
        self.setPalette(self.palette)

    def animation(self):
        # self.anim = QPropertyAnimation(self, b'pos')
        # self.anim.setDuration(1000)
        # self.anim.setStartValue(QPointF(5, 30))
        # self.anim.setKeyValueAt(0.3, QPointF(144, 30))
        # self.anim.setKeyValueAt(0.5, QPointF(54, 90))
        # self.anim.setKeyValueAt(0.8, QPointF(240, 250))
        # self.anim.setEndValue(QPointF(300, 60))

        self.animation = QPropertyAnimation(self, b'rotation')
        self.animation.setDuration(1000)
        self.animation.setLoopCount(1000)
        self.animation.setStartValue(QPointF(0, 1))
        self.animation.setEndValue(QPointF(360, 1))
        self.animation.start()

        # self.anim2 = QPropertyAnimation(self, b'rotation')
        # self.anim2.setDuration(1000)
        # self.anim2.setLoopCount(1000)
        # self.anim2.setStartValue(QPointF(0, 1))
        # self.anim2.setEndValue(QPointF(360, 1))
        # self.anim2.start()
        # self.anim2.setEasingCurve(QEasingCurve.Linear)

    def _set_rotation(self, angle):
        print(angle)
        self.pixmap_item.setRotation(angle.x())  # 旋转度数

    rotation = pyqtProperty(QPointF, fset=_set_rotation)
