# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Load(object):
    def setupUi(self, Load):
        Load.setObjectName("Load")
        Load.resize(884, 520)
        Load.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Load)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.root = QtWidgets.QWidget(Load)
        self.root.setObjectName("root")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.root)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.load_icon = QtWidgets.QLabel(self.root)
        self.load_icon.setMinimumSize(QtCore.QSize(190, 190))
        self.load_icon.setObjectName("load_icon")
        self.verticalLayout_2.addWidget(self.load_icon, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.text = QtWidgets.QLabel(self.root)
        self.text.setObjectName("text")
        self.verticalLayout_2.addWidget(self.text, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tip = QtWidgets.QLabel(self.root)
        self.tip.setMinimumSize(QtCore.QSize(400, 160))
        self.tip.setMaximumSize(QtCore.QSize(400, 16777215))
        self.tip.setWordWrap(True)
        self.tip.setObjectName("tip")
        self.verticalLayout_2.addWidget(self.tip, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.root, 0, QtCore.Qt.AlignVCenter)

        self.retranslateUi(Load)
        QtCore.QMetaObject.connectSlotsByName(Load)

    def retranslateUi(self, Load):
        _translate = QtCore.QCoreApplication.translate
        Load.setWindowTitle(_translate("Load", "Load"))
        self.load_icon.setText(_translate("Load", "loading"))
        self.text.setText(_translate("Load", "TextLabel"))
        self.tip.setText(_translate("Load", "TextLabel"))

