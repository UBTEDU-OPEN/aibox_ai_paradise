#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys

from PyQt5.QtCore import QObject
from oneai.posenet_solver import PosenetSolver
from oneai.common.utils.image_helper import ImageHelper

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class PoseNetModel(QObject):

    def __init__(self):
        super().__init__()
        self.solver = None
        self.load_state = False

    def load(self):
        if self.load_state:
            return True
        if self.solver is None:
            self.solver = PosenetSolver()
        try:
            self.solver.load()
            self.load_state = True
        except:
            self.load_state = False
        return self.load_state

    def detect_pose(self, image):
        if self.load_state:
            image = ImageHelper.convert_undistorted_img(image)
            return self.solver.detect(image)

    def unload(self):
        if self.solver is not None:
            self.solver.unload()
            self.load_state = False
            self.solver = None
