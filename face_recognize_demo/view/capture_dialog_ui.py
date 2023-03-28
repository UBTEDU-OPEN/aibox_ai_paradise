# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capture_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(680, 249)
        Dialog.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setStyleSheet("background: #FFFFFF;\n"
"border-radius: 8px;\n"
"border-radius: 8px;")
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 48, 0, 48)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("font-family: Source Han Sans CN;\n"
"font-weight: bold;\n"
"font-size: 24px;\n"
"color: #141A30;\n"
"text-align: center;\n"
"line-height: 48px;\n"
"background: transparent;")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(115, -1, 115, 30)
        self.horizontalLayout_3.setSpacing(50)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pb_cancel = QtWidgets.QPushButton(self.frame)
        self.pb_cancel.setMinimumSize(QtCore.QSize(120, 50))
        self.pb_cancel.setStyleSheet("font-family: Source Han Sans CN;\n"
"font-weight: bold;\n"
"background: #4F5A7E;\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-size: 20px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")
        self.pb_cancel.setAutoDefault(False)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout_3.addWidget(self.pb_cancel, 0, QtCore.Qt.AlignRight)
        self.pb_capture = QtWidgets.QPushButton(self.frame)
        self.pb_capture.setMinimumSize(QtCore.QSize(120, 50))
        self.pb_capture.setStyleSheet("font-family: Source Han Sans CN;\n"
"font-weight: bold;\n"
"background: #9189FE;\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-size: 20px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")
        self.pb_capture.setDefault(True)
        self.pb_capture.setObjectName("pb_capture")
        self.horizontalLayout_3.addWidget(self.pb_capture, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.setStretch(0, 130)
        self.verticalLayout.setStretch(1, 145)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "请在人形框变为绿色时拍照"))
        self.pb_cancel.setText(_translate("Dialog", "取消"))
        self.pb_capture.setText(_translate("Dialog", "拍照"))

