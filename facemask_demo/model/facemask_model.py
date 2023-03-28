#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : facemask_model.py
# Created   : 2020/5/29 4:46 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
# 

class FacemaskModel(object):

    def __init__(self):
        self.confidenceLevel = 0
        self.wareMaskCount = 0
        self.unwareMaskCount = 0
        self.voiceMute = False