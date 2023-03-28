#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: ObjectDetectionSolver.py
# Created: 2020-04-28 18:24:02
# Author: kyang(kun.yang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:
###

import cv2
import sys
import os,json
from oneai.common.base.Constants import InferParamenterAssister
from oneai.common.config.default_config import DeFaultConfig
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from oneai.ObjectDetectionSolver import ObjectDetectionSolver
from oneai.common.utils.common_utility import CommonUtil
class ObSlover(ObjectDetectionSolver):
    def __init__(self):
        ObjectDetectionSolver.__init__(self, DeFaultConfig.grpc_port, DeFaultConfig.grpc_ip)

    def detectImg(self, image, threshold=0.3, num_of_target=8):

        """"
        :param image: 待检测的图片数据
        :param threshold: 识别置信度阈值
        :param num_of_target: 识别目标的最大数目

        :return: 包含被识别出的物体信息的列表 , 原始图片按照darknet中的需要的尺寸调整大小
        """

        return self.get_detections()(image, threshold, num_of_target)

    def get_detections(self, infer_param=None):
        """获取对图片进行检测的函数

        :param infer_param: 参数字典. 参见 InferParamenterAssister
        :return: 返回处理图片的函数，函数接受图片作为参数，形如 function(image), function 返回一个 ObjectDetectionResult 对象
        """
        if self.model is None:
            return None

        infer_id = InferParamenterAssister.get_param_value(InferParamenterAssister.infer_id, infer_param)
        if infer_id is None:
            infer_id = 0

        def hand(image, threshold, num_of_target):
            data = {}
            data[DeFaultConfig.data_keys[DeFaultConfig.func_key]] = 'inference'
            data[DeFaultConfig.data_keys[DeFaultConfig.image_key]] = CommonUtil.ndarray_to_base64str(image)
            data[DeFaultConfig.data_keys[DeFaultConfig.threshold_key]] = threshold
            data[DeFaultConfig.data_keys[DeFaultConfig.targets_key]] = num_of_target
            data[DeFaultConfig.data_keys[DeFaultConfig.model_key]] = self.model_name
            call_future = self.model.cmd_node(data)
            #可以使用call_future.add_done_callback添加回调函数，实现异步操作
            result = json.loads(call_future.result().buf)
            w = result[DeFaultConfig.data_keys[DeFaultConfig.width_key]]
            h = result[DeFaultConfig.data_keys[DeFaultConfig.height_key]]
            image = cv2.resize(image, (w,h))
            detections = result[DeFaultConfig.data_keys[DeFaultConfig.result_key]]

            return detections, image

        return hand
