import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from photo_to_cartoon_demo.view.cartoon_main_view import CartoonMainUI

FONT_STRING = "Source Han Sans CN"

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import resources_rc

def qapp():
    if QApplication.instance():
        _app = QApplication.instance()
    else:
        _app = QApplication(sys.argv)
    return _app

def cartoon_main():
    if (FONT_STRING not in QtGui.QFontDatabase().families()) and ("思源黑体 CN" not in QtGui.QFontDatabase().families()):
        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../common/resource/font/SourceHanSansCN-Bold.otf"))

        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../common/resource/font/SourceHanSansCN-Regular.otf"))

    app = qapp()
    window = CartoonMainUI()
    window.showFullScreen()
    app.processEvents()
    # window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    cartoon_main()