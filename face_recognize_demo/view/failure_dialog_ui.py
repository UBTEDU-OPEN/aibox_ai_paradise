# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'failure_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(603, 222)
        Dialog.setStyleSheet("background: transparent;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setStyleSheet("background: #FFFFFF;\n"
"border-radius: 8px;\n"
"border-radius: 8px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 30, 0, 30)
        self.verticalLayout.setSpacing(35)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("font-family: SourceHanSansCN;\n"
"font-weigth: bold;\n"
"font-size: 24px;\n"
"color: #141A30;\n"
"text-align: center;\n"
"line-height: 48px;")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.pb_ok = QtWidgets.QPushButton(self.frame)
        self.pb_ok.setMinimumSize(QtCore.QSize(120, 50))
        self.pb_ok.setStyleSheet("background: #9189FE;\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-family: SourceHanSansCN;\n"
"font-weight: bold;\n"
"font-size: 20px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")
        self.pb_ok.setObjectName("pb_ok")
        self.verticalLayout.addWidget(self.pb_ok, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "录入失败，请重新拍照"))
        self.pb_ok.setText(_translate("Dialog", "好的"))

