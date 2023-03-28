
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QPixmap
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import resources_rc

from face_recognize_demo.com import ubt_device
from face_recognize_demo.view.trackrecognition_main_ui import TrackrecognitionMainUI


class FaceRecognitionMainUI(TrackrecognitionMainUI):

    def __init__(self, parent=None, configure_file_path=None, option=None, domain=None):
        super(FaceRecognitionMainUI, self).__init__(parent=parent, configure_file_path=configure_file_path, option=option, domain=domain)

        self.recognition_mask_label = QLabel(self.camera_label)
        self.recognition_mask_label.setScaledContents(True)
        self.recognition_mask_label.setGeometry(29 * ubt_device.scale_width, 29 * ubt_device.scale_height, 582 * ubt_device.scale_width, 422 * ubt_device.scale_height)
        pixmap = QPixmap(":/resource/img_recognize_mask.png")
        self.recognition_mask_label.setPixmap(pixmap)

    def show_recognition_mask(self, show):
        if show:
            self.recognition_mask_label.show()
        else:
            self.recognition_mask_label.hide()


