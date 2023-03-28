import os
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import Qt

from common.ui.loading.loading_activing import LoadingActiving
from face_recognize_demo.com import ubt_device

from photo_to_cartoon_demo.presenter.cartoon_presenter import CartoonPresenter
from photo_to_cartoon_demo.view.cartoon_fail_dialog import CartoonFailDialog
from photo_to_cartoon_demo.view.cartoon_ui import Ui_cartoon
from common.utility.configure_string_single import ConfigureStringSingle
from photo_to_cartoon_demo.view.save_result_view import SaveResultWidget
from photo_to_cartoon_demo.view.video_view import VideoWidget

sys.path.append('..')
from common.ui.loading.load import Load

k_camera_label_width = 640
k_camera_label_height = 480

#pyrcc5 -o resources_rc.py resources.qrc

class CartoonMainUI(QWidget, Ui_cartoon):
    # 关闭窗口信号
    close_window_clicked = Signal()
    # 拍照按钮点击信号
    capture_btn_clicked = Signal()
    # 生成按钮点击信号
    make_cartoon_btn_clicked = Signal()
    # 保存按钮点击信号
    save_btn_clicked = Signal()
    # 取消拍照
    cancel_capture_clicked = Signal()

    def __init__(self, parent=None):
        super(CartoonMainUI, self).__init__(parent)
        # '/home/oneai/Desktop/ai_application/photo_to_cartoon_demo/language/local/'
        configure_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "language/local/")
        self.configure = ConfigureStringSingle(configure_file_path, domain='messages')

        self.show_loading()

        self.setupUi(self)

        self.close_window_btn.clicked.connect(self.close_window_clicked)
        self.take_picture_btn.clicked.connect(self.capture_btn_clicked)
        self.make_cartoon_btn.clicked.connect(self.make_cartoon_btn_clicked)
        self.save_photo_btn.clicked.connect(self.save_btn_clicked)

        self.init_camera_ui()

        self.init_save_result_ui()

        self.init_ui_style()

        self.configure_string()

        self.configureFont()

        self.presenter = CartoonPresenter(self, self.configure)

    def init_camera_ui(self):
        """
        添加视频区域组件

        """
        self.video_content_lab.setStyleSheet("background-color: transparent")
        self.camera = VideoWidget(self.video_content_lab, cancel_capture=self.cancel_capture)
        self.camera.setGeometry(0, 0, k_camera_label_width * ubt_device.scale_width,
                                k_camera_label_height * ubt_device.scale_height)

    def init_save_result_ui(self):
        """
        展示结果页面组件，隐藏

        """
        self.save_window = SaveResultWidget(self, configure=self.configure)
        self.save_window.setHidden(True)
        self.save_window.setGeometry(0, 0, 1920, 1080)

    def init_ui_style(self):
        """
        初始化UI 风格

        """
        logo_pixmap = QPixmap(":/resources/logo.png")
        self.label_2.setPixmap(logo_pixmap)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.video_content_lab.setScaledContents(True)

        self.cartoon_result_lab.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

        self.close_window_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_close.png)}")
        self.take_picture_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_camera.png)}")

        self.enable_create_cartoon_btn(False)
        self.enable_save_btn(False)

        self.cartoon_result_lab.setHidden(True)

        self.body_left_widget.setStyleSheet("QWidget#body_left_widget{border-image: url(:/resources/img_block.png)}")
        self.body_right_widget.setStyleSheet("QWidget#body_right_widget{border-image: url(:/resources/img_block.png)}")

        self.result_lab.setStyleSheet("QLabel#result_lab{border-image: url(:/resources/result_default.png)}")

        self.cartoon_result_lab.setStyleSheet("QLabel#cartoon_result_lab{background-color:#ffffff;border-radius:8px;}")

        self.line_widget.setStyleSheet("QWidget{background-color:rgba(120, 132, 147,0.4);}")

    def cancel_capture(self):
        """
        取消拍照按钮被点击

        """
        self.cancel_capture_clicked.emit()

    def show_loading(self):
        """
        显示加载界面

        """
        self.loading = Load(50*1000)

    def close_loading(self):
        """
        关闭加载界面

        """
        self.loading.dismiss()

    def configure_string(self):
        """
        配置主界面的文案显示

        """
        self.title_label.setText(self.configure.get_value_for_key("k_title"))
        self.title_desc_label.setText(self.configure.get_value_for_key("k_title_desc"))

        self.capture_tip_lab.setText(self.configure.get_value_for_key("k_capture_tip"))
        self.result_tip_label.setText(self.configure.get_value_for_key("k_save_tip"))

        self.make_cartoon_btn.setText(" " + self.configure.get_value_for_key("k_make_cartoon_btn"))
        self.save_photo_btn.setText(" " + self.configure.get_value_for_key("k_save_btn"))

    def click_make_cartoon(self):
        """
        生成按钮被点击

        """
        self.enable_create_cartoon_btn(False)
        self.camera.enable_cancel_btn(False)

    def show_cartoon_image(self, image):
        """
        展示卡通画效果

        """
        self.cartoon_result_lab.setPixmap(QtGui.QPixmap(image))
        self.cartoon_result_lab.setHidden(False)

        self.enable_create_cartoon_btn(False)
        self.enable_save_btn(True)
        self.camera.enable_cancel_btn(True)

    def show_camera(self, image):
        """
        展示摄像头数据

        """
        self.camera.bg_pixmap = image
        self.camera.update()

    def set_save_result_view(self, original_photo=None, cartoon_photo=None):
        """
        保存的时候展示结果页面

        """
        self.save_window.set_cartoon_result(original_photo, cartoon_photo)

    def show_loading_activing(self):
        self.loading_activing = LoadingActiving(title=self.configure.get_value_for_key("k_creating"), parent=self.show_result_widget)
        self.loading_activing.show()

    def dismiss_loaing_activing(self):
        self.loading_activing.close()

    def picture_status_action(self, capture):
        """
        拍照状态

        """
        if capture:
            self.enable_take_picture_btn(False)
            self.camera.capture_mode(True)
            self.enable_create_cartoon_btn(True)
            self.enable_save_btn(False)
        else:
            self.enable_take_picture_btn(True)
            self.camera.capture_mode(False)
            self.enable_create_cartoon_btn(False)
            self.enable_save_btn(False)
            self.cartoon_result_lab.setHidden(True)

    def configureFont(self):
        """
        配置字体

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

        capture_tip_font = QFont("Source Han Sans CN")
        capture_tip_font.setWeight(QFont.Normal)
        capture_tip_font.setPixelSize(14)

        self.capture_tip_lab.setFont(capture_tip_font)
        self.capture_tip_lab.setStyleSheet("QLabel#capture_tip_lab{color:#FFFFFF;}")

        result_tip_font = QFont("Source Han Sans CN")
        result_tip_font.setWeight(QFont.Normal)
        result_tip_font.setPixelSize(14)

        self.result_tip_label.setFont(result_tip_font)
        self.result_tip_label.setStyleSheet("QLabel#result_tip_label{color:#FFFFFF;}")

        add_btn_font = QFont("Source Han Sans CN")
        add_btn_font.setWeight(QFont.Normal)
        add_btn_font.setPixelSize(16)
        self.make_cartoon_btn.setFont(add_btn_font)
        self.make_cartoon_btn.setIcon(QtGui.QIcon(":/resources/ic_create_small.png"))
        self.make_cartoon_btn.setStyleSheet("QPushButton{background-color:#9189FE;border-radius:8px;color:#ffffff;}")

        save_btn_font = QFont("Source Han Sans CN")
        save_btn_font.setWeight(QFont.Normal)
        save_btn_font.setPixelSize(16)
        self.save_photo_btn.setFont(save_btn_font)
        self.save_photo_btn.setIcon(QtGui.QIcon(":/resources/ic_save_small.png"))
        self.save_photo_btn.setStyleSheet("QPushButton{background-color:#9189FE;border-radius:8px;color:#ffffff;}")


    def enable_take_picture_btn(self, enable):
        if not enable:
            self.take_picture_btn.setEnabled(False)
            self.take_picture_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_camera_disable.png)}")
        else:
            self.take_picture_btn.setEnabled(True)
            self.take_picture_btn.setStyleSheet("QPushButton{border-image: url(:/resources/ic_camera.png)}")

    def enable_create_cartoon_btn(self, enable):
        if not enable:
            self.make_cartoon_btn.setEnabled(False)
            op = QtWidgets.QGraphicsOpacityEffect()
            op.setOpacity(0.3)
            self.make_cartoon_btn.setGraphicsEffect(op)
            self.make_cartoon_btn.setAutoFillBackground(False)
            self.make_cartoon_btn.setStyleSheet("QPushButton{background-color:#9189FE;border-radius:8px;color:#ffffff;}")

        else:
            self.make_cartoon_btn.setEnabled(True)
            op = QtWidgets.QGraphicsOpacityEffect()
            op.setOpacity(1.0)
            self.make_cartoon_btn.setGraphicsEffect(op)
            self.make_cartoon_btn.setAutoFillBackground(False)
            self.make_cartoon_btn.setStyleSheet("QPushButton{background-color:#9189FE;border-radius:8px;color:#ffffff;}")

    def enable_save_btn(self, enable):
        if not enable:
            self.save_photo_btn.setEnabled(False)
            op = QtWidgets.QGraphicsOpacityEffect()
            op.setOpacity(0.3)
            self.save_photo_btn.setGraphicsEffect(op)
            self.save_photo_btn.setAutoFillBackground(False)
            self.save_photo_btn.setStyleSheet("QPushButton{background-color:#9189FE;border-radius:8px;color:#ffffff;}")
        else:
            self.save_photo_btn.setEnabled(True)
            op = QtWidgets.QGraphicsOpacityEffect()
            op.setOpacity(1.0)
            self.save_photo_btn.setGraphicsEffect(op)
            self.save_photo_btn.setAutoFillBackground(False)
            self.save_photo_btn.setStyleSheet("QPushButton{background-color:#9189FE;border-radius:8px;color:#ffffff;}")

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.drawPixmap(0, 0, 1920, 1080, QPixmap(":/resources/backgroud.png"))
        painter.end()
