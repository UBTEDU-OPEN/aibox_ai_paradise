#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel
from view.indicator_widget import IndicatorWidget


class GuideDetail(QWidget):
    def __init__(self, icon, tip, index):
        super().__init__()
        self.item_icon = QLabel(self)
        self.item_icon.setGeometry(0, 0, 680, 390)
        self.item_icon.setPixmap(icon)

        self.item_indicator = IndicatorWidget(self)
        self.item_indicator.setHighlight(index)
        self.item_indicator.setGeometry(340, 395, 48, 6)

        self.item_name = QLabel(self)
        self.item_name.setObjectName('guide_tip')
        self.item_name.setText(tip)
        self.item_name.setGeometry(47, 418, 533, 72)
