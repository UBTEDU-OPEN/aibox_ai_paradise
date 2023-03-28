# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alert_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_alert_win(object):
    def setupUi(self, alert_win):
        alert_win.setObjectName("alert_win")
        alert_win.resize(1920, 1080)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(alert_win.sizePolicy().hasHeightForWidth())
        alert_win.setSizePolicy(sizePolicy)
        alert_win.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(alert_win)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.alert_root = QtWidgets.QWidget(alert_win)
        self.alert_root.setStyleSheet("background: #CC141A30;")
        self.alert_root.setObjectName("alert_root")
        self.root_layout = QtWidgets.QHBoxLayout(self.alert_root)
        self.root_layout.setObjectName("root_layout")
        self.alert_parent = QtWidgets.QWidget(self.alert_root)
        self.alert_parent.setMinimumSize(QtCore.QSize(468, 180))
        self.alert_parent.setMaximumSize(QtCore.QSize(468, 214))
        self.alert_parent.setStyleSheet("background: #FFFFFF;\n"
"border-radius: 8px;")
        self.alert_parent.setObjectName("alert_parent")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.alert_parent)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalWidget = QtWidgets.QWidget(self.alert_parent)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.title = QtWidgets.QLabel(self.horizontalWidget)
        self.title.setStyleSheet("font-family: Source Han Sans CN;\n"
"font-weight: bold;\n"
"font-size: 24px;\n"
"color: #141A30;\n"
"text-align: center;")
        self.title.setText("")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.horizontalLayout_2.addWidget(self.title, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.horizontalWidget)
        self.horizontalWidget1 = QtWidgets.QWidget(self.alert_parent)
        self.horizontalWidget1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalWidget1.setObjectName("horizontalWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget1)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_sure = QtWidgets.QPushButton(self.horizontalWidget1)
        self.pb_sure.setMinimumSize(QtCore.QSize(120, 50))
        self.pb_sure.setMaximumSize(QtCore.QSize(120, 50))
        self.pb_sure.setStyleSheet("background: #9189FE;\n"
"border-radius: 8px;\n"
"font-family: Source Han Sans CN;\n"
"font-weight: bold;\n"
"font-size: 20px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")
        self.pb_sure.setText("")
        self.pb_sure.setObjectName("pb_sure")
        self.horizontalLayout.addWidget(self.pb_sure, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.verticalLayout_2.addWidget(self.horizontalWidget1, 0, QtCore.Qt.AlignVCenter)
        self.root_layout.addWidget(self.alert_parent)
        self.verticalLayout.addWidget(self.alert_root)

        self.retranslateUi(alert_win)
        QtCore.QMetaObject.connectSlotsByName(alert_win)

    def retranslateUi(self, alert_win):
        pass

