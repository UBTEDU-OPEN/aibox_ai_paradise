# This Python file uses the following encoding: utf-8
import sys,os
from PyQt5 import QtGui
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import resources_rc
sys.path.append('..')
from face_recognize_demo.com import ubt_device
from face_recognize_demo.com.demo_type import DemoType, Type
from face_recognize_demo.view.trackrecognition_main_ui import TrackrecognitionMainUI

FONT_STRING = "Source Han Sans CN"

def track_recognition_main():
    DemoType(demo_type=Type.track_demo_item)

    if (FONT_STRING not in QtGui.QFontDatabase().families()) and ("思源黑体 CN" not in QtGui.QFontDatabase().families()):
        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../common/resource/font/SourceHanSansCN-Bold.otf"))

        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../common/resource/font/SourceHanSansCN-Regular.otf"))

    cfgpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "language/local/")

    window = TrackrecognitionMainUI(configure_file_path=cfgpath, option="track_recognition_string", domain='tracking_messages')
    window.showFullScreen()
    sys.exit(ubt_device.app.exec_())
    pass


if __name__ == "__main__":
    track_recognition_main()
