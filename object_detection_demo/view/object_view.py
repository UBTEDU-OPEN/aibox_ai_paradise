#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:object_view.py
# Created:2020/5/26 下午7:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:智能盘点View
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import PyQt5.QtCore as QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QVBoxLayout, QListWidgetItem, QListView, QHBoxLayout

from view.goods_item import GoodsItem
from R import R
from view.select_item import SelectItem
from view.vertical_scrollbar import UbtVerticalScrollBar
from view.base import Ui_Base
from config.object_config_util import ConfigUtils
from common.ui.slider.slider import Slider
from common.ui.widget.buttonlabel import ButtonLabel
from common.ui.bubbleDialog.popwindow import PopWindow
from common.utility.configure_string_single import ConfigureStringSingle


class ObView(QWidget):
    updateGoodsSelectSignal = QtCore.pyqtSignal(object)
    updateThreSholdSignal = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        # parent.setAutoFillBackground(True)
        self.parent = parent
        self.goods_item_widgets = []
        self.goods_item_selected = []
        self.goods_show_widgets = []
        self.widget = Ui_Base()
        self.widget.setupUi(parent)
        self.init_ui(parent)
        self.init_goods_group()
        self.init_goods_select()
        self.init_threshold_slider()

    def init_threshold_slider(self):
        threshold = self.widget.threshold
        slider = Slider(40, ConfigureStringSingle.get_common_string_cfg().get_value_for_key('ubt_default'))
        threshold.layout().addWidget(slider)
        slider.value_changed.connect(self.threshold_change)

    def init_ui(self, widget):
        with open(R.qss_style) as fp:
            qss = fp.read()
            widget.setStyleSheet(qss)
        real_content = self.widget
        real_content.card_icon.setPixmap(QPixmap(R.imgs_img_logo))

        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(R.imgs_img_bg)))
        self.parent.setPalette(palette)

        s_conf = ConfigUtils()

        real_content.top_layout.setContentsMargins(40, 46, 0, 0)
        real_content.title.setMinimumHeight(50)
        real_content.title.setText(s_conf.get_section_value(s_conf.rcn, 'title'))
        real_content.sub_title.setText(s_conf.get_section_value(s_conf.rcn, 'sub_title'))
        real_content.sub_title.adjustSize()
        real_content.sub_title.setWordWrap(True)
        real_content.describe.setText(s_conf.get_section_value(s_conf.rcn, 'inventory_desc'))
        real_content.threshold_label.setText(s_conf.get_section_value(s_conf.rcn, 'threshold_setting'))
        real_content.select_goods_label.setText(s_conf.get_section_value(s_conf.rcn, 'select_inventory'))

        btn_close = ButtonLabel()
        btn_close.set_selector(R.imgs_ic_close, R.imgs_ic_close_press)
        btn_close.setPixmap(QPixmap(R.imgs_ic_close))
        btn_close.setObjectName(u"btn_close")
        btn_close.setMinimumSize(QSize(42, 42))
        btn_close.setAlignment(Qt.AlignCenter)

        real_content.horizontalLayout_2.addWidget(btn_close, 0, Qt.AlignTop)
        btn_close.clicked.connect(self.parent.show_exit)
        # btn_close.clicked.connect(self.parent.close)

        # add round corner for camera image label
        # camera_mask = QHBoxLayout()
        # camera_mask.setContentsMargins(0, 0, 0, 0)
        # camera_mask.setAlignment(Qt.AlignCenter)

        mask = QLabel(real_content.camera)
        pix = QPixmap(R.imgs_ic_rc_camera)
        mask.setPixmap(pix)
        real_content.camera.setFixedSize(640, 480)
        # mask.resize(640, 480)
        # real_content.camera.setPixmap(QPixmap('resource/images/ic_rc_camera.png'))
        # camera_mask.addWidget(mask)
        # real_content.camera.setLayout(camera_mask)

        # add threshold info for threshold label
        info_btn = ButtonLabel()
        info_btn.set_selector(R.imgs_ic_info, R.imgs_ic_info_press)
        info_btn.setFixedSize(24, 24)
        info_btn.setPixmap(QPixmap(R.imgs_ic_info))

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignVCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        txt = QLabel(s_conf.get_section_value(s_conf.rcn, 'threshold_setting'))
        txt.setObjectName('threshold_txt')
        txt.setMinimumHeight(40)
        txt.setAlignment(Qt.AlignCenter)
        layout.addWidget(txt, 0, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(info_btn, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        real_content.threshold_label.setLayout(layout)
        real_content.threshold_label.setText("")

        self.pop_tip = PopWindow(info_btn, parent=self.parent)

        # draw pop
        # pop_widget = QWidget(self.parent)
        # pop_widget.setLayout()

    def init_goods_group(self):
        import tkinter
        win = tkinter.Tk()
        print('screenwidth', win.winfo_screenwidth())
        right_margin = win.winfo_screenwidth() - 1702
        if right_margin < 0:
            right_margin = 28
        self.widget.frame.setContentsMargins(0, 0, right_margin, 20)
        # self.widget.frame.setFixedWidth(800)
        # self.widget.frame.setStyleSheet("QFrame{margin-right:%dpx;}" % (win.winfo_screenwidth() - 1710))
        goods_list_widget = self.widget.select_goods_list
        # goods_list_widget.setGridSize(QSize(220, 50))
        goods_list_widget.setViewMode(QListView.IconMode)
        # goods_list_widget.setResizeMode(QListView.Adjust)
        # goods_list_widget.setWordWrap(True)
        # goods_list_widget.setWrapping(True)
        goods_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        goods_list_widget.setVerticalScrollBar(UbtVerticalScrollBar(QtCore.Qt.Vertical))
        goods_list_widget.setStyleSheet(
            "QWidget{border-bottom-left-radius: 8px;border-bottom-right-radius: 8px;}")

        goods_list = ConfigUtils().getCoCoNames()

        for goods_item in goods_list:
            widget = GoodsItem(goods_item[0], goods_item[1])
            widget.displaySignal.connect(self.display_update)
            widget.updateSelectSignal.connect(self.select_update)

            item = QListWidgetItem()
            item.setSizeHint(QSize(220, 50))
            goods_list_widget.addItem(item)
            goods_list_widget.setItemWidget(item, widget)
            self.goods_item_widgets.append(widget)

    def display_update(self, disable):
        for widget in self.goods_item_widgets:
            widget.update(disable)

    def select_update(self, widget):
        if widget.checked:
            self.goods_item_selected.append(widget)
        else:
            self.goods_item_selected.remove(widget)
        self.update_goods_show()
        # self.updateGoodsSelectSignal.emit(self.goods_item_selected)
        self.update_select(self.goods_item_selected)

    def update_goods_show(self):
        select = []
        for widget, goods in zip(self.goods_show_widgets, self.goods_item_selected):
            select.append(widget)
            widget.update_widget(goods)
        for item in list(set(self.goods_show_widgets) - set(select)):
            item.show_default()

    def update_goods_count(self, keys):
        for widget, goods in zip(self.goods_show_widgets, self.goods_item_selected):
            widget.update_widget_count(keys)
        del keys

    def init_goods_select(self):
        list_widget = self.widget.selected_list
        list_widget.setFlow(QListWidget.LeftToRight)

        for goods in range(3):
            widget = SelectItem()

            item = QListWidgetItem()
            # item.setFlags(~Qt.ItemIsEnabled)
            item.setFlags(Qt.ItemIsUserCheckable)
            item.setSizeHint(QSize(140, 180))
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)
            self.goods_show_widgets.append(widget)

    def threshold_change(self, value):
        print("threshold", value)
        self.update_threshold(value / 100)
        # self.updateThreSholdSignal.emit(value / 100)

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

    def set_select_control(self, update_select, update_threshold):
        self.update_select = update_select
        self.update_threshold = update_threshold
        # self.updateGoodsSelectSignal.connect(update_select)
        # self.updateThreSholdSignal.connect(update_threshold)
