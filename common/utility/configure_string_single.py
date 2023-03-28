import sys
import threading
import os
import gettext

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class ConfigureStringSingle(object):
    _instance_lock = threading.Lock()
    _init_flag = False

    def __init__(self, locale_dir, domain):
        self.locale_dir = locale_dir
        self.domain = domain
        self.locale_txt = None

        # only for test to set, if normal set None
        self.default_language = None

        self.init_locale()

    def init_locale(self):
        if not self.find_mo_file():
            self.default_language = ['en']

        t = gettext.translation(self.domain, self.locale_dir, languages=self.default_language, fallback=True)
        self.locale_txt = t.gettext

    def get_value_for_key(self, key):
        return self.locale_txt(key)

    def find_mo_file(self):
        return gettext.find(self.domain, self.locale_dir, languages=self.default_language, all=True)

    @classmethod
    def get_common_string_cfg(cls):
        locale_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locale')
        cfg = ConfigureStringSingle(locale_dir, "ai_common_lang")
        return cfg


if __name__ == '__main__':
    print(ConfigureStringSingle.get_common_string_cfg().get_value_for_key('ubt_load_error'))
