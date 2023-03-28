#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:common_utility.py
# Created:2020/6/28 上午11:20
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:commonutil
import glob
import os
import sys

import cv2

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class CommonUtil(object):

    @classmethod
    def get_camera(cls, width=640, height=480):
        device_list = glob.glob("/dev/video[0-9]")
        if len(device_list) == 0:
            device_list = ["/dev/video0"]
        cap = None
        for device in device_list:
            cap = cv2.VideoCapture(CommonUtil._gst_str(device, width, height), cv2.CAP_GSTREAMER)
            if cap.isOpened():
                return cap
        return cap

    @classmethod
    def _gst_str(cls, device, width=640, height=480):
        """ Nvidia gst parameter

        :param device: /dev/video[0-9];
        :return:
        """
        return 'v4l2src device={} ! video/x-raw, width=(int){}, height=(int){}, framerate=(fraction){}/1 ! ' \
               'videoconvert !  video/x-raw, format=(string)BGR ! appsink'.format(
            device, width, height, 30)

    @classmethod
    def contol_cpu_wake(cls, enable):
        """
        控制系统休眠状态
        ： param enable:true:休眠设置不生效;false:生效
        """
        if enable:
            os.system(
                "xfconf-query -c xfce4-power-manager -np '/xfce4-power-manager/presentation-mode' -t 'bool' -s true")
        else:
            os.system(
                "xfconf-query -c xfce4-power-manager -np '/xfce4-power-manager/presentation-mode' -t 'bool' -s false")


if __name__ == '__main__':
    print(CommonUtil.get_camera())
