# -*-coding:utf-8 -*-
# This Python file uses the following encoding: utf-8
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from form import Ui_Slider
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSlider
from PyQt5.QtCore import QRect
from common.base.view import View
from slider_presenter import SliderPresenter
import logging

GROOVE_SIZE = (516, 10)
HANDLE_SIZE = (30, 30)
BUBBLE_SIZE = (70, 34.5)
BUBBLE_SPACING = 7.5
BUBBLE_TEXT_COLOR = (0x91, 0x89, 0xfe)
BUBBLE_TEXT_SIZE = 16
BUBBLE_TEXT_FAMILY = 'SourceHanSansCN-Bold'
BUBBLE_TEXT_MARGIN = 3
TICKS_POSITION_OFFSET = 5
TICKS_HEIGHT = 6
TICKS_COLOR = (0x2C, 0x3A, 0x4B)
DEFAULT_VALUE_SIZE = (72, 16)
DEFAULT_VALUE_OFFSET = 21
DEFAULT_VALUE_COMMON_COLOR = (0x14, 0x1A, 0x30)
DEFAULT_VALUE_HIGHLIGHT_COLOR = (0x91, 0x89, 0xfe)


class Slider(QWidget, View):

    # signal
    value_changed = QtCore.pyqtSignal(int)
    mouse_released = QtCore.pyqtSignal()

    def __init__(self, default_value=50, default_desc='默认值'):
        super(Slider, self).__init__()

        self.default_desc = default_desc

        self.ui = Ui_Slider()
        self.slider_moving = False
        self.init_ui()
        self.load_stylesheet()
        self.init_signals()
        self.ui.slider.setValue(default_value)
        self.default_value = default_value
        self.presenter = SliderPresenter(self)
        self.previous_value = self.default_value
        self.default_value_rect = QRect()

    def init_ui(self):
        """ 初始化UI设置

        :return:
        """
        self.ui.setupUi(self)
        decrease_icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_arrow_decrease.png")
        decrease_icon = QtGui.QIcon(decrease_icon_path)
        self.ui.pb_left.setIcon(decrease_icon)
        increase_icon_path = os.path.join(os.path.dirname(__file__), "resource/images", "ic_arrow_increase.png")
        increase_icon = QtGui.QIcon(increase_icon_path )
        self.ui.pb_right.setIcon(increase_icon)
        # 替换release event, 把鼠标事件传递给父控件
        self.ui.slider.sliderReleased.connect(self.on_slider_released)
        self.ui.slider.sliderMoved.connect(self.on_slider_moving)

    def load_stylesheet(self):
        """ 加载stylesheet设置

        :return:
        """
        qss_path = os.path.join(os.path.dirname(__file__), "resource/qss", "default.qss")
        with open(qss_path) as fp:
            qss = fp.read()
            self.setStyleSheet(qss)

    def init_signals(self):
        """ 初始化信号槽

        :return:
        """
        self.ui.slider.valueChanged.connect(self.on_value_changed)
        self.ui.pb_left.clicked.connect(self.on_decrease_button_clicked)
        self.ui.pb_right.clicked.connect(self.on_increase_button_clicked)

    def on_value_changed(self, value):
        """ 槽函数， 处理slider值变化信号

        :param value: slider当前值
        :return:
        """
        if not self.slider_moving:
            self.mouse_released.emit()
        self.update()

    def paintEvent(self, event):
        """ 绘制自定义UI

        :param event: event
        :return:
        """
        super(Slider, self).paintEvent(event)
        factor = 0.8
        if self.ui.slider.value() > self.ui.slider.maximum() / 2:
            factor = 0.4
        bubble_x = self.ui.slider.x() + HANDLE_SIZE[0] / 2 + (self.ui.slider.width() - HANDLE_SIZE[0]) * \
                   (self.ui.slider.value() - factor) / self.ui.slider.maximum() - BUBBLE_SIZE[0] / 2
        bubble_y = self.ui.slider.y() - BUBBLE_SIZE[1] - BUBBLE_SPACING
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing);
        # 绘制气泡背景图
        pix = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "resource/images", "img_bubble_number.png"))
        qp.drawPixmap(QtCore.QRect(bubble_x, bubble_y, *BUBBLE_SIZE), pix)
        # 绘制气泡文字
        qp.setPen(QtGui.QColor(*BUBBLE_TEXT_COLOR))
        font = QtGui.QFont(BUBBLE_TEXT_FAMILY)
        font.setPixelSize(BUBBLE_TEXT_SIZE)
        qp.setFont(font)
        qp.drawText(bubble_x, bubble_y - BUBBLE_TEXT_MARGIN, *BUBBLE_SIZE, QtCore.Qt.AlignCenter, "≥" + str(self.ui.slider.value()) + "%")

        # 画刻度
        slider_width = self.ui.slider.width() - HANDLE_SIZE[0]
        step = slider_width / 10
        start_point = self.ui.slider.x() + HANDLE_SIZE[0] / 2
        ticks_y = self.ui.slider.y() + self.ui.slider.height() + TICKS_POSITION_OFFSET + TICKS_HEIGHT / 2
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(*TICKS_COLOR))
        for i in range(0, 11):
            ticks_x = start_point + i * step
            qp.drawEllipse(ticks_x, ticks_y, TICKS_HEIGHT/2, TICKS_HEIGHT/2)

        # 标注默认值
        default_x = self.ui.slider.x() + HANDLE_SIZE[0] / 2 + (self.ui.slider.width() - HANDLE_SIZE[0]) * \
                   self.default_value / self.ui.slider.maximum() - DEFAULT_VALUE_SIZE[0] / 2
        default_y = self.ui.slider.y() + self.ui.slider.height() + DEFAULT_VALUE_OFFSET
        if self.value == self.default_value:
            # 高亮显示
            qp.setPen(QtGui.QColor(*DEFAULT_VALUE_HIGHLIGHT_COLOR))
        else:
            qp.setPen(QtGui.QColor(*DEFAULT_VALUE_COMMON_COLOR))

        qp.drawText(default_x, default_y, *DEFAULT_VALUE_SIZE, QtCore.Qt.AlignCenter, self.default_desc)
        self.default_value_rect = QRect(default_x, default_y, *DEFAULT_VALUE_SIZE)

        qp.end()

    def mouseReleaseEvent(self, event):
        """ 发送信号， 由presenter处理

        :param event:
        :return:
        """
        if event.pos() in self.default_value_rect:
            self.ui.slider.setValue(self.default_value)
        self.mouse_released.emit()
        event.accept()

    def set_default_value(self, value):
        """ 设置默认值

        :param value:  新的默认值
        :return:
        """
        self.default_value = value

    def on_decrease_button_clicked(self):
        """ 处理微调减按键

        :return:
        """
        cur_value = self.value
        self.ui.slider.setValue(cur_value - 1 if cur_value > self.ui.slider.minimum() else cur_value)
        self.mouse_released.emit()

    def on_increase_button_clicked(self):
        """ 处理微调加按键

        :return:
        """
        cur_value = self.value
        self.ui.slider.setValue(cur_value + 1 if cur_value < self.ui.slider.maximum() else cur_value)
        self.mouse_released.emit()


    @property
    def value(self):
        """ 获取滑块当前值

        :return: int - 滑块当前值
        """
        return self.ui.slider.value()

    def on_slider_moving(self):
        """ 滑块移动时， 设置标记

        """
        self.slider_moving = True

    def on_slider_released(self):
        """ slider鼠标释放时， 重置滑动标记

        """
        self.slider_moving = False
        self.mouse_released.emit()

