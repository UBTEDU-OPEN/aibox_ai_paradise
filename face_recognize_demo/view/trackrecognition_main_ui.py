import sys
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import *

from face_recognize_demo.com import ubt_device
from face_recognize_demo.presenter.mainwindow_presenter import MainwindowPresenter
from face_recognize_demo.record.record_list_widget import RecordListWidget
from face_recognize_demo.record.record_presenter import RecordPresenter
from face_recognize_demo.sample.sample_list_widget import FaceSampleList
from face_recognize_demo.view.capture_mask_widget import PhotoBackgroundWidget
from face_recognize_demo.view.facerecognition_ui import Ui_window_widget
from face_recognize_demo.view.ubt_camera_widget import Camera_Widget

sys.path.append('..')
from common.ui.slider.slider import Slider
from common.ui.loading.load import Load
from common.utility.common_utility import CommonUtil
from common.utility.configure_string_single import  ConfigureStringSingle

kmid_widget_width = 1420
kleft_widget_width = 126
kright_widget_width = 320


k_confidence_widget_height = 217
k_confidence_widget_width = 680

k_sample_widget_height = 545
k_sample_widget_width = 680

k_main_header_widget_width = 1420
k_main_header_widget_height = 188

k_camera_label_width = 640
k_camera_label_height = 480

from common.ui.bubbleDialog.popwindow import PopWindow

class TrackrecognitionMainUI(QWidget, Ui_window_widget):

    # signals
    add_sample_clicked = Signal()
    close_button_clicked = Signal()
    delete_sample_item_clicked = Signal(str)
    delete_all_sample_clicked = Signal()
    threshold_changed = Signal(int)
    threshold_tip_clicked = Signal()

    def __init__(self, parent=None, configure_file_path=None, option=None, domain=None):
        super(TrackrecognitionMainUI, self).__init__(parent)

        self.conf = ConfigureStringSingle(configure_file_path, domain)
        self.common_configure = ConfigureStringSingle.get_common_string_cfg()

        self.show_loading()

        self.setupUi(self)

        self.configureSize()

        self.configureFont()

        '''资源文件配置'''
        logo_pixmap = QPixmap(":/resource/logo.png")
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setScaledContents(True)
        # self.close_Button.setIcon(QIcon(":/resource/ic_close.png"))

        self.init_camera_ui()

        self.init_record_ui()

        self.init_smaple_ui()

        '''添加关闭窗口事件'''
        self.close_Button.clicked.connect(self.close_button_clicked)

        self.pop = PopWindow(self.pushButton, parent=self)

        # add custom slider
        self.init_slider_ui()

        '''添加样本控件'''
        self.init_photo_ui()

        self.main_widget.setStyleSheet("QWidget#main_widget{border-image: url(:/resource/backgroud.png)}")

        self.configure_string()

        self.presenter = MainwindowPresenter(self, option, self.conf)

    def configure_string(self):
        """

        :return:
        """
        self.title_label.setText(self.conf.get_value_for_key("k_title"))
        self.title_desc_label.setText(self.conf.get_value_for_key("k_title_desc"))
        self.camera_label.setScaledContents(True)
        self.title_record_label.setText(self.conf.get_value_for_key("k_record"))
        self.threshold_text_label.setText(self.conf.get_value_for_key('k_threshold_title'))

    def showRecord(self, records):
        self.recordPresenter.update_records(records)

    def showRecognitionResult(self, image):
        self.camera.bg_pixmap = image
        self.camera.update()

    def init_camera_ui(self):
        """

        :return:
        """
        self.camera_label.setStyleSheet("background-color: transparent")
        self.camera = Camera_Widget(self.camera_label)
        self.camera.setGeometry(0, 0, k_camera_label_width * ubt_device.scale_width,
                                k_camera_label_height * ubt_device.scale_height)

    def init_record_ui(self):
        """

        :return:
        """
        self.record_list_widget = RecordListWidget(self.record_list_widget)
        self.record_list_widget.setGeometry(0, 0, k_camera_label_width * ubt_device.scale_width,
                                            k_camera_label_height * ubt_device.scale_height)
        self.recordPresenter = RecordPresenter(self.record_list_widget)

    def init_smaple_ui(self):
        """

        :return:
        """
        self.sample_list_widget = FaceSampleList(self.sample_widget, self.conf,
                                                 self.setPhotoStatu)
        self.sample_list_widget.setGeometry(0, 0, k_sample_widget_width * ubt_device.scale_width,
                                            k_sample_widget_height * ubt_device.scale_height)
        self.sample_list_widget.button_item_clicked.connect(self.add_sample_clicked)
        self.sample_list_widget.delete_item_clicked.connect(self.delete_sample_item_clicked)
        self.sample_list_widget.clear_item_clicked.connect(self.delete_all_sample_clicked)

    '''添加样本ui'''
    def init_photo_ui(self):
        """

        :return:
        """
        self.photo_widget = PhotoBackgroundWidget(self.mid_body_left_widget)
        self.photo_widget.setGeometry(0, 0, k_camera_label_width * ubt_device.scale_width, k_camera_label_height * ubt_device.scale_height)
        self.photo_widget.hide()

    def init_slider_ui(self):
        self.slider = Slider(75, default_desc=self.conf.get_value_for_key('k_thresold_default_desc'))
        self.slider_widget.layout().addWidget(self.slider)
        self.slider.value_changed.connect(self.threshold_changed)

    def setPhotoStatu(self):
        self.add_sample_clicked.emit()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(0, 0, ubt_device.desk_screen_width, ubt_device.desk_screen_height, QPixmap(":/resource/backgroud.png"))
        painter.end()

    def configureSize(self):
        """按照比例系数设置主容器的宽高

        :return:
        """
        self.left_widget.setFixedWidth(kleft_widget_width * ubt_device.scale_width)
        self.mid_widget.setFixedWidth(kmid_widget_width * ubt_device.scale_width)

        self.right_widget.setFixedWidth(kright_widget_width * ubt_device.scale_width)

        self.sample_widget.setFixedWidth(k_sample_widget_width * ubt_device.scale_width)
        self.sample_widget.setFixedHeight(k_sample_widget_height * ubt_device.scale_height)

        self.camera_label.setFixedWidth(k_camera_label_width * ubt_device.scale_width)
        self.camera_label.setFixedHeight(k_camera_label_height * ubt_device.scale_height)

        self.confidence_frame.setFixedWidth(k_confidence_widget_width * ubt_device.scale_width)
        self.confidence_frame.setFixedHeight(k_confidence_widget_height * ubt_device.scale_height)

        self.mid_head_widget.setFixedWidth(k_main_header_widget_width * ubt_device.scale_width)
        self.mid_head_widget.setFixedHeight(k_main_header_widget_height * ubt_device.scale_height)

    def configureFont(self):
        """ 配置字体

        :return:
        """
        title_font = QFont("Source Han Sans CN")
        title_font.setWeight(QFont.Bold)
        title_font.setPixelSize(36)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("QLabel#title_label{color:#ffffff;}")

        title_desc_font = QFont("Source Han Sans CN")
        title_desc_font.setWeight(QFont.Normal)
        title_desc_font.setPixelSize(18)

        self.title_desc_label.setFont(title_desc_font)
        self.title_desc_label.setStyleSheet("QLabel#title_desc_label{color:#787A93;}")

        title_record_font = QFont("Source Han Sans CN")
        title_record_font.setWeight(QFont.Bold)
        title_record_font.setPixelSize(20)
        self.title_record_label.setFont(title_record_font)
        self.title_record_label.setStyleSheet("QLabel#title_record_label{color:#FFFFFF;}")

        threshold_record_font = QFont("Source Han Sans CN")
        threshold_record_font.setWeight(QFont.Bold)
        threshold_record_font.setPixelSize(24)
        self.threshold_text_label.setFont(threshold_record_font)
        self.threshold_text_label.setStyleSheet("QLabel#threshold_text_label{color:#FFFFFF;}")

    def load_stylesheet(self):
        """ 加载stylesheet设置

        :return:
        """
        qss_path = ":/resource/qss/default.qss"
        with open(qss_path) as fp:
            qss = fp.read()
            self.setStyleSheet(qss)

    def enter_capture_mode(self):
        """ 进入拍照模式

        """
        self.photo_widget.show()
        self.set_capture_no_face()

    def set_capture_no_face(self):
        """ 拍照模式下未发现人脸

        """
        self.photo_widget.setStatus(PhotoBackgroundWidget.Status.NO_FACE)

    def set_capture_valid(self):
        """ 拍照模式下发现未注册人脸

        """
        self.photo_widget.setStatus(PhotoBackgroundWidget.Status.UNKNOWN_FACE)

    def set_capture_not_valid(self):
        """ 拍照模式下发现已注册人脸

        """
        self.photo_widget.setStatus(PhotoBackgroundWidget.Status.KNOWN_FACE)


    def quit_capture_mode(self):
        """

        :return:
        """
        self.photo_widget.hide()
        self.photo_widget.setStatus(PhotoBackgroundWidget.Status.NO_FACE)

    def add_sample_item(self, image, name):
        """

        :param image:
        :param name:
        :return:
        """
        self.sample_list_widget.add_item(image, name)
        self.sample_list_widget.set_status_for_item_added()

    def delete_sample_item(self, name):
        """

        :param item:
        """
        self.sample_list_widget.delete_item(name)

    def delete_all_samples(self):
        """

        :return:
        """
        self.sample_list_widget.delete_all_items()

    def set_list_status_for_item_added(self):
        """

        :return:
        """
        self.sample_list_widget.set_status_for_item_added()

    def set_list_status_for_empty(self):
        """

        :return:
        """
        self.sample_list_widget.set_status_for_empty_list()

    def get_sample_list_count(self):
        """

        :return:
        """
        return self.sample_list_widget.get_item_count()

    def show_recognition_mask(self, show):
        pass

    def show_loading(self):
        """ 显示加载界面

        """
        self.loading = Load(50*1000)

    def close_loading(self):
        """ 关闭加载界面

        """
        self.loading.dismiss()

    def showEvent(self, e) -> None:
        print('showEvent')
        CommonUtil.contol_cpu_wake(True)

    def closeEvent(self, e) -> None:
        print('closeEvent')
        CommonUtil.contol_cpu_wake(False)

    def changeEvent(self, e) -> None:
        if self.isActiveWindow():
            CommonUtil.contol_cpu_wake(True)
        else:
            CommonUtil.contol_cpu_wake(False)

