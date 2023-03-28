#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: face_mask_inference.py
# Created: 2020-05-26 09:05:20
# Author: ChenglongXiong (chenglong.xiong@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:人脸口罩检测
###
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageQt
import time, os
import cv2
import numpy
import logging
WARE_SIG = 'masked'#戴口罩
UNWARE_SIG = 'unmasked'#未戴口罩
NOTWELL_SIG = 'notwell'#戴了口罩但是未完全戴好/半口罩

class FaceMaskProp:
    """人脸口罩检测
    """
    # def __init__(self, image, result, confidence = 90, text = ('已戴口罩', '未戴口罩'), path = '.'):
    #     """类初始化
    #
    #     Args:
    #         image (array): 图片
    #         result (list): 推理结果
    #         text (tuple, optional): 图片文本信息. 默认值 ('已戴口罩', '未戴口罩').
    #         path (str, optional): 素材路径. 默认值 './'.
    #     """
    #     self.confidence = confidence
    #     self.src_img = image
    #     self.inference_data = result
    #     self.img_text = text
    #     self.ui_path = path
    #     self.ui_file = ('img_recognize_green.png', 'img_recognize_red.png')
    #     self.font = 'simsun.ttc'

    def __init__(self, confidence = 60, text = ('已戴口罩', '未戴口罩'), path = '.', common_path = '.'):
        """[summary]

        Args:
            confidence (int, optional): 置信值. Defaults to 60.
            text (tuple, optional): 图片文本信息. 默认值 ('已戴口罩', '未戴口罩').
            path (str, optional): 素材路径. 默认值 './'.
        """        
        self.confidence = confidence
        self.img_text = text
        self.ui_path = path
        self.common_path = common_path
        self.ui_file = ('img_recognize_green.png', 'img_recognize_red.png')
        self.font_regular = 'SourceHanSansCN-Regular.otf'
        self.font_bold = 'SourceHanSansCN-Bold.otf'
        self.ui_nomask_confidence = 'tab_weidaikouzhao.png'
        self.ui_nomask_time = 'img_bg_purple.png'
        self.ui_nomask_lable = 'img_weidaikouzhao.png'
        self.ui_nomask_lable1 = 'img_weidaikouzhao_zhijiao.png'
        self.nomask_size = (110, 110)
        self.least_size = (102, 120)

        self.fontStyle = ImageFont.truetype(self.common_path + '/' + self.font_bold, 12, encoding="utf-8")

        self.logo_img_green = Image.open(self.ui_path + '/' + self.ui_file[0])
        self.logo_img_red = Image.open(self.ui_path + '/' + self.ui_file[1])

    def fill_data(self, image, result):
        self.src_img = image
        self.inference_data = result

    def confidence_set(self, val):
        """设置置信值

        Args:
            val (int): 置信值
        """        
        self.confidence = val

    def pics_get(self, flag = 1):
        """获取人脸图片

        Args:
            flag (int, optional): 标志, 0 获取已戴口罩 1获取未戴口罩. 默认 1.

        Returns:
            list: 人脸,list[[img,time]]
        """
        result = []
        local_time = time.localtime(time.time())
        #轮询推理结果数据
        try:
            for item in self.inference_data:
                item_confidence = item[1] * 100
                rect = item[0]
                mask_att = item[2]
                if item_confidence >= self.confidence:
                    if mask_att != WARE_SIG:
                        # 新版ai模型识别框会返回负值
                        rect[0] = 0 if rect[0] < 0 else rect[0]
                        rect[1] = 0 if rect[1] < 0 else rect[1]
                        # 截图
                        tmp_img = self.src_img[rect[1]:(rect[3]), rect[0]:(rect[2])].copy()
                        # 时间
                        tmp_time = '{:0>2d}'.format(local_time.tm_hour) + ':' + '{:0>2d}'.format(
                            local_time.tm_min) + ':' + '{:0>2d}'.format(
                            local_time.tm_sec)  # str(local_time.tm_hour)+':'+str(local_time.tm_min)+':'+str(local_time.tm_sec)
                        # 置信度
                        tmp_confidence = str(int(item_confidence)) + '%'
                        result.append(self._draw_nomask_img(tmp_img, tmp_confidence, tmp_time))
        except Exception as e:
            error_str = '{} {}'.format(e.__class__.__name__, e)
            logging.error(error_str)

        return result

    def _draw_nomask_img(self, img, confidence, time):
        """绘制没带口罩的照片

        Args:
            img:待绘制的图片
            confidence:置信值
            time:时间
        Returns:
            array: 已画好的图片
        """   
        src_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        fontStyle_bold = ImageFont.truetype(self.common_path + '/' + self.font_bold, 15, encoding="utf-8")
        fontStyle_regular = ImageFont.truetype(self.common_path + '/' + self.font_regular, 15, encoding="utf-8")

        img_nomask = src_img.resize(self.nomask_size)
        #添加置信值
        img_confidence = Image.open(self.ui_path + '/' + self.ui_nomask_confidence)
        draw_confidence = ImageDraw.Draw(img_confidence)
        draw_confidence.text((10, 6), confidence, (255, 255, 255), font = fontStyle_bold)

        ##添加时间
        img_time = Image.open(self.ui_path + '/' + self.ui_nomask_time)
        draw_time = ImageDraw.Draw(img_time)
        draw_time.text((24, 10), time, (255, 255, 255), font = fontStyle_regular)

        dst_img = Image.open(self.ui_path + '/' + self.ui_nomask_lable)
        tmp_img = Image.open(self.ui_path + '/' + self.ui_nomask_lable1)
        dst_img.paste(img_nomask, (0, 0), tmp_img)
        dst_img.paste(img_confidence, (0, 0), img_confidence)
        dst_img.paste(img_time, (0, 110), img_time)
        return dst_img

    def make_img(self):
        """绘制图片

        Returns:
            array: 绘制好的图片
        """        
        dst_img = self.src_img
        for item in self.inference_data:
            item_confidence = item[1]*100
            mask_att = item[2]
            rect = item[0]
            if item_confidence >= self.confidence:
                dst_img = self._draw_img(dst_img, mask_att, int(item_confidence), (rect[0], rect[1], rect[2], rect[3]))
        return dst_img

    def _draw_img(self, img, mask_att, confidence, points):
        """绘制图片
 
        Args:
            img:待绘制的图片
            id:id
            confidence:置信值
            points:矩形框位置
        Returns:
            [array]: 绘制好的图片
        """
        id = 0
        logo_img = None
        if mask_att == WARE_SIG:
            id = 0
            #logo_img = self.logo_img_green
            #每次有对ui进行绘画操作，所以每次都得重新打开，避免在多次绘画，照成信息模糊
            logo_img = Image.open(self.ui_path + '/' + self.ui_file[0])
        else:
            id = 1
            #logo_img = self.logo_img_red
            #每次有对ui进行绘画操作，所以每次都得重新打开，避免在多次绘画，照成信息模糊
            logo_img = Image.open(self.ui_path + '/' + self.ui_file[1])
        text = self.img_text[id]
        # logo_img = Image.open(self.ui_path + '/' + self.ui_file[id])
        draw = ImageDraw.Draw(logo_img)
        draw.text((10.5, 5), text, (255, 255, 255), font = self.fontStyle)
        draw.text((80.5, 136), str(confidence) + '%', (255, 255, 255), font = self.fontStyle)

        src_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        #识别框最小限制
        new_points = self._img_draw_update(points, src_img.size)

        logo_img = logo_img.resize((new_points[2] - new_points[0], new_points[3] - new_points[1]))
        src_img.paste(logo_img, (new_points[0], new_points[1]), logo_img)

        return cv2.cvtColor(numpy.asarray(src_img), cv2.COLOR_RGB2BGR)

    def _img_draw_update(self, points, max):
        """矩形框大小适配

        Args:
            points (tuple): 矩形框位置
            max (tuple): x轴y轴最大值

        Returns:
            [tuple]: 适配后的矩形框位置
        """        
        len_x = points[2] - points[0]
        len_y = points[3] - points[1]
        point_centor = (points[0] + len_x//2, points[1] + len_y//2)
        if len_x < self.least_size[0]:
            len_x = self.least_size[0]
        if len_y < self.least_size[1]:
            len_y = self.least_size[1]
        left_upper_x = point_centor[0] - len_x//2
        right_down_x = point_centor[0] + len_x//2
        if left_upper_x < 0:
            right_down_x = right_down_x - left_upper_x
            left_upper_x = 0
        elif right_down_x > max[0]:
            left_upper_x = left_upper_x - (right_down_x - max[0])
            right_down_x = max[0]

        left_upper_y = point_centor[1] - len_y//2
        right_down_y = point_centor[1] + len_y//2
        if left_upper_y < 0:
            right_down_y = right_down_y - left_upper_y
            left_upper_y = 0
        elif right_down_y > max[1]:
            left_upper_y = left_upper_y - (right_down_y - max[1])
            right_down_y = max[1]

        return (left_upper_x, left_upper_y, right_down_x, right_down_y)

    def face_static(self):
        """人脸口罩统计

        Returns:
            [tuple]: (已戴口罩统计, 未戴口罩统计)
        """
        face_mask = 0
        face_nomask = 0
        for item in self.inference_data:
            item_confidence = item[1]*100
            mask_att = item[2]
            if item_confidence >= self.confidence:
                if mask_att == WARE_SIG:
                    face_mask = face_mask + 1
                else:
                    face_nomask = face_nomask + 1
        return (face_mask, face_nomask)

# if __name__ == '__main__':
#
#     from oneai.mask_detection_solver import MaskDetectionSolver
#     from jetcam.usb_camera import USBCamera
#
#     path2 = os.path.abspath(os.path.join(os.getcwd(), "../.."))
#     path = os.path.join(path2, "view/resource/images")
#     print('-------------')
#     print(path)
#
#     face_mask_solver = MaskDetectionSolver()
#     camera = USBCamera(width=1024, height=576)
#     face_mask_solver.load()
#
#     # sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#
#     while True:
#         img_raw = camera.read()
#         result = face_mask_solver.detect_face_mask(img_raw)
#         face_mask_prop = FaceMaskProp(img_raw, result.result_data, 90, ('已戴口罩', '未戴口罩'), path)
#         # print('mask:%d, nomask:%d' %())
#         image = face_mask_prop.make_img()
#         cv2.imshow('', image)
#         if cv2.waitKey(1) == 27:
#             break
#
#     face_mask_solver.unload()
