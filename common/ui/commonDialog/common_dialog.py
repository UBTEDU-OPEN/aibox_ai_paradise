# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'empty_sample_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(626, 220)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(29, 48, 29, 48)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font-family: SourceHanSansCN-Bold;\n"
"font-size: 28px;\n"
"color: #141A30;\n"
"text-align: center;\n"
"line-height: 48px;\n"
"background: transparent;")

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignHCenter)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(50)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 30)
        self.pb_cancel = QPushButton(Dialog)
        self.pb_cancel.setObjectName(u"pb_cancel")
        self.pb_cancel.setMinimumSize(QSize(200, 80))
        self.pb_cancel.setStyleSheet(u"background: #4F5A7E;\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-family: SourceHanSansCN-Bold;\n"
"font-size: 28px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")

        self.horizontalLayout_2.addWidget(self.pb_cancel, 0, Qt.AlignRight)

        self.pb_ok = QPushButton(Dialog)
        self.pb_ok.setObjectName(u"pb_ok")
        self.pb_ok.setMinimumSize(QSize(200, 80))
        self.pb_ok.setStyleSheet(u"background: #FF9584;\n"
"border-radius: 8px;\n"
"border-radius: 8px;\n"
"font-family: SourceHanSansCN-Bold;\n"
"font-size: 28px;\n"
"color: #FFFFFF;\n"
"text-align: center;\n"
"line-height: 48px;")

        self.horizontalLayout_2.addWidget(self.pb_ok, 0, Qt.AlignLeft)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6e05\u7a7a\u4eba\u8138\u4fe1\u606f\u5c06\u4e0d\u53ef\u627e\u56de\uff0c\u786e\u5b9a\u8981\u5168\u90e8\u6e05\u7a7a\u5417\uff1f", None))
        self.pb_cancel.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
        self.pb_ok.setText(QCoreApplication.translate("Dialog", u"\u5168\u90e8\u6e05\u7a7a", None))
    # retranslateUi

