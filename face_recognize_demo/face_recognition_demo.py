# This Python file uses the following encoding: utf-8
import sys,os

from PyQt5 import QtGui

sys.path.append('..')
from face_recognize_demo.com import ubt_device
from face_recognize_demo.com.demo_type import DemoType, Type
from face_recognize_demo.view.facerecognition_main_ui import FaceRecognitionMainUI

FONT_STRING = "Source Han Sans CN"

def facerecognition_main():
    if (FONT_STRING not in QtGui.QFontDatabase().families()) and ("思源黑体 CN" not in QtGui.QFontDatabase().families()):
        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../common/resource/font/SourceHanSansCN-Bold.otf"))

        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../common/resource/font/SourceHanSansCN-Regular.otf"))

    # cfgpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configure_string/face_recognition_string_configure.ini")

    DemoType(demo_type=Type.face_demo_item)
    cfgpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "language/local/")

    window = FaceRecognitionMainUI(configure_file_path=cfgpath, option="face_recognition_string", domain='messages')

    window.showFullScreen()
    sys.exit(ubt_device.app.exec_())

if __name__ == "__main__":
    facerecognition_main()

