#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:object_model.py
# Created:2020/5/26 下午7:23
# Author:ldchr
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:智能盘点model

from model.object_solver import ObSlover
from config.object_config_util import ConfigUtils
import cv2
import numpy as np

from R import R
from model.image import ImagePaste
from PIL import Image, ImageDraw, ImageFont
import os
from oneai.common.utils.image_helper import ImageHelper


class ObModel(object):
    def __init__(self):
        self.solver = ObSlover()
        self.solver.load()
        self.objects = ()
        self.configUtils = ConfigUtils()
        self.threshold = 0.4
        self.detections = None
        self.image = None
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.ttc_path = self.base_path + R.ttc_simsun
        self.fontStyle = ImageFont.truetype(self.ttc_path, 15, encoding="utf-8")
        # 框体颜色BGR
        self.colors = ((254, 137, 145), (142, 212, 161), (46, 179, 244), (203, 203, 203))
        # 字体 颜色 RGB
        self.text_colors = ((145, 137, 254), (161, 212, 142), (244, 179, 46), (203, 203, 203))
        self.keys = list()

    """
        objects  list 类型
    """

    def setobjects(self, objects):
        self.objects = objects

    def unload(self):
        self.solver.unload()

    def detect(self, image, threshold=0.4):
        self.threshold = threshold
        image = ImageHelper.convert_undistorted_img(image)
        self.detections, self.image = self.solver.detectImg(image, threshold)
        return self.make_image()

    def make_image(self, out_size=None):
        """生成带标记的结果图片

        :param out_size: 输出图片大小
        :return: image
        """
        return self.get_visual_image_maker()(out_size)

    def get_visual_image_maker(self):

        def visual_image_maker(out_size):
            img = self.cvDrawBoxes(self.detections, self.image, out_size)
            return img

        return visual_image_maker

    # def convertBack(self, x, y, w, h):
    #     xmin = int(round(x - (w / 2)))
    #     xmax = int(round(x + (w / 2)))
    #     ymin = int(round(y - (h / 2)))
    #     ymax = int(round(y + (h / 2)))
    #     return xmin, ymin, xmax, ymax

    '''
        投影效果
    '''

    def textDrawShadow(self, x, y, draw, fillcolor, font, shadowcolor, text):
        # draw.text((x - 1, y), text, font=font, fill=shadowcolor)
        # draw.text((x + 1, y), text, font=font, fill=shadowcolor)
        # draw.text((x, y - 1), text, font=font, fill=shadowcolor)
        # draw.text((x, y + 1), text, font=font, fill=shadowcolor)
        # # thicker border
        # draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
        # draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
        # draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
        # draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
        # now draw the text over it
        draw.text((x, y), text, font=font, fill=fillcolor)

    def cvDrawBoxes(self, detections, img, out_size=None):
        scaling = (1.0, 1.0)
        if out_size is not None and out_size != self.image_size:
            img = cv2.resize(img, out_size)
            scaling = np.array(out_size) / self.image_size
        self.keys.clear()
        for detection in detections:
            x1, y1, x2, y2 = detection[2][0] * scaling[0], \
                         detection[2][1] * scaling[1], \
                         detection[2][2] * scaling[0], \
                         detection[2][3] * scaling[1]
            # xmin, ymin, xmax, ymax = self.convertBack(
            #     float(x), float(y), float(w), float(h))
            # 防止边框超出屏幕
            x1 = 0 if x1 + 10 < 0 else x1
            y1 = 20 if y1 - 20 < 0 else y1
            pt1 = (int(x1), int(y1))
            pt2 = (int(x2), int(y2))
            key = detection[0]
            self.keys.append(key)
            color = self.colors[3]
            text_color = self.text_colors[3]
            for object in self.objects:
                if key == object[0]:
                    if isinstance(object[1], int):
                        color = self.colors[object[1]]
                        text_color = self.text_colors[object[1]]
                    else:
                        print("color type require integer")
            # cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
            rect_image = ImagePaste(self.configUtils.getValue(key), str(round(detection[1] * 100)))
            # rect_image = rect_image.draw_rect((pt2[0] - pt1[0], pt2[1] - pt1[1]), color)
            out_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            # out_image.paste(rect_image, pt1, rect_image)
            out_image = out_image.convert("RGBA")
            text_image = Image.new("RGBA", out_image.size, (0, 0, 0, 0))
            darw_text = ImageDraw.Draw(text_image)
            r = 14
            if pt2[0] - pt1[0] < 14 or pt2[0] - pt1[0] < 14:
                r = 0
            elif 14 < pt2[0] - pt1[0] < 45 or 14 < pt2[0] - pt1[0] < 45:
                r = 3
            self.textDrawShadow(pt1[0] + 10, pt1[1] - 20, darw_text, text_color, self.fontStyle, (0, 0, 0, 178),
                                self.configUtils.getValue(detection[0]) + str(round(detection[1] * 100)) + "%")
            combined = Image.alpha_composite(out_image, text_image)
            img = cv2.cvtColor(np.asanyarray(combined), cv2.COLOR_RGB2BGR)
            self.rounded_rectangle(img, pt1, pt2, r, color, 2)
        # print(self.keys)
        return img, self.keys

    def rounded_rectangle(self, img, pt1, pt2, corner_radius, fill=None, outline=None):
        upper_left_point = pt1  # (upper_left_point[0], upper_left_point[1])
        bottom_right_point = pt2  # (bottom_right_point[0],bottom_right_point[1])
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
