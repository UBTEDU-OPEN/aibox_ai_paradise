# -*-coding:utf-8 -*-
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import cv2

from common.utility.configure_string_single import ConfigureStringSingle

from face_recognize_demo.com import ubt_device
from face_recognize_demo.com.fr_manager import record
from face_recognize_demo.model.facerecognition_model import FaceRecognitionModel, DEFAULT_THRESHOLD
from face_recognize_demo.view.capture_dialog_view import CaptureDialogView
from face_recognize_demo.view.failure_dialog_view import FailureDialogView
from face_recognize_demo.view.name_input_dialog_view import NameInputDialogView

sys.path.append('..')
from common.base.presenter import Presenter
from common.utility.UBTQToastTools import UBTQToastTools
from common.ui.commonDialog.BaseDialog import BaseDialogView

from enum import Enum


class MainwindowPresenter(Presenter):
    class _Status(Enum):
        DETECT = 1
        CAPTURE_NOT_VALID = 2
        CAPTURE_VALID = 3
        CAPTURE_NO_FACE = 4
        INPUT_NAME = 5

    def __init__(self, view, option, con):
        super(MainwindowPresenter, self).__init__(view)

        self.configure_str = con
        self.common_configure = ConfigureStringSingle.get_common_string_cfg()

        # handle signals
        self.view.add_sample_clicked.connect(self.on_add_sameple_clicked)
        self.view.close_button_clicked.connect(self.on_close_button_clicked)
        self.view.delete_sample_item_clicked.connect(self.on_delete_sample)
        self.view.delete_all_sample_clicked.connect(self.on_delete_all_samples)
        self.view.threshold_changed.connect(self.on_threshold_changed)
        self.view.threshold_tip_clicked.connect(self.on_threshold_tip_clicked)

        self._option = option
        # 创建model
        self._create_model()

        self._status = self._Status.DETECT

        self.records_count = 0
        self.pop = None

    def on_add_sameple_clicked(self):
        """ 弹出拍照对话框， 进入拍照流程

        """
        # 判断样本数是否超出最大值
        if self.model.sample_count() >= self.model.SAMPLE_MAX_COUNT:
            UBTQToastTools.showTip(self.configure_str.get_value_for_key("k_max_add"), self.view)
            return
        self.view.enter_capture_mode()

        self.capture_dialog = CaptureDialogView(self.view,
                                                tip=self.configure_str.get_value_for_key("k_photograph_tip"),
                                                cancel_title=self.configure_str.get_value_for_key("k_cancel"),
                                                ok_title=self.configure_str.get_value_for_key("k_photograph"))

        self.capture_dialog.setGeometry(919 * ubt_device.scale_width, 380 * ubt_device.scale_height,
                                        self.capture_dialog.width() * ubt_device.scale_width, self.capture_dialog.height() * ubt_device.scale_height)

        # # connect signals
        self.capture_dialog.cancelled.connect(self.on_capture_dialog_cancelled)
        self.capture_dialog.captured.connect(self.on_capture_dialog_confirmed)
        self.capture_dialog.show()
        self._status = self._Status.CAPTURE_NO_FACE

        self.view.show_recognition_mask(False)

        self.model.add_sample_status = True

    def on_delete_sample(self, name):
        """

        :param name:
        """
        self.model.delete_sample(name)
        self.view.delete_sample_item(name)

        self._check_sample_count()

    def on_delete_all_samples(self):
        """ 清空按钮事件处理， 弹框确认

        """
        self.delete_confirm_dialog = BaseDialogView(self.configure_str.get_value_for_key("k_clear_tip"),
                                                    self.configure_str.get_value_for_key("k_clear_all"),
                                                    self.configure_str.get_value_for_key("k_cancel"),
                                               parent=self.view,
                                               sure_button_action=self.on_delete_all_confirmed
                                               )
        self.delete_confirm_dialog.show()

    def on_delete_all_confirmed(self):
        """ 清空样本

        """
        self.model.delete_all()
        self.view.delete_all_samples()
        UBTQToastTools.showTip(self.configure_str.get_value_for_key("k_clear_smaple_success"), self.view)
        self._check_sample_count()

    def on_capture_dialog_cancelled(self):
        """ 拍照对话框取消， 返回识别模式

        """
        # self.model.add_sample_status = False
        self.capture_dialog.close()
        self.view.quit_capture_mode()
        self._status = self._Status.DETECT
        self.view.show_recognition_mask(True)

    def on_capture_dialog_confirmed(self):
        """ 拍照按钮处理函数

        """
        # 样本已存在时, 立即提示用户
        if self._Status.CAPTURE_NOT_VALID == self._status:
            UBTQToastTools.showTip(self.configure_str.get_value_for_key('k_input_same_photo'), self.capture_dialog)
            return
        elif self._Status.CAPTURE_NO_FACE == self._status:
            UBTQToastTools.showTip(self.configure_str.get_value_for_key('k_no_face'), self.capture_dialog)
            return

        self._show_input_dialog()
        self.view.quit_capture_mode()
        self._status = self._Status.INPUT_NAME

    def on_input_dialog_confirmed(self, name):
        """

        :return:
        """
        if "" == name:
            return

        # 名字已存在
        if self.model.search_sample(name):
            UBTQToastTools.showTip(self.configure_str.get_value_for_key('k_input_name_repeat'), self.input_dialog)
            return

        # add sample
        frame = cv2.cvtColor(self.saved_frame, cv2.COLOR_RGB2BGR)
        ret = self.model.add_sample(frame, name)

        self.input_dialog.close()
        self.on_capture_dialog_cancelled()

        # self.model.add_sample_status = False

        # 切换回识别模式
        self._status = self._Status.DETECT

        if ret:
            # update sample list
            image = self.model.convert_cv2_to_qpixmap(frame, True)
            self.view.add_sample_item(image, name)
            UBTQToastTools.showTip(self.configure_str.get_value_for_key('k_add_success'), self.view)
        else:
            # 录入失败
            failure_dialog = FailureDialogView(self.view,
                                               title=self.configure_str.get_value_for_key("k_input_failer"),
                                               btn_title=self.configure_str.get_value_for_key("k_ok"))
            failure_dialog.show()



    def on_input_dialog_cancelled(self):
        """ 名字输入对话框取消按钮点击

        """
        self.capture_dialog.close()
        self.on_add_sameple_clicked()

    def on_detect_finished(self, result):
        """

        :param result:
        :return:
        """
        image = None
        records = []
        faces = result.result_data

        if self._Status.DETECT == self._status:
            image, records = self.model.make_image(result)
            # 添加样本状态由最后识别结束后转换为不添加样本状态
            self.model.add_sample_status = False
        elif self._Status.CAPTURE_NOT_VALID == self._status:
            if len(faces) == 0:
                self._status = self._Status.CAPTURE_NO_FACE
            elif faces[0][5] == 0:
                # 未注册人脸相似度为0
                self._status = self._Status.CAPTURE_VALID
            self.view.set_capture_not_valid()
            image = self.model.convert_cv2_to_qpixmap(result.image, swapp=False)
        elif self._Status.CAPTURE_VALID == self._status:
            if len(faces) == 0:
                self._status = self._Status.CAPTURE_NO_FACE
            elif faces[0][5] != 0 and faces[0][5] <= (1 - DEFAULT_THRESHOLD):
                self._status = self._Status.CAPTURE_NOT_VALID
            self.view.set_capture_valid()
            self.saved_frame = result.image
            image = self.model.convert_cv2_to_qpixmap(result.image, swapp=False)
        elif self._Status.CAPTURE_NO_FACE == self._status:
            if len(faces) > 0 and faces[0][5] == 0:
                self._status = self._Status.CAPTURE_VALID
            elif len(faces) > 0 and faces[0][5] != 0 and faces[0][5] <= (1 - DEFAULT_THRESHOLD):
                self._status = self._Status.CAPTURE_NOT_VALID
            self.view.set_capture_no_face()
            image = self.model.convert_cv2_to_qpixmap(result.image, swapp=False)

        if image is not None:
            self.view.showRecognitionResult(image)

    def on_threshold_tip_clicked(self):
        pass
        # PopWindow.show_pop(self)
        # if self.pop is not None:
        #     print("zhanshi")
        #     self.pop.show_pop()
        # else:
        #     self.pop = PopWindow(self.view.pushButton)
        #     print("zzzzz")

    def close_sure_dialog(self):
        self.dialog.close()
        self._close()

    def on_close_button_clicked(self):
        """
        :return:
        """
        self.dialog = BaseDialogView(parent=self.view,sure_button_action=self.close_sure_dialog)
        self.dialog.show()

    def on_get_record_smaple(self, records=None):
        """
        :param records:
        :return:
        """
        if records is not None:
            for record in records:
                name = record.name
                smaple = self.model.get_sample_image_by_name(name)
                record.smaple = smaple

            self.on_update_records(records)

    def on_update_records(self, records):
        """
        :param records:
        :return:
        """
        if self.records_count != len(records):
            self.records_count = len(records)

            first_record = records[0]
            # tem_r = copy.deepcopy(first_record)

            temp_record = record()
            temp_record.reccordImg = first_record.reccordImg
            temp_record.name = first_record.name
            temp_record.record_time = first_record.record_time
            temp_record.confirence = first_record.confirence
            temp_record.smaple = first_record.smaple

            self.view.showRecord(temp_record)

    def on_add_samples_from_model(self, samples):
        for (img, name) in samples:
            self.view.add_sample_item(img, name)

    def on_add_sample_from_model(self, pixmap, name):
        """ 处理model初始化时发起的添加样本事件

        :param pixmap: (QPixmap) 图片数据
        :param name: (str) 样本名
        """
        self.view.add_sample_item(pixmap, name)

    def on_threshold_changed(self, value):
        threshold = value / 100.0
        self.model.threshold = threshold

    def on_model_loaded(self, success):
        """ 关闭view加载界面

        """
        self.model.load_finished.disconnect(self.on_model_loaded)
        if not success:
            self.view.close_loading()
            self._show_reload_dialog()
        else:
            QTimer.singleShot(1000, self.view.close_loading)

    def _show_input_dialog(self):
        """ 显示姓名输入框

        """
        self.input_dialog = NameInputDialogView(self.view,
                                                placeholder_text=self.configure_str.get_value_for_key('k_input_name_tip'),
                                                cancel_title=self.configure_str.get_value_for_key('k_cancel'),
                                                ok_title=self.configure_str.get_value_for_key('k_enter'))
        self.input_dialog.setGeometry(919 * ubt_device.scale_width, 380 * ubt_device.scale_height,
                                      self.input_dialog.width() * ubt_device.scale_width, self.input_dialog.height() * ubt_device.scale_height)

        # capture_dialog_rect = self.capture_dialog.geometry()
        # self.input_dialog.setGeometry(capture_dialog_rect)
        # connect signals
        self.input_dialog.input_confirmed.connect(self.on_input_dialog_confirmed)
        self.input_dialog.cancel_clicked.connect(self.on_input_dialog_cancelled)
        self.input_dialog.show()

        self.input_dialog.become_first_focus()

    def _check_sample_count(self):
        """ 检查样本数, 切换控件显示

        """
        # 是否要切换列表控件状态
        if self.view.get_sample_list_count() < 2:
            self.view.set_list_status_for_empty()

    def _reload(self):
        """ 尝试重新加载模型

        """
        del self._model
        self._create_model()
        self.view.show_loading()
        self._reset()

    def _close(self):
        """ 释放模型，退出

        """
        self.model.stop_detecting()
        # del self.model
        self.view.close()

    def _on_camera_error(self):
        """ 摄像头读取出错处理

        """
        self.model.camera_error.disconnect(self._on_camera_error)
        self._close_all_popup()
        self._show_reload_dialog()

    def _show_reload_dialog(self):
        """ 显示重新加载对话框

        """
        reload_dialog = BaseDialogView(self.common_configure.get_value_for_key('ubt_load_error'),
                                       self.common_configure.get_value_for_key('ubt_reload'),
                                       self.common_configure.get_value_for_key('ubt_quit'),
                                       parent=self.view,
                                       sure_button_action=lambda: (reload_dialog.close(), self._reload()),
                                       cancel_btn_action=self._close)
        reload_dialog.show()

    def _create_model(self):
        """ 创建model, 绑定信号槽

        """
        self._model = FaceRecognitionModel(self._option)
        self._model.load_sample.connect(self.on_add_sample_from_model)
        self._model.load_samples_signal.connect(self.on_add_samples_from_model)
        self._model.detect_finished.connect(self.on_detect_finished)
        self._model.load_finished.connect(self.on_model_loaded)
        self._model.record_result_signal.connect(self.on_get_record_smaple)
        self._model.camera_error.connect(self._on_camera_error)
        # 延迟1妙加载，防止loading界面过快消失
        QTimer.singleShot(1000, self.model.start)
        # self._model.start()

    def _reset(self):
        """ 重置ui

        """
        self.view.delete_all_samples()
        self._status = self._Status.DETECT
        self.view.quit_capture_mode()
        self.records_count = 0

    def _close_all_popup(self):
        """ 关闭所有弹出窗口

        """
        child = QApplication.activeModalWidget()
        while child:
            child.close()
            child = QApplication.activeModalWidget()

        child = QApplication.activePopupWidget()
        while child:
            child.close()
            child = QApplication.activePopupWidget()

        try:
            self.delete_confirm_dialog.close()
        except Exception:
            pass

        try:
            self.dialog.close()
        except Exception:
            pass

