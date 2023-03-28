from PIL import Image, ImageDraw, ImageFont
import sys, os
import cv2
import numpy as np
import random

from R import R

"""
    智能盘点识别框绘制
"""


class ImagePaste(object):

    def __init__(self, title, threshold):
        self.title = title
        self.threshold = threshold
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.up_image_path = self.base_path + '/resource/images/up_icon.png'
        self.down_image_path = self.base_path + '/resource/images/down_icon.png'
        self.rect_image_path = self.base_path + '/resource/images/rect_icon.png'
        self.ttc_path = self.base_path + R.ttc_simsun

    def draw_imgUp(self):
        up_image = Image.open(self.up_image_path)
        draw = ImageDraw.Draw(up_image)
        fontStyle = ImageFont.truetype(self.ttc_path, 15, encoding="utf-8")
        draw.text((5, 5), self.title, (255, 255, 255), font=fontStyle)
        return up_image

    def draw_imgDown(self):
        down_image = Image.open(self.down_image_path)
        draw = ImageDraw.Draw(down_image)
        fontStyle = ImageFont.truetype(self.ttc_path, 15, encoding="utf-8")
        draw.text((15, 5), self.threshold, (255, 255, 255), font=fontStyle)
        return down_image

    def draw_rect(self, size, color):
        rect_image = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(rect_image)
        r = 14
        if size[0] < 14 or size[1] < 14:
            r = 0
        elif 14 < size[0] < 45 or 14 < size[1] < 45:
            r = 3
        self.rounded_rectangle(draw, ((0, 0), (size[0] - 3, size[1] - 3)), r, fill=color, outline=1)
        return rect_image

    def rounded_rectangle(self, draw, xy, corner_radius, fill=None, outline=None):
        upper_left_point = xy[0]  # (upper_left_point[0], upper_left_point[1])
        bottom_right_point = xy[1]  # (bottom_right_point[0],bottom_right_point[1])
        # top
        draw.line([(upper_left_point[0] + corner_radius, upper_left_point[1]),
                   (bottom_right_point[0] - corner_radius, upper_left_point[1])], fill=fill, width=outline)
        # cv2
        draw.line([(upper_left_point[0] + corner_radius, bottom_right_point[1]),
                   (bottom_right_point[0] - corner_radius, bottom_right_point[1])], fill=fill, width=outline)
        # left
        draw.line([(upper_left_point[0], upper_left_point[1] + corner_radius),
                   (upper_left_point[0], bottom_right_point[1] - corner_radius)], fill=fill, width=outline)
        # right
        draw.line([(bottom_right_point[0], upper_left_point[1] + corner_radius),
                   (bottom_right_point[0], bottom_right_point[1] - corner_radius)], fill=fill, width=outline)
        draw.arc(
            [upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
            180,
            270,
            fill=fill,
            width=outline)
        draw.arc([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2),
                  bottom_right_point],
                 0,
                 90,
                 fill=fill, width=outline
                 )
        draw.arc([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2),
                  (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
                 90,
                 180,
                 fill=fill, width=outline
                 )
        draw.arc([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]),
                  (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
                 270,
                 360,
                 fill=fill, width=outline
                 )

