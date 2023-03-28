#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:config_util.py
# Created:2020/9/18 下午15:53
# Author:zzj
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:风格配置工具

import configparser
import os
import gettext
import threading

from common.utility.configure_string_single import ConfigureStringSingle


class StyleUtils(object):
    _instance_lock = threading.Lock()
    _init_flag = False

    def __init__(self, configpath=os.path.split(os.path.realpath(__file__))[0] + '/style_config.ini'):
        if not StyleUtils._init_flag:
            self.styles = "style.images"
            self.names = "style.name"
            self.colors = "style.colors"
            self.samples = "style.sample.images"
            self.config = configparser.RawConfigParser()
            self.config.read(configpath, encoding="utf-8")
            StyleUtils._init_flag = True
            self.lang_cfg = None
            self.init_locale()

    def __new__(cls, *args, **kwargs):
        if not hasattr(StyleUtils, "_instance"):
            with StyleUtils._instance_lock:
                if not hasattr(StyleUtils, "_instance"):
                    StyleUtils._instance = object.__new__(cls)

        return StyleUtils._instance

    def init_locale(self):
        locale_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locale')
        lang_cfg = ConfigureStringSingle(locale_dir, 'style')
        self.lang_cfg = lang_cfg

    def getStyles(self):
        return self.config.items(self.styles)

    def getNameForStyle(self, key):
        return self.lang_cfg.get_value_for_key(key)
        # return self.config[self.names][key]

    def getColorForStyle(self, key):
        return self.config[self.colors][key]

    def getImgForStyle(self, key):
        return self.config[self.styles][key]

    def getSampleForStyle(self, key):
        return self.config[self.samples][key]

    def get_section_value(self, section, key):
        return self.config[section][key]


if __name__ == '__main__':
    con = StyleUtils()
    print(con.getStyles())
    print(con.getImgForStyle('style2'))
    print(con.getSampleForStyle('style2'))
