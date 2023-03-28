# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Bubble(object):
    def setupUi(self, Bubble):
        Bubble.setObjectName("Bubble")
        Bubble.resize(1920, 1080)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Bubble.sizePolicy().hasHeightForWidth())
        Bubble.setSizePolicy(sizePolicy)
        Bubble.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Bubble)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pop = QtWidgets.QWidget(Bubble)
        self.pop.setMaximumSize(QtCore.QSize(640, 109))
        self.pop.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.pop.setObjectName("pop")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pop)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.content = QtWidgets.QLabel(self.pop)
        self.content.setMinimumSize(QtCore.QSize(640, 96))
        self.content.setMaximumSize(QtCore.QSize(640, 96))
        self.content.setStyleSheet("background-color:#FFFFFF;\n"
"border-radius: 10px;")
        self.content.setLineWidth(2)
        self.content.setText("")
        self.content.setObjectName("content")
        self.verticalLayout_2.addWidget(self.content)
        self.arrow = QtWidgets.QLabel(self.pop)
        self.arrow.setEnabled(True)
        self.arrow.setMinimumSize(QtCore.QSize(46, 13))
        self.arrow.setMaximumSize(QtCore.QSize(46, 13))
        self.arrow.setText("")
        self.arrow.setObjectName("arrow")
        self.verticalLayout_2.addWidget(self.arrow, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.pop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Bubble)
        QtCore.QMetaObject.connectSlotsByName(Bubble)

    def retranslateUi(self, Bubble):
        pass

