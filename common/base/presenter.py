# -*-coding:utf-8 -*-
from PyQt5 import QtCore


class Presenter(QtCore.QObject):
    
    def __init__(self, view):
        super(Presenter, self).__init__()

        self._view = view
        self._model = None

    @property
    def view(self):
        """

        :return:
        """
        return self._view

    @property
    def model(self):
        """

        :return:
        """
        return self._model

