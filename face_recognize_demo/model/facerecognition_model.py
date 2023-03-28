# -*-coding:utf-8 -*-
import sys
import os

from common.utility.common_utility import CommonUtil


from face_recognize_demo.com.fr_manager import FaceRecognitionManager

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.base.model import Model

import cv2
import time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal as Signal
import glob
from pathlib import Path

DEFAULT_THRESHOLD = 0.75
_FACE_RECOG_SAMPLE_DIR = "face_recognition"
_TRACK_RECOG_SAMPLE_DIR = "track_recognition"

class FaceRecognitionModel(QtCore.QThread, Model):

    detect_finished = Signal(object)
    load_sample = Signal(QPixmap, str)
    load_finished = Signal(bool)
    record_result_signal = Signal(list)

    load_samples_signal = QtCore.pyqtSignal(list)

    camera_error = Signal()


    SAMPLE_MAX_COUNT = 100

    def __init__(self, option, threshold=DEFAULT_THRESHOLD):
        super(FaceRecognitionModel, self).__init__()

        self.add_sample_status = False

        self.ai_solver = None

        self.threshold = threshold
        self._running_flag = True
        self.image_handler = FaceRecognitionManager()
        self.image_handler.record_list_signal.connect(self.record_result_signal)
        self.mutex = QtCore.QMutex()
        self._sample_count = 0
        self.sample_list = []
        # 创建样本目录
        dir_name = _FACE_RECOG_SAMPLE_DIR
        if "track" in option:
            dir_name = _TRACK_RECOG_SAMPLE_DIR
        home = str(Path.home())
        self.sample_path = os.path.join(home, ".cache", dir_name, "samples")
        if not os.path.exists(self.sample_path):
            Path(self.sample_path).mkdir(parents=True, exist_ok=True)

    def __del__(self):
        self._close_camera()

    def _init_camera(self):
        """ 初始化摄像头

        """
        self.cam = CommonUtil.get_camera()
        if not self.cam.isOpened():
            return False

        return True

    def get_frame(self):
        """ 从摄像头读取一帧并返回

        :return: 读取成功返回一帧，失败返回None
        """
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                return frame

        return None

    def _close_camera(self):
        """ 关闭摄像头

        """
        if self.cam.isOpened():
            self.cam.release()

    def add_sample(self, image, name):
        """ 添加样本

        :param image: (np.ndarray) 图片数据
        :param name: (string) 样本名
        :return: 成功返回True, 失败False
        """
        locker = QtCore.QMutexLocker(self.mutex)
        ret = self.ai_solver.add_sample(image, name)
        if ret:
            file_path = os.path.join(self.sample_path, name + ".jpg")
            cv2.imwrite(file_path, image)
            self._sample_count += 1

        return ret

    def delete_sample(self, name):
        """ 按样本名删除样本

        :param name: (string) 样本名
        """
        locker = QtCore.QMutexLocker(self.mutex)
        self.ai_solver.delete_sample(name)
        file_path = os.path.join(self.sample_path, name + ".jpg")
        os.remove(file_path)
        self._sample_count -= 1

    def delete_all(self):
        """ 删除所有样本

        """
        locker = QtCore.QMutexLocker(self.mutex)
        self.ai_solver.delete_all()

        # 删除图片文件
        files = glob.glob(self.sample_path + "/*.jpg")
        for f in files:
            os.remove(f)

        self._sample_count = 0

    def get_sample_image_by_name(self, name):
        """ 获取样本图片QPixmap数据

        :param name: (string) 样本名
        :return: QPixmap数据, 失败时返回None
        """
        file_name = os.path.join(self.sample_path, name + ".jpg")
        pixmap = None
        if os.path.exists(file_name):
            pixmap = QtGui.QPixmap(file_name)

        return pixmap

    def search_sample(self, name):
        """ 查找样本是否存在

        :param name: (string) 样本名
        :return: 存在返回True, 失败False
        """
        locker = QtCore.QMutexLocker(self.mutex)
        ret = self.ai_solver.search(name)
        return ret

    def detect_face(self, image):
        """ 识别人脸

        :param image: (np.ndarray) 图片数据
        :return: 识别结果列表
        """
        locker = QtCore.QMutexLocker(self.mutex)
        temp_threshold = (1 - self.threshold) if not self.add_sample_status else (1 - DEFAULT_THRESHOLD)

        arg = {'threshold': temp_threshold}
        result = self.ai_solver.detect_face(image, **arg)
        return result

    def stop_detecting(self):
        """

        :return:
        """
        self._running_flag = False
        self._close_camera()
        if self.ai_solver is not None:
            self.ai_solver.unload()
            del self.ai_solver
            self.ai_solver = None

    def run(self):
        """

        :return:
        """
        from oneai.FaceRecognizeSolver import FaceRecognizeSolver, FaceRecognizeDetectResult

        self._running_flag = True

        if not self._init_camera():
            self.load_finished.emit(False)
            return

        self.ai_solver = FaceRecognizeSolver()
        self.ai_solver.load()
        self.load_samples()

        frame = self.get_frame()
        _ = self.detect_face(frame)
        self.load_finished.emit(True)

        while self._running_flag:
            frame = self.get_frame()
            if frame is None:
                self.stop_detecting()
                self.camera_error.emit()
                break

            result = self.detect_face(frame)
            self.detect_finished.emit(result)

    def make_image(self, result):
        """

        :param result:
        :return:
        """
        image, records = self.image_handler.get_visual_image_maker(result, self.threshold)

        height, width, channel = image.shape
        bytes_per_line = 3 * width
        img = QImage(image.data, width, height, bytes_per_line,QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(img)

        return pixmap, records

    def convert_cv2_to_qpixmap(self, cv2_image, swapp=True):
        """

        :param swapp:
        :param cv2_image:
        :return:
        """
        height, width, channel = cv2_image.shape
        bytes_per_line = 3 * width
        image = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        if swapp:
            image = image.rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def load_samples(self):
        """ 加载以保存的样本

        """
        files = glob.glob(self.sample_path + "/*.jpg")
        for file in files:
            # 样本名
            basename = os.path.basename(file)
            name = os.path.splitext(basename)[0]

            cv2_img = cv2.imread(file)
            ret = cv2_img is not None
            if ret and self._sample_count < self.SAMPLE_MAX_COUNT:
                ret = self.ai_solver.add_sample(cv2_img, name)
                if ret:
                    pix = self.convert_cv2_to_qpixmap(cv2_img, swapp=True)
                    # self.load_sample.emit(pix, name)
                    self.sample_list.append((pix, name))
                    self._sample_count += 1

            if not ret:
                os.remove(file)

        self.load_samples_signal.emit(self.sample_list)

    def sample_count(self):
        """ 获取样本数

        :return:  样本数目
        """
        return self._sample_count

