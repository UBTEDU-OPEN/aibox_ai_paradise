#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel
from common.ui.widget.buttonlabel import ButtonLabel

from R import R
from view.SlidingStackedWidget import SlidingStackedWidget
from view.guide_detail import GuideDetail
from view.indicator_widget import IndicatorWidget


class GuideItem(QWidget):
    icons = [R.imgs_img_1, R.imgs_img_2, R.imgs_img_3, R.imgs_img_4]

    def __init__(self, common_cfg):
        super().__init__()
        self.common_cfg = common_cfg
        self.tips = [self.common_cfg.get_value_for_key('ubt_yanshee_pose_guide_tip1').replace("\\n", "\n"),
                     self.common_cfg.get_value_for_key('ubt_yanshee_pose_guide_tip2').replace("\\n", "\n"),
                     self.common_cfg.get_value_for_key('ubt_yanshee_pose_guide_tip3').replace("\\n", "\n"),
                     self.common_cfg.get_value_for_key('ubt_yanshee_pose_guide_tip4').replace("\\n", "\n")]
        self.stackedWidget = SlidingStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setGeometry(0, 0, 680, 390)
        self.stackedWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        for item, tip, index in zip(self.icons, self.tips, [0, 1, 2, 3]):
            label = QLabel()
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setScaledContents(True)
            icon = QPixmap(item)
            icon = icon.scaled(680, 390)
            label.setPixmap(icon)
            self.stackedWidget.addWidget(label)
            # self.stackedWidget.addWidget(GuideDetail(icon, tip, index))


        # self.stackedWidget.autoStart()

        # draw left arrow
        self.widget_left = ButtonLabel(self)
        self.widget_left.setObjectName('left_arrow')
        self.widget_left.setGeometry(20, 235, 40, 40)
        self.widget_left.setPixmap(QPixmap(R.imgs_ic_previous))
        self.widget_left.clicked.connect(self.move_left)

        # draw right arrow
        self.widget_right = ButtonLabel(self)
        self.widget_right.setObjectName('right_arrow')
        self.widget_right.setGeometry(620, 235, 40, 40)
        self.widget_right.setPixmap(QPixmap(R.imgs_ic_next))
        self.widget_right.clicked.connect(self.move_right)
        self.handle_arrow_visible()

        # draw indicator
        self.item_indicator = IndicatorWidget(self)
        self.item_indicator.setHighlight(self.stackedWidget.current_index())
        self.item_indicator.setGeometry(340, 395, 48, 6)

        # draw tip
        self.item_name = QLabel(self)
        self.item_name.setObjectName('guide_tip')
        self.item_name.setText(self.tips[self.stackedWidget.current_index()])
        self.item_name.setGeometry(47, 410, 580, 78)
        # self.item_name.setAlignment(QtCore.Qt.AlignTop)

    def handle_arrow_visible(self):
        count = self.stackedWidget.count()
        index = self.stackedWidget.current_index()
        if index == 0:
            self.widget_left.hide()
        elif index == count - 1:
            self.widget_right.hide()
        else:
            self.widget_left.show()
            self.widget_right.show()

    def move_left(self):
        self.stackedWidget.slideInPrev()
        self.handle_arrow_visible()
        self.item_indicator.setHighlight(self.stackedWidget.current_index())
        self.item_name.setText(self.tips[self.stackedWidget.current_index()])

    def move_right(self):
        self.stackedWidget.slideInNext()
        self.handle_arrow_visible()
        self.item_indicator.setHighlight(self.stackedWidget.current_index())
        self.item_name.setText(self.tips[self.stackedWidget.current_index()])
