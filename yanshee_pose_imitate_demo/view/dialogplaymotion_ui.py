# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogplaymotion.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogPlayMotion(object):
    def setupUi(self, DialogPlayMotion):
        DialogPlayMotion.setObjectName("DialogPlayMotion")
        DialogPlayMotion.resize(1920, 1080)
        DialogPlayMotion.setMaximumSize(QtCore.QSize(1920, 1080))
        self.lb_camera_full = QtWidgets.QLabel(DialogPlayMotion)
        self.lb_camera_full.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.lb_camera_full.setMaximumSize(QtCore.QSize(1920, 1080))
        self.lb_camera_full.setText("")
        self.lb_camera_full.setObjectName("lb_camera_full")
        self.widget = QtWidgets.QWidget(DialogPlayMotion)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.widget.setMaximumSize(QtCore.QSize(1920, 1080))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(38, 0, 88, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 70, 0, 70)
        self.verticalLayout.setSpacing(40)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lb_action1 = QtWidgets.QLabel(self.widget)
        self.lb_action1.setMinimumSize(QtCore.QSize(170, 170))
        self.lb_action1.setMaximumSize(QtCore.QSize(170, 170))
        self.lb_action1.setText("")
        self.lb_action1.setPixmap(QtGui.QPixmap(":/images/img_action1.png"))
        self.lb_action1.setObjectName("lb_action1")
        self.verticalLayout.addWidget(self.lb_action1)
        self.lb_action2 = QtWidgets.QLabel(self.widget)
        self.lb_action2.setMinimumSize(QtCore.QSize(170, 170))
        self.lb_action2.setMaximumSize(QtCore.QSize(170, 170))
        self.lb_action2.setText("")
        self.lb_action2.setPixmap(QtGui.QPixmap(":/images/img_action2.png"))
        self.lb_action2.setObjectName("lb_action2")
        self.verticalLayout.addWidget(self.lb_action2)
        self.lb_action3 = QtWidgets.QLabel(self.widget)
        self.lb_action3.setMinimumSize(QtCore.QSize(170, 170))
        self.lb_action3.setMaximumSize(QtCore.QSize(170, 170))
        self.lb_action3.setText("")
        self.lb_action3.setPixmap(QtGui.QPixmap(":/images/img_action3.png"))
        self.lb_action3.setObjectName("lb_action3")
        self.verticalLayout.addWidget(self.lb_action3)
        self.lb_action4 = QtWidgets.QLabel(self.widget)
        self.lb_action4.setMinimumSize(QtCore.QSize(170, 170))
        self.lb_action4.setMaximumSize(QtCore.QSize(170, 170))
        self.lb_action4.setText("")
        self.lb_action4.setPixmap(QtGui.QPixmap(":/images/img_action4.png"))
        self.lb_action4.setObjectName("lb_action4")
        self.verticalLayout.addWidget(self.lb_action4)
        self.lb_action5 = QtWidgets.QLabel(self.widget)
        self.lb_action5.setMinimumSize(QtCore.QSize(170, 170))
        self.lb_action5.setMaximumSize(QtCore.QSize(170, 170))
        self.lb_action5.setText("")
        self.lb_action5.setPixmap(QtGui.QPixmap(":/images/img_action5.png"))
        self.lb_action5.setObjectName("lb_action5")
        self.verticalLayout.addWidget(self.lb_action5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(445, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(700, 930))
        self.label.setMaximumSize(QtCore.QSize(700, 930))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/img_action1_stand.png"))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(478, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 35, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pb_back = QtWidgets.QPushButton(self.widget)
        self.pb_back.setMinimumSize(QtCore.QSize(50, 50))
        self.pb_back.setMaximumSize(QtCore.QSize(50, 50))
        self.pb_back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/ic_fullscreen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_back.setIcon(icon)
        self.pb_back.setIconSize(QtCore.QSize(80, 80))
        self.pb_back.setObjectName("pb_back")
        self.verticalLayout_2.addWidget(self.pb_back)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(DialogPlayMotion)
        QtCore.QMetaObject.connectSlotsByName(DialogPlayMotion)

    def retranslateUi(self, DialogPlayMotion):
        _translate = QtCore.QCoreApplication.translate
        DialogPlayMotion.setWindowTitle(_translate("DialogPlayMotion", "Dialog"))

import resource_rc
