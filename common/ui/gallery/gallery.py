# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gallery.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Gallery(object):
    def setupUi(self, Gallery):
        Gallery.setObjectName("Gallery")
        Gallery.resize(1920, 1080)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Gallery.sizePolicy().hasHeightForWidth())
        Gallery.setSizePolicy(sizePolicy)
        Gallery.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Gallery)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pop = QtWidgets.QWidget(Gallery)
        self.pop.setMinimumSize(QtCore.QSize(273, 298))
        self.pop.setMaximumSize(QtCore.QSize(273, 298))
        self.pop.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.pop.setObjectName("pop")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pop)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.arrow = QtWidgets.QLabel(self.pop)
        self.arrow.setEnabled(True)
        self.arrow.setMinimumSize(QtCore.QSize(46, 13))
        self.arrow.setMaximumSize(QtCore.QSize(46, 13))
        self.arrow.setText("")
        self.arrow.setObjectName("arrow")
        self.verticalLayout_2.addWidget(self.arrow, 0, QtCore.Qt.AlignHCenter)
        self.content = QtWidgets.QFrame(self.pop)
        self.content.setStyleSheet("background-color:#FFFFFF;\n"
"border-radius: 10px;")
        self.content.setObjectName("content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.content)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2.addWidget(self.content)
        self.verticalLayout.addWidget(self.pop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Gallery)
        QtCore.QMetaObject.connectSlotsByName(Gallery)

    def retranslateUi(self, Gallery):
        pass

