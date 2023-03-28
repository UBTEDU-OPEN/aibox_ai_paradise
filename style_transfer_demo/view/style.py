# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'style.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Base(object):
    def setupUi(self, Base):
        Base.setObjectName("Base")
        Base.resize(1590, 784)
        Base.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Base)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.root = QtWidgets.QFrame(Base)
        self.root.setLineWidth(0)
        self.root.setObjectName("root")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.root)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left = QtWidgets.QWidget(self.root)
        self.left.setMinimumSize(QtCore.QSize(150, 0))
        self.left.setMaximumSize(QtCore.QSize(150, 16777215))
        self.left.setObjectName("left")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.left)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.card_icon = QtWidgets.QLabel(self.left)
        self.card_icon.setObjectName("card_icon")
        self.verticalLayout_3.addWidget(self.card_icon, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout.addWidget(self.left, 0, QtCore.Qt.AlignLeft)
        self.main = QtWidgets.QFrame(self.root)
        self.main.setMinimumSize(QtCore.QSize(0, 0))
        self.main.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.main.setObjectName("main")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 100)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.top = QtWidgets.QWidget(self.main)
        self.top.setMaximumSize(QtCore.QSize(16777215, 200))
        self.top.setObjectName("top")
        self.top2 = QtWidgets.QVBoxLayout(self.top)
        self.top2.setContentsMargins(0, 80, 0, 0)
        self.top2.setSpacing(0)
        self.top2.setObjectName("top2")
        self.top_title = QtWidgets.QLabel(self.top)
        self.top_title.setStyleSheet("")
        self.top_title.setObjectName("top_title")
        self.top2.addWidget(self.top_title, 0, QtCore.Qt.AlignBottom)
        self.sub_title = QtWidgets.QLabel(self.top)
        self.sub_title.setStyleSheet("")
        self.sub_title.setObjectName("sub_title")
        self.top2.addWidget(self.sub_title, 0, QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.top2.addItem(spacerItem)
        self.verticalLayout_4.addWidget(self.top)
        spacerItem1 = QtWidgets.QSpacerItem(20, 55, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem1)
        self.operate = QtWidgets.QWidget(self.main)
        self.operate.setMinimumSize(QtCore.QSize(1440, 120))
        self.operate.setMaximumSize(QtCore.QSize(16777215, 150))
        self.operate.setObjectName("operate")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.operate)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.img_scene = QtWidgets.QFrame(self.operate)
        self.img_scene.setObjectName("img_scene")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.img_scene)
        self.horizontalLayout_4.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.img_style = QtWidgets.QFrame(self.img_scene)
        self.img_style.setObjectName("img_style")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.img_style)
        self.horizontalLayout_7.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_4.addWidget(self.img_style)
        self.img_sample = QtWidgets.QFrame(self.img_scene)
        self.img_sample.setObjectName("img_sample")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.img_sample)
        self.horizontalLayout_6.setContentsMargins(50, 0, -1, 0)
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4.addWidget(self.img_sample)
        self.horizontalLayout_2.addWidget(self.img_scene, 0, QtCore.Qt.AlignLeft)
        self.palette = QtWidgets.QFrame(self.operate)
        self.palette.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.palette.setObjectName("palette")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.palette)
        self.horizontalLayout_3.setContentsMargins(50, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2.addWidget(self.palette, 0, QtCore.Qt.AlignLeft)
        self.line_2 = QtWidgets.QFrame(self.operate)
        self.line_2.setStyleSheet("background-color: #212A44;")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2, 0, QtCore.Qt.AlignRight)
        self.btn_export = QtWidgets.QFrame(self.operate)
        self.btn_export.setObjectName("btn_export")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.btn_export)
        self.verticalLayout_9.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_2.addWidget(self.btn_export, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_4.addWidget(self.operate, 0, QtCore.Qt.AlignLeft)
        self.preview = QtWidgets.QWidget(self.main)
        self.preview.setMinimumSize(QtCore.QSize(1440, 0))
        self.preview.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.preview.setObjectName("preview")
        self.preview2 = QtWidgets.QHBoxLayout(self.preview)
        self.preview2.setContentsMargins(0, 45, 0, 0)
        self.preview2.setSpacing(80)
        self.preview2.setObjectName("preview2")
        self.draw = QtWidgets.QWidget(self.preview)
        self.draw.setMinimumSize(QtCore.QSize(0, 0))
        self.draw.setObjectName("draw")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.draw)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.img_handle = QtWidgets.QFrame(self.draw)
        self.img_handle.setMinimumSize(QtCore.QSize(0, 0))
        self.img_handle.setObjectName("img_handle")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.img_handle)
        self.horizontalLayout_5.setContentsMargins(0, 0, 30, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5.addWidget(self.img_handle)
        self.img = QtWidgets.QFrame(self.draw)
        self.img.setMinimumSize(QtCore.QSize(0, 0))
        self.img.setMaximumSize(QtCore.QSize(16777215, 480))
        self.img.setObjectName("img")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.img)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5.addWidget(self.img)
        self.preview2.addWidget(self.draw)
        self.line = QtWidgets.QFrame(self.preview)
        self.line.setStyleSheet("background-color: #4C788493;")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.preview2.addWidget(self.line)
        self.result = QtWidgets.QWidget(self.preview)
        self.result.setObjectName("result")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.result)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.result_label = QtWidgets.QFrame(self.result)
        self.result_label.setObjectName("result_label")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.result_label)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_2.addWidget(self.result_label)
        self.img_result = QtWidgets.QFrame(self.result)
        self.img_result.setMaximumSize(QtCore.QSize(16777215, 480))
        self.img_result.setObjectName("img_result")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.img_result)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_2.addWidget(self.img_result, 0, QtCore.Qt.AlignVCenter)
        self.preview2.addWidget(self.result)
        self.preview2.setStretch(0, 1)
        self.preview2.setStretch(2, 1)
        self.verticalLayout_4.addWidget(self.preview)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.main, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addWidget(self.root)

        self.retranslateUi(Base)
        QtCore.QMetaObject.connectSlotsByName(Base)

    def retranslateUi(self, Base):
        _translate = QtCore.QCoreApplication.translate
        Base.setWindowTitle(_translate("Base", "Base"))
        self.card_icon.setText(_translate("Base", "TextLabel"))
        self.top_title.setText(_translate("Base", "主标题"))
        self.sub_title.setText(_translate("Base", "副标题"))
