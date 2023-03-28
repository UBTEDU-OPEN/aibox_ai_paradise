#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:splash.py
# Created:2020/6/3 下午7:47
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import time


class MyWindow(QtWidgets.QPushButton):

    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.setText("关闭窗口")
        # self.clicked.connect(QtWidgets.qApp.quit)

    def load_data(self, sp):
        # index = 0
        # while True:
        #     sp.setPixmap(QtGui.QPixmap("resource/images/launch_animation_0000" + str(index) + ".png"))
        #     index += 1
        #     QtWidgets.qApp.processEvents()  # 允许主进程处理事件
        #     if index == 90:
        #         index = 0
        index = 0
        while True:  # 模拟主程序加载过程
            time.sleep(1)  # 加载数据
            # sp.setPixmap()
            sp.showMessage("加载... {0}%".format(index), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
            # sp.setPixmap(QtGui.QPixmap("resource/images/launch_animation_0000" + str(index) + ".png"))
            QtWidgets.qApp.processEvents()  # 允许主进程处理事件
            index += 1
            if index == 90:
                index = 0


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("resource/images/launch_animation_00000.png"))
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()  # 显示启动界面
    QtWidgets.qApp.processEvents()  # 处理主进程事件
    window = MyWindow()
    window.setWindowTitle("QSplashScreen类使用")
    window.resize(300, 30)
    window.load_data(splash)  # 加载数据
    window.show()
    splash.finish(window)  # 隐藏启动界面
