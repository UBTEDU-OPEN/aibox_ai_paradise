import configparser
import sys, os
import gettext
import threading

from common.utility.configure_string_single import ConfigureStringSingle


class ConfigUtils(object):
    _instance_lock = threading.Lock()
    _init_flag = False

    def __init__(self, configpath=os.path.split(os.path.realpath(__file__))[0] + '/coco_names.ini'):
        if not ConfigUtils._init_flag:
            self.names = "coco.names"
            self.imgs = "coco.images"
            self.rcn = "strings.rcn"
            self.config = configparser.RawConfigParser()
            self.config.read(configpath, encoding="utf-8")
            ConfigUtils._init_flag = True
            self.lang_cfg = None
            self.init_locale()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ConfigUtils, "_instance"):
            with ConfigUtils._instance_lock:
                if not hasattr(ConfigUtils, "_instance"):
                    ConfigUtils._instance = object.__new__(cls)

        return ConfigUtils._instance

    def init_locale(self):
        locale_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locale')
        lang_cfg = ConfigureStringSingle(locale_dir, 'object')
        self.lang_cfg = lang_cfg

    """
        :return 列表类型的所有key
    """

    def getKeys(self):
        return self.config.options(self.names)

    """
        :return 所有键值对
    """

    def getCoCoNames(self):
        return self.config.items(self.names)

    def getValue(self, key):
        return self.lang_cfg.get_value_for_key(key)
        # return self.config[self.names][key]

    def getImgValue(self, key):
        return self.config[self.imgs][key]

    def get_section_value(self, section, key):
        return self.lang_cfg.get_value_for_key(key)
        # return self.config[section][key]


if __name__ == '__main__':
    pass
    config = ConfigUtils()
    print(config.getValue('charger'))
    # print(config.get_section_value(None, 'sub_title'))
    # print(config.getCoCoNames())
    # print(config.getValue('bicycle'))
    # fileName = os.path.join(os.path.dirname(__file__), "config/strings_cg.ini")
    # s_conf = ConfigUtils(fileName)
    # print(config.get_section_value(config.rcn, 'sub_title'))
