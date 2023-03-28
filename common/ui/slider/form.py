# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Slider(object):
    def setupUi(self, Slider):
        Slider.setObjectName("Slider")
        Slider.resize(650, 172)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Slider.sizePolicy().hasHeightForWidth())
        Slider.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Slider)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_left = QtWidgets.QPushButton(Slider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_left.sizePolicy().hasHeightForWidth())
        self.pb_left.setSizePolicy(sizePolicy)
        self.pb_left.setMaximumSize(QtCore.QSize(17, 22))
        self.pb_left.setText("")
        self.pb_left.setFlat(True)
        self.pb_left.setObjectName("pb_left")
        self.horizontalLayout.addWidget(self.pb_left)
        self.slider = QtWidgets.QSlider(Slider)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)
        self.pb_right = QtWidgets.QPushButton(Slider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_right.sizePolicy().hasHeightForWidth())
        self.pb_right.setSizePolicy(sizePolicy)
        self.pb_right.setMaximumSize(QtCore.QSize(17, 22))
        self.pb_right.setText("")
        self.pb_right.setFlat(True)
        self.pb_right.setObjectName("pb_right")
        self.horizontalLayout.addWidget(self.pb_right)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout.setStretch(0, 30)
        self.verticalLayout.setStretch(1, 30)
        self.verticalLayout.setStretch(2, 30)

        self.retranslateUi(Slider)
        QtCore.QMetaObject.connectSlotsByName(Slider)

    def retranslateUi(self, Slider):
        _translate = QtCore.QCoreApplication.translate
        Slider.setWindowTitle(_translate("Slider", "Slider"))

