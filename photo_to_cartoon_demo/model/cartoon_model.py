from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap

from common.utility.common_utility import CommonUtil

from common.base.model import Model
from PyQt5.QtCore import pyqtSignal as Signal

class CartoonModel(QtCore.QThread, Model):
    camera_stream = Signal(object)
    camera_error = Signal(bool)

    def __init__(self):
        super(CartoonModel, self).__init__()
        self.cartoon_solver = None

    def release(self):
        """
        释放模型

        """
        if self.cartoon_solver is not None:
            self.cartoon_solver.release()

    def make_cartoon_picture(self, image):
        """
        生成卡通图片

        :param image:推理的图片

        :return: array
        """
        if self.cartoon_solver is None:
            from oneai.photo2cartoon_solver import Image2CartoonSolver
            self.cartoon_solver = Image2CartoonSolver()
            self.cartoon_solver.load()

        result = self.cartoon_solver.image2cartoon(image)

        return result

    def convert_cv2_to_qpixmap(self, cv2_image, swapp=True):
        """

        :param swapp:
        :param cv2_image:
        :return: QPixmap
        """
        height, width, channel = cv2_image.shape
        bytes_per_line = 3 * width
        image = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        if swapp:
            image = image.rgbSwapped()
        pixmap = QPixmap.fromImage(image)

        return pixmap

    def _init_camera(self):
        """
        初始化摄像头

        """
        self.cam = CommonUtil.get_camera()
        if not self.cam.isOpened():
            return False

        return True

    def get_frame(self):
        """
        从摄像头读取一帧并返回

        :return: 读取成功返回一帧，失败返回None
        """
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                return frame

        return None

    def run(self):
        """
        获取摄像头数据

        :return:
        """
        if not self._init_camera():
            self.camera_error.emit(True)
            return

        self.camera_error.emit(False)
        while True:
            frame = self.get_frame()
            if frame is None:
                self.camera_error.emit(True)
                break

            self.camera_stream.emit(frame)
