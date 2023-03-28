# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QListWidget, QWidget,QListView, QListWidgetItem, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap, QFontMetrics

import time

from face_recognize_demo.com import ubt_device


class RecordCustomItem(QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.content_image_label = QLabel(self)
        self.content_image_label.setGeometry(0, 0, 110 * ubt_device.scale_width, 110 * ubt_device.scale_height)
        self.content_image_label.setScaledContents(True)

        self.top_bg = QLabel(self)
        self.top_bg.setGeometry(0, 0, 110 * ubt_device.scale_width, 8 * ubt_device.scale_height)
        self.top_bg.setObjectName("top_bg_label")
        pixmap = QPixmap(":/resource/record_top_bg.png")
        self.top_bg.setPixmap(pixmap)
        # self.top_bg.setStyleSheet("QLabel#top_bg_label{background-image:url(:/resource/record_top_bg.png)}")
        self.top_bg.setScaledContents(True)

        self.bottom_label = QLabel(self)
        self.bottom_label.setGeometry(0, 110 * ubt_device.scale_height, 110 * ubt_device.scale_width, 153 * ubt_device.scale_width)
        self.bottom_label.hide()
        self.bottom_label.setObjectName("bottom_label")
        self.bottom_label.setStyleSheet("QWidget#bottom_label{background-color:rgba(145,137,254,0.4);border-bottom-left-radius: 10px;border-bottom-right-radius: 10px;}")

        self.reconrd_image_label = QLabel(self.bottom_label)
        self.reconrd_image_label.setGeometry(0, 0, 110 * ubt_device.scale_width, 110 * ubt_device.scale_width)
        self.reconrd_image_label.setScaledContents(True)

        self.confi_label = QLabel(self.bottom_label)
        self.confi_label.setGeometry(0, 0, 46 * ubt_device.scale_width, 26 * ubt_device.scale_width)
        confi_font = QFont("Source Han Sans CN")
        confi_font.setWeight(QFont.Bold)
        confi_font.setPixelSize(16)
        self.confi_label.setFont(confi_font)
        self.confi_label.setText("90%")
        # self.confi_label.hide()
        self.confi_label.setAlignment(Qt.AlignCenter)
        self.confi_label.setObjectName("confi_label")
        self.confi_label.setStyleSheet("QLabel#confi_label{background-color:rgba(161,212,142,0.5);border-bottom-right-radius: 10px;color:#ffffff;}")

        self.name_label = QLabel(self.bottom_label)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setGeometry(0, (1 + 110) * ubt_device.scale_width, 110 * ubt_device.scale_width, 20 * ubt_device.scale_width)
        name_font = QFont("Source Han Sans CN")
        name_font.setWeight(QFont.Bold)
        name_font.setPixelSize(16)
        self.name_label.setFont(name_font)
        self.name_label.setObjectName("record_name_label")
        self.name_label.setStyleSheet("QLabel#record_name_label{color:#ffffff;}")

        self.time_label = QLabel(self.bottom_label)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setGeometry(0, (22 + 110) * ubt_device.scale_width, 110 * ubt_device.scale_width, 20 * ubt_device.scale_width)
        time_font = QFont("Source Han Sans CN")
        # time_font.setWeight(QFont.Regular)
        time_font.setPixelSize(16)
        self.time_label.setFont(time_font)
        self.time_label.setObjectName("record_time_label")
        self.time_label.setStyleSheet("QLabel#record_time_label{color:#ffffff;}")

    def set_content_image(self, image):
        self.content_image_label.setPixmap(QtGui.QPixmap(image))

    def set_record_image(self, image):
        self.reconrd_image_label.setPixmap(QtGui.QPixmap(image))

    def set_name(self, name):
        if name == None:
            self.bottom_label.hide()
            return

        self.bottom_label.show()
        # 名字过长时, 右边做省略处理
        font_metrics = QFontMetrics(self.name_label.font())
        elided_name = font_metrics.elidedText(name, Qt.ElideRight, self.name_label.width())
        self.name_label.setText(elided_name)

    def set_confirence(self, value):
        if value == None:
            self.bottom_label.hide()
            return

        self.bottom_label.show()
        self.confi_label.setText(value)

    def set_time(self, time_text):
        self.time_label.setText(time_text)


class RecordListWidget(QWidget):
    def __del__(self):
        print("已经释放RecordListWidget")

    def __init__(self, parent):
        super(RecordListWidget, self).__init__(parent)

        self.list_widget = QListWidget(self)
        self.list_widget.resize(640 * ubt_device.scale_width, 273 * ubt_device.scale_height)

        self.list_widget.setFlow(QListView.LeftToRight)
        self.list_widget.setViewMode(QListView.ListMode)

        self.list_widget.setSpacing(5)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setStyleSheet("QWidget{background-color:transparent}")

        for default in range(5):
            self.add_default_item()

    def add_default_item(self):
        """

        :return:
        """
        custom_widget = self.create_item()

        custom_widget.set_content_image(":/resource/face_default.png")

    def add_record_item(self, smaple_img, record_img, name, record_time, confirence):
        """

        :param smaple_img: (QPixmape) 样本
        :param record_img: (QPixmape) 打卡截图
        :param name: (str) 名字
        :param record_time: (str) 打卡时间
        :param confirence: (str) 置信度
        :return:
        """
        custom_widget = self.create_item()

        custom_widget.set_content_image(smaple_img)
        custom_widget.set_record_image(record_img)
        custom_widget.set_name(name)
        custom_widget.set_confirence(confirence)
        custom_widget.set_time(record_time)

    def create_item(self):
        """

        :return:
        """
        custom_widget = RecordCustomItem()

        item = QListWidgetItem(self.list_widget)
        item.setFlags(Qt.NoItemFlags);
        item.setFlags(Qt.ItemIsEnabled);
        item.setSizeHint(QSize(110 * ubt_device.scale_width, 263 * ubt_device.scale_width))
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, custom_widget)

        return custom_widget

