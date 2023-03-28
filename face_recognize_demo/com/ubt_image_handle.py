# This Python file uses the following encoding: utf-8

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont,QBitmap,QPainter,QColor,QPixmap

def drawCycleImage(image,radius):
    size = image.size()
    mask = QBitmap(size)
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.HighQualityAntialiasing);
    painter.setRenderHint(QPainter.SmoothPixmapTransform);
    painter.fillRect(mask.rect(), Qt.white);
    painter.setBrush(QColor(0, 0, 0));
    painter.drawRoundedRect(mask.rect(), radius, radius);

    new_image = QPixmap(image)
    new_image.setMask(mask)
    painter.end();
    return new_image
