# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'facerecognition.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window_widget(object):
    def setupUi(self, window_widget):
        window_widget.setObjectName("window_widget")
        window_widget.resize(1920, 1080)
        window_widget.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(window_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_widget = QtWidgets.QWidget(window_widget)
        self.main_widget.setStyleSheet("")
        self.main_widget.setObjectName("main_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_widget = QtWidgets.QWidget(self.main_widget)
        self.left_widget.setMinimumSize(QtCore.QSize(126, 0))
        self.left_widget.setMaximumSize(QtCore.QSize(126, 16777215))
        self.left_widget.setStyleSheet("")
        self.left_widget.setObjectName("left_widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.left_widget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 31, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem)
        self.logo_label = QtWidgets.QLabel(self.left_widget)
        self.logo_label.setMinimumSize(QtCore.QSize(126, 100))
        self.logo_label.setMaximumSize(QtCore.QSize(1001, 100))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.logo_label.setFont(font)
        self.logo_label.setStyleSheet("")
        self.logo_label.setText("")
        self.logo_label.setObjectName("logo_label")
        self.verticalLayout_6.addWidget(self.logo_label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 751, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.left_widget)
        spacerItem2 = QtWidgets.QSpacerItem(54, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.mid_widget = QtWidgets.QWidget(self.main_widget)
        self.mid_widget.setMinimumSize(QtCore.QSize(1420, 0))
        self.mid_widget.setMaximumSize(QtCore.QSize(1420, 16777215))
        self.mid_widget.setObjectName("mid_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.mid_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(20, 34, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        self.mid_head_widget = QtWidgets.QWidget(self.mid_widget)
        self.mid_head_widget.setMinimumSize(QtCore.QSize(0, 188))
        self.mid_head_widget.setMaximumSize(QtCore.QSize(16777215, 188))
        self.mid_head_widget.setStyleSheet("")
        self.mid_head_widget.setObjectName("mid_head_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.mid_head_widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.title_label = QtWidgets.QLabel(self.mid_head_widget)
        self.title_label.setMinimumSize(QtCore.QSize(0, 100))
        self.title_label.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_4.addWidget(self.title_label)
        self.title_desc_label = QtWidgets.QLabel(self.mid_head_widget)
        self.title_desc_label.setMaximumSize(QtCore.QSize(1300, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.title_desc_label.setFont(font)
        self.title_desc_label.setWordWrap(True)
        self.title_desc_label.setObjectName("title_desc_label")
        self.verticalLayout_4.addWidget(self.title_desc_label)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addWidget(self.mid_head_widget)
        self.mid_body_widget = QtWidgets.QWidget(self.mid_widget)
        self.mid_body_widget.setObjectName("mid_body_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mid_body_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mid_body_left_widget = QtWidgets.QWidget(self.mid_body_widget)
        self.mid_body_left_widget.setStyleSheet("")
        self.mid_body_left_widget.setObjectName("mid_body_left_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.mid_body_left_widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.camera_label = QtWidgets.QLabel(self.mid_body_left_widget)
        self.camera_label.setMinimumSize(QtCore.QSize(0, 480))
        self.camera_label.setMaximumSize(QtCore.QSize(16777215, 480))
        self.camera_label.setStyleSheet("background-color: rgb(255, 186, 63);")
        self.camera_label.setText("")
        self.camera_label.setObjectName("camera_label")
        self.verticalLayout_5.addWidget(self.camera_label)
        spacerItem6 = QtWidgets.QSpacerItem(20, 44, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem6)
        self.title_record_label = QtWidgets.QLabel(self.mid_body_left_widget)
        self.title_record_label.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title_record_label.setFont(font)
        self.title_record_label.setObjectName("title_record_label")
        self.verticalLayout_5.addWidget(self.title_record_label)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem7)
        self.record_list_widget = QtWidgets.QWidget(self.mid_body_left_widget)
        self.record_list_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.record_list_widget.setStyleSheet("")
        self.record_list_widget.setObjectName("record_list_widget")
        self.verticalLayout_5.addWidget(self.record_list_widget)
        self.horizontalLayout_2.addWidget(self.mid_body_left_widget)
        self.line_widget = QtWidgets.QWidget(self.mid_body_widget)
        self.line_widget.setObjectName("line_widget")
        self.widget = QtWidgets.QWidget(self.line_widget)
        self.widget.setGeometry(QtCore.QRect(50, 0, 1, 480))
        self.widget.setStyleSheet("background-color: rgb(120, 132, 147);")
        self.widget.setObjectName("widget")
        self.horizontalLayout_2.addWidget(self.line_widget)
        self.mid_body_right_weight = QtWidgets.QWidget(self.mid_body_widget)
        self.mid_body_right_weight.setStyleSheet("")
        self.mid_body_right_weight.setObjectName("mid_body_right_weight")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.mid_body_right_weight)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 70)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.confidence_frame = QtWidgets.QFrame(self.mid_body_right_weight)
        self.confidence_frame.setStyleSheet("background-color: rgb(91, 105, 149, 102);\n"
"border-radius: 8px;\n"
"border-radius: 8px;")
        self.confidence_frame.setObjectName("confidence_frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.confidence_frame)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.slider_title_frame = QtWidgets.QFrame(self.confidence_frame)
        self.slider_title_frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.slider_title_frame.setStyleSheet("background-color: rgb(79, 90, 126);\n"
"border-radius: 8px 8px 0px 0px;")
        self.slider_title_frame.setObjectName("slider_title_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.slider_title_frame)
        self.horizontalLayout_4.setContentsMargins(30, 13, 0, 13)
        self.horizontalLayout_4.setSpacing(15)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.threshold_text_label = QtWidgets.QLabel(self.slider_title_frame)
        self.threshold_text_label.setStyleSheet("font-family: SourceHanSansCN-Bold;\n"
"font-size: 32px;\n"
"color: #FFFFFF;\n"
"line-height: 48px;\n"
"background:transparent;")
        self.threshold_text_label.setObjectName("threshold_text_label")
        self.horizontalLayout_4.addWidget(self.threshold_text_label, 0, QtCore.Qt.AlignLeft)
        self.pushButton = QtWidgets.QPushButton(self.slider_title_frame)
        self.pushButton.setStyleSheet("*{\n"
"width: 32px;\n"
"height: 32px;\n"
"opacity: 0.5;\n"
"border-image: url(:/resource/ic_info.png);\n"
"background-color:transparent;\n"
"}\n"
"*:pressed {\n"
"border-image: url(:/resource/ic_info_press.png);\n"
"}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        spacerItem8 = QtWidgets.QSpacerItem(557, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.verticalLayout_8.addWidget(self.slider_title_frame)
        self.slider_widget = QtWidgets.QWidget(self.confidence_frame)
        self.slider_widget.setStyleSheet("background-color:transparent;")
        self.slider_widget.setObjectName("slider_widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.slider_widget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_8.addWidget(self.slider_widget)
        self.verticalLayout_8.setStretch(1, 157)
        self.verticalLayout_3.addWidget(self.confidence_frame)
        spacerItem9 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem9)
        self.sample_widget = QtWidgets.QWidget(self.mid_body_right_weight)
        self.sample_widget.setStyleSheet("")
        self.sample_widget.setObjectName("sample_widget")
        self.verticalLayout_3.addWidget(self.sample_widget)
        self.verticalLayout_3.setStretch(1, 554)
        self.verticalLayout_3.setStretch(2, 20)
        self.horizontalLayout_2.addWidget(self.mid_body_right_weight)
        self.horizontalLayout_2.setStretch(0, 32)
        self.horizontalLayout_2.setStretch(1, 5)
        self.horizontalLayout_2.setStretch(2, 34)
        self.verticalLayout_2.addWidget(self.mid_body_widget)
        self.horizontalLayout.addWidget(self.mid_widget)
        self.right_widget = QtWidgets.QWidget(self.main_widget)
        self.right_widget.setMinimumSize(QtCore.QSize(320, 0))
        self.right_widget.setMaximumSize(QtCore.QSize(320, 16777215))
        self.right_widget.setStyleSheet("")
        self.right_widget.setObjectName("right_widget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.right_widget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem10 = QtWidgets.QSpacerItem(20, 53, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem10)
        self.widget_9 = QtWidgets.QWidget(self.right_widget)
        self.widget_9.setMinimumSize(QtCore.QSize(0, 60))
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem11 = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem11)
        self.close_Button = QtWidgets.QPushButton(self.widget_9)
        self.close_Button.setMinimumSize(QtCore.QSize(24, 24))
        self.close_Button.setMaximumSize(QtCore.QSize(24, 24))
        self.close_Button.setAutoFillBackground(False)
        self.close_Button.setStyleSheet("* { \n"
"background-color:  transparent;\n"
"border-image: url(\":/resource/ic_close.png\") ;\n"
"}\n"
"\n"
"*:pressed {\n"
"border-image: url(\":/resource/ic_close_press.png\") ;\n"
"}")
        self.close_Button.setText("")
        self.close_Button.setIconSize(QtCore.QSize(24, 24))
        self.close_Button.setCheckable(False)
        self.close_Button.setAutoDefault(False)
        self.close_Button.setDefault(False)
        self.close_Button.setFlat(True)
        self.close_Button.setObjectName("close_Button")
        self.horizontalLayout_3.addWidget(self.close_Button)
        spacerItem12 = QtWidgets.QSpacerItem(53, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)
        self.verticalLayout_7.addWidget(self.widget_9)
        spacerItem13 = QtWidgets.QSpacerItem(20, 937, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem13)
        self.horizontalLayout.addWidget(self.right_widget)
        self.verticalLayout.addWidget(self.main_widget)

        self.retranslateUi(window_widget)
        QtCore.QMetaObject.connectSlotsByName(window_widget)

    def retranslateUi(self, window_widget):
        _translate = QtCore.QCoreApplication.translate
        window_widget.setWindowTitle(_translate("window_widget", "Form"))
        self.title_label.setText(_translate("window_widget", "无感人脸打卡"))
        self.title_desc_label.setText(_translate("window_widget", "无感打卡基于人脸识别算法，将样本和实时人脸进行快速比对，并输出比对结果与实践，可用于身份验证"))
        self.title_record_label.setText(_translate("window_widget", "打卡记录"))
        self.threshold_text_label.setText(_translate("window_widget", "置信度设置"))
