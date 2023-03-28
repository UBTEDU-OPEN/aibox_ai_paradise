import cv2
import os
import sys
import threading
from enum import Enum

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from common.utility.configure_string_single import ConfigureStringSingle

from common.ui.commonDialog.BaseDialog import BaseDialogView

from photo_to_cartoon_demo.model.cartoon_model import CartoonModel
from photo_to_cartoon_demo.view.cartoon_fail_dialog import CartoonFailDialog

sys.path.append('..')
from common.base.presenter import Presenter

from PyQt5.QtCore import pyqtSignal as Signal

class CartoonPresenter(Presenter):
    class _Status(Enum):
        DEFAULE = 1
        CAPTURE = 2
        MAKING_CARTOON = 3
        CARTOON = 4

    cartoon_fail_signal = Signal()

    def __init__(self, view, configure_string_object=None):
        super(CartoonPresenter, self).__init__(view)
        self.local_configure = configure_string_object
        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()
        # 绑定view面的信号槽
        self.view.close_window_clicked.connect(self.close_window_action)
        self.view.capture_btn_clicked.connect(self.capture_action)
        self.view.make_cartoon_btn_clicked.connect(self.make_cartoon_action)
        self.view.save_btn_clicked.connect(self.save_action)
        self.view.cancel_capture_clicked.connect(self.cancel_capture_action)

        self.cartoon_fail_signal.connect(self.show_no_face_view)

        self.status = self._Status.DEFAULE

        self.last_image = None

        self.create_model()

    def create_model(self):
        """
        创建model, 绑定信号槽

        """
        self._model = CartoonModel()

        self._model.camera_stream.connect(self.camera_result)
        self._model.camera_error.connect(self.on_camera_error)
        # 延迟1妙加载，防止loading界面过快消失
        QTimer.singleShot(1000, self.model.start)

    def close_window_action(self):
        """
        关闭窗口

        """
        self.dialog = BaseDialogView(parent=self.view, sure_button_action=self.close_sure_dialog)
        self.dialog.show()

    def close_sure_dialog(self):
        """
        退出程序关闭窗口

        """
        self.dialog.close()

        self.close()

    def close(self):
        """
        关闭，释放资源

        """
        self.view.close()
        self._model.release()

    def capture_action(self):
        """
        拍照

        """
        self.status = self._Status.CAPTURE
        self.view.picture_status_action(True)

    def make_cartoon_action(self):
        """
        生成卡通照片

        """
        self.view.click_make_cartoon()

        self.view.show_loading_activing()

        make_cartoon_thread = threading.Thread(target=self.async_create_cartoon)
        make_cartoon_thread.start()

    def async_create_cartoon(self):
        """
        异步生成卡通图片

        """
        result = self.model.make_cartoon_picture(self.last_image)

        self.view.dismiss_loaing_activing()
        if result == "":
            self.cartoon_fail_signal.emit()
        else:
            result = cv2.resize(result, (450, 450))

            pixmap_image = self.model.convert_cv2_to_qpixmap(result)

            self.view.show_cartoon_image(pixmap_image)

            self.cartoon_image = pixmap_image
            self.status = self._Status.CARTOON

    def save_action(self):
        """
        保存卡通照片

        """
        self.save_cartoon()

    def cancel_capture_action(self):
        """
        取消拍照,弱国当前有生成的卡通画，需要提示用户是否需要保存

        """
        if self.status == self._Status.CARTOON:
            self.cancel_capture_dialog = BaseDialogView(parent=self.view,
                                                        title=self.local_configure.get_value_for_key("k_check_save"),
                                                        ok_txt=self.local_configure.get_value_for_key("k_save_btn"),
                                                        cancel_txt=self.local_configure.get_value_for_key("k_give_up_btn"),
                                                        sure_button_action=self.save_cartoon,
                                                        cancel_btn_action=self.give_up_save)
            self.cancel_capture_dialog.show()
        else:
            self.give_up_save()

    def give_up_save(self):
        """
        放弃保存的是哦胡需要重置状态

        """
        self.reset_status()

    def reset_status(self):
        """
        重置状态

        """
        self.status = self._Status.DEFAULE
        self.view.picture_status_action(False)

    def save_cartoon(self):
        """
        保存卡通画，保存后重置拍照状态

        """
        pixmap_image = self.model.convert_cv2_to_qpixmap(self.last_image, swapp=True)
        self.view.set_save_result_view(pixmap_image, self.cartoon_image)

        self.save(save_view=self.view.save_window)

        self.reset_status()

    def save(self, filepath='/home/oneai/cartoon', save_view=None):
        """
        保存，如果存在就保存为副本，如果副本存在，就一直按照最大数字累加（《人像卡通化-副本》，《人像卡通化-副本1》，《人像卡通化-副本2》）

        """
        title = self.common_cfg.get_value_for_key("ubt_cartoon_title")
        file_name = f'{title}.jpg'

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        target_file = self.get_file_name(filepath, file_name)

        file, suffix = QFileDialog.getSaveFileName(save_view,
                                                   self.common_cfg.get_value_for_key('ubt_style_file_save'),
                                                   target_file[:-4],
                                                   '.jpg;;.png')
        result = file + suffix
        if not len(result) == 0:
            save_view.grab().save(result)

    def get_file_name(self, file_path, file_name):
        """
        生成对应的文件名

        """
        str_copy = self.common_cfg.get_value_for_key('ubt_style_copy')
        f = os.path.join(file_path, file_name)
        num = -1
        try:
            if os.path.exists(f):
                files = os.listdir(file_path)
                for sf in files:
                    if file_name[:-4] in sf:
                        left = sf[:-4].replace(file_name[:-4], "")
                        if left == "":
                            if num == -1:
                                num = 0
                        else:
                            tmp = int(left[len(str_copy) + 1:])
                            if tmp > num:
                                num = tmp
        except Exception:
            pass
        finally:
            if num == -1:
                return f
            else:
                str_list = list(f)
                content = f'-{str_copy}{str(num + 1)}'
                str_list.insert(-4, content)
                return "".join(str_list)

    def on_camera_error(self, open_error):
        """
        摄像头读取出错处理

        :param open_error:如果为True 表示开启摄像头错误,弹出异常对话框，如果为False 表示正常开启摄像头
        """
        if not open_error:
            self.view.close_loading()
        else:
            self.show_reload_dialog()
            self.view.close_loading()

    def show_reload_dialog(self):
        """
        显示重新加载对话框

        """
        reload_dialog = BaseDialogView(self.common_cfg.get_value_for_key("ubt_load_error"),
                                       self.common_cfg.get_value_for_key("ubt_reload"),
                                       self.common_cfg.get_value_for_key("ubt_quit"),
                                       parent=self.view,
                                       sure_button_action=lambda: (reload_dialog.close(), self._reload()),
                                       cancel_btn_action=self.close)
        reload_dialog.show()

    def _reload(self):
        """
        尝试重新加载模型

        """
        del self._model
        self.create_model()
        self.view.show_loading()

    def show_no_face_view(self):
        no_face_view = CartoonFailDialog(title=self.local_configure.get_value_for_key("k_no_face_tip"),
                                         other_title=self.local_configure.get_value_for_key("k_capture_again"),
                                         parent=self.view,
                                         other_btn_action=self.capture_again,
                                         cancel_btn_action=self.capture_again)

        no_face_view.show()

    def capture_again(self):
        """
        如果卡通化失败，重新拍摄

        """
        self.reset_status()


    def camera_result(self, image):
        """
        展示摄像头数据

        ;param image:摄像头数据
        """
        if self._Status.DEFAULE == self.status:
            pixmap_image = self.model.convert_cv2_to_qpixmap(image, swapp=True)
            self.view.show_camera(pixmap_image)

            self.last_image = image

