import cv2, numpy, os, sys
from PIL import Image, ImageDraw, ImageFont

# def handle_recognition_result(result=None, title=None):
#     a_result = result.result_data
#
#     pil_image = Image.fromarray(result.image)
#     draw = ImageDraw.Draw(pil_image)
#     for i in a_result:
#         data = i
#         name = data[0]
#         top = int(data[2] / result.narrow_rate)
#         right = int(data[3] / result.narrow_rate)
#         bottom = int(data[4] / result.narrow_rate)
#         left = int(data[1] / result.narrow_rate)
#
#         color = (255, 0, 0) if name == title else (0, 255, 0)
#
#         font_style = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + '/resource/simsun.ttc', 20,
#                                        encoding="utf-8")
#
#         draw.text((left + 10, top - 22), name, color, font=font_style)
#         draw.text((right - 10 - 22, bottom - 22), str(90), color, font=font_style)
#
#         result.image = numpy.asarray(pil_image)
#
#         rounded_rectangle(result.image, (left, top), (right, bottom), 10, color, outline=1)
#
#     result.image = cv2.cvtColor(result.image, cv2.COLOR_RGB2BGR)
#     del draw
#
#     return result.image


def rounded_rectangle(img, pt1, pt2, corner_radius, fill=None, outline=None):
    upper_left_point = pt1
    bottom_right_point = pt2
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