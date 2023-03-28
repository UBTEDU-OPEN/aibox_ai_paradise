# -*-coding:utf-8 -*-
from PyQt5 import QtCore


class View(QtCore.QObject):

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
