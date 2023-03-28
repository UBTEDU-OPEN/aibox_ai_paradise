import cv2, numpy, os, sys
import threading
import time

from PIL import Image, ImageDraw, ImageFont

from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal as Signal
from common.utility.configure_string_single import ConfigureStringSingle

from common.utility.common_utility import CommonUtil
import copy
import pickle
from face_recognize_demo.com.demo_type import DemoType, Type


class record:
     def __init__(self, img=None, name=None, record_time=None, confirence=None):
         self.reccordImg = img
         self.name = name
         self.record_time = record_time
         self.confirence = confirence
         self.smaple = None

class FaceRecognitionManager(QtCore.QObject):
    record_list_signal = QtCore.pyqtSignal(list)

    def __init__(self ,recognitionResult=None, record_result=None):
        super(FaceRecognitionManager,self).__init__()

        self.configure = ConfigureStringSingle.get_common_string_cfg()

        self.UNKNOWN_FACE = 'unknown'

        self.record_list = []
        self.recognitionResult = recognitionResult
        self.record_result = record_result
        self.previous_faces = []
        self.demo = DemoType()

    def recognition(self):
        '''测试模拟'''
        time.sleep(1)
        self.cap = CommonUtil.get_camera()
        while True:
            ret, frame = self.cap.read()
            if ret:
                result = self.solver.detect_face(frame)
                image = self.get_visual_image_maker(result)

                height, width, channel = image.shape
                bytesPerline = 3 * width
                img = QImage(image.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
                image = QPixmap.fromImage(img)
                # self.recognitionResult(image)

                # self.obj_connection.ubtresultsignal.emit(image)

                # del img

    def add_record(self, img, name, confirence):
        add = True

        for object in self.record_list:
            if object.name == name:
                val = time.time() - object.record_time

                if val <= 3:
                    add = False

        if add:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            height, width, channel = img.shape
            bytesPerline = 3 * width
            image = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
            self.record_list.insert(0,record(image, name, time.time(), confirence))

            self.record_list_signal.emit(self.record_list)



    def get_visual_image_maker(self, result=None, threshold=0.75):
        a_result = result.result_data

        # 画面中识别到的人脸不变时， 不更新打卡记录
        should_update = False
        current_known_faces = [data[0] for data in a_result if data[0] != self.UNKNOWN_FACE]
        current_known_faces.sort()
        if current_known_faces != self.previous_faces:
            self.previous_faces = current_known_faces
            should_update = True

        for i in a_result:
            pil_image = Image.fromarray(result.image)
            draw = ImageDraw.Draw(pil_image)
            data = i
            name = data[0]
            top = int(data[2] / result.narrow_rate)
            right = int(data[3] / result.narrow_rate)
            bottom = int(data[4] / result.narrow_rate)
            left = int(data[1] / result.narrow_rate)
            temp_confi = 1 - data[5]

            confirence = int(round(temp_confi,2) * 100)

            name = self.UNKNOWN_FACE if confirence < (threshold * 100) else name
           
            confirence_str = str(confirence) + '%'

            color = (255, 149, 132) if name == self.UNKNOWN_FACE else (161, 212, 145)

            fontStyle = ImageFont.truetype(
                os.path.dirname(os.path.realpath(__file__)) + '/resource/SourceHanSansCN-Bold.otf', 21,
                encoding="utf-8")

            if name != self.UNKNOWN_FACE:

                '''图解作为打卡记录'''
                temp_img = result.image.copy()
                crop_img = temp_img[top:bottom, left:right]
                # self.add_record(crop_img, name, confirence_str)
                # 打卡记录使用子线程处理，以免影响视频的绘制，后续用队列管理，无需多次创建子线程
                if should_update:
                    thread = threading.Thread(target=self.add_record, args=(crop_img,name, confirence_str), daemon=True)
                    thread.start()

                draw.text((right - 10 - 30 - 10, bottom - 26), confirence_str, color, font=fontStyle)
                draw.text((left + 10, top - 26), name, color, font=fontStyle)

                desc_image = numpy.asarray(pil_image)

                self.rounded_rectangle(desc_image, (left, top), (right, bottom), 10, color, outline=2)

                result.image = desc_image
            else:
                if self.demo.type_item == Type.face_demo_item:
                    draw.text((left + 10, top - 26), self.configure.get_value_for_key('ubt_unknown') , color, font=fontStyle)

                    desc_image = numpy.asarray(pil_image)
                    self.rounded_rectangle(desc_image, (left, top), (right, bottom), 10, color, outline=2)

                    result.image = desc_image

        result.image = cv2.cvtColor(result.image, cv2.COLOR_RGB2BGR)
        #
        # del draw

        return result.image, []

    def rounded_rectangle(self, img, pt1, pt2, corner_radius, fill=None, outline=None):
        upper_left_point = pt1  # (upper_left_point[0], upper_left_point[1])
        bottom_right_point = pt2  # (bottom_right_point[0],bottom_right_point[1])

        center_x = int((pt2[0] + pt1[0]) * 0.5)
        center_y = int((pt2[1] + pt1[1]) * 0.5)

        center_point = (center_x, center_y)
        cv2.drawMarker(img, center_point, fill, 0, 30, 2)

        # top
        cv2.line(img, (upper_left_point[0] + corner_radius, upper_left_point[1]),
                 (bottom_right_point[0] - corner_radius, upper_left_point[1]), fill, outline)
        # cv2
        cv2.line(img, (upper_left_point[0] + corner_radius, bottom_right_point[1]),
                 (bottom_right_point[0] - corner_radius, bottom_right_point[1]), fill, outline)
        # left
        cv2.line(img, (upper_left_point[0], upper_left_point[1] + corner_radius),
                 (upper_left_point[0], bottom_right_point[1] - corner_radius), fill, outline)
        # right
        cv2.line(img, (bottom_right_point[0], upper_left_point[1] + corner_radius),
                 (bottom_right_point[0], bottom_right_point[1] - corner_radius), fill, outline)

        # corners
        cv2.ellipse(img, (upper_left_point[0] + corner_radius, upper_left_point[1] + corner_radius),
                    (corner_radius, corner_radius), 180, 0, 90, fill, outline)
        cv2.ellipse(img, (bottom_right_point[0] - corner_radius, upper_left_point[1] + corner_radius),
                    (corner_radius, corner_radius), 270, 0, 90, fill, outline)
        cv2.ellipse(img, (bottom_right_point[0] - corner_radius, bottom_right_point[1] - corner_radius),
                    (corner_radius, corner_radius), 10, 0, 90, fill, outline)
        cv2.ellipse(img, (upper_left_point[0] + corner_radius, bottom_right_point[1] - corner_radius),
                    (corner_radius, corner_radius), 90, 0, 90, fill, outline)


    def releaseCamera(self):
        self.cap.release()







