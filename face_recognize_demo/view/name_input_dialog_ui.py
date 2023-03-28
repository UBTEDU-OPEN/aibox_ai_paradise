# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'name_input_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(680, 240)
        Dialog.setMinimumSize(QtCore.QSize(680, 240))
        Dialog.setStyleSheet("background: #FFFFFF;\n"
"border-radius: 8px;\n"
"border-radius: 8px;")
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 25, 0, 30)
        self.verticalLayout.setSpacing(25)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(126, 30, 126, 30)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_input = QtWidgets.QFrame(Dialog)
        self.frame_input.setStyleSheet("background-color: rgba(79,90, 126, 0.2);\n"
"border-radius: 8px;\n"
"border-radius: 8px;")
        self.frame_input.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_input.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_input.setLineWidth(0)
        self.frame_input.setObjectName("frame_input")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_input)
        self.horizontalLayout_2.setContentsMargins(30, 10, 30, 10)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.le_name_input = QtWidgets.QLineEdit(self.frame_input)
        self.le_name_input.setStyleSheet("font-family: SourceHanSansCN;\n"
"font-weight: bold;\n"
"font-size: 24px;\n"
"color: #141A30;\n"
"line-height: 48px;\n"
"background-color: transparent;")
        self.le_name_input.setMaxLength(10)
        self.le_name_input.setObjectName("le_name_input")
        self.horizontalLayout_2.addWidget(self.le_name_input)
        self.horizontalLayout_3.addWidget(self.frame_input)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_cancel = QtWidgets.QPushButton(Dialog)
        self.pb_cancel.setMinimumSize(QtCore.QSize(120, 50))
        self.pb_cancel.setStyleSheet("background: #4F5A7E;\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-family: SourceHanSansCN;\n"
"font-weight: bold;\n"
"font-size: 20px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")
        self.pb_cancel.setCheckable(False)
        self.pb_cancel.setAutoDefault(False)
        self.pb_cancel.setFlat(True)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout.addWidget(self.pb_cancel, 0, QtCore.Qt.AlignRight)
        self.pb_ok = QtWidgets.QPushButton(Dialog)
        self.pb_ok.setMinimumSize(QtCore.QSize(120, 50))
        self.pb_ok.setStyleSheet(":enabled{\n"
"background: rgb(145,137,254);\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-family: SourceHanSansCN;\n"
"font-weight: bold;\n"
"font-size: 20px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;\n"
"}\n"
"\n"
":disabled {\n"
"background: rgb(145,137,254, 77);\n"
"color: #FFFFFF;\n"
"}\n"
"")
        self.pb_ok.setDefault(True)
        self.pb_ok.setFlat(True)
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout.addWidget(self.pb_ok, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.le_name_input.setPlaceholderText(_translate("Dialog", "姓名"))
        self.pb_cancel.setText(_translate("Dialog", "取消"))
        self.pb_ok.setText(_translate("Dialog", "录入"))

