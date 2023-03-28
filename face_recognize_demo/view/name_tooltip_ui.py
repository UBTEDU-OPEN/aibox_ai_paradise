# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'name_tooltip.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NameTooltip(object):
    def setupUi(self, NameTooltip):
        NameTooltip.setObjectName("NameTooltip")
        NameTooltip.resize(174, 62)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NameTooltip.sizePolicy().hasHeightForWidth())
        NameTooltip.setSizePolicy(sizePolicy)
        NameTooltip.setWindowTitle("")
        NameTooltip.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.verticalLayout = QtWidgets.QVBoxLayout(NameTooltip)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content = QtWidgets.QLabel(NameTooltip)
        self.content.setMinimumSize(QtCore.QSize(0, 0))
        self.content.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.content.setStyleSheet("background-color:#FFFFFF;\n"
"border-radius: 8px;\n"
"font-family: Source Han Sans CN;\n"
"font-weight: normal;\n"
"font-size: 14px;\n"
"color: #787A93;\n"
"padding: 8px 4px 8px 4px;\n"
"text-align: center;")
        self.content.setLineWidth(0)
        self.content.setText("")
        self.content.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.content.setObjectName("content")
        self.verticalLayout.addWidget(self.content)
        self.frame = QtWidgets.QFrame(NameTooltip)
        self.frame.setStyleSheet("background-color:transparent;")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.arrow = QtWidgets.QLabel(self.frame)
        self.arrow.setEnabled(True)
        self.arrow.setMinimumSize(QtCore.QSize(20, 15))
        self.arrow.setMaximumSize(QtCore.QSize(20, 16777215))
        self.arrow.setStyleSheet("background-color:transparent;")
        self.arrow.setLineWidth(0)
        self.arrow.setText("")
        self.arrow.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.arrow.setObjectName("arrow")
        self.horizontalLayout.addWidget(self.arrow, 0, QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(NameTooltip)
        QtCore.QMetaObject.connectSlotsByName(NameTooltip)

    def retranslateUi(self, NameTooltip):
        pass

import resources_rc
