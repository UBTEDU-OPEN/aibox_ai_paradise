# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

app = QApplication([])

kscreen_width = 1920
kscreen_height = 1080

desktop = QtWidgets.QApplication.desktop()
desk_screen_width = desktop.width()
desk_screen_height = desktop.height()

scale_width = desk_screen_width / kscreen_width
scale_height = desk_screen_height / kscreen_height
