#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:style_model.py
# Created:2020/9/23 下午3:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:风格迁移model
import os
import sys

from PyQt5.QtCore import QObject

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from oneai.style_transfer_solver import StyleTransferSolver


class StyleModel(QObject):

    def __init__(self):
        super().__init__()
        self.solver = None

    def load(self, style_id):
        if self.solver is None:
            self.solver = StyleTransferSolver()
        try:
            self.solver.load(style_id)
        except:
            pass

    def transfer(self, image_path):
        out = None
        if self.solver is None:
            self.solver = StyleTransferSolver()
        try:
            out = self.solver.transfer(image_path)
        except:
            pass
        return out

    def unload(self):
        if self.solver is not None:
            self.solver.unload()
            self.solver = None
