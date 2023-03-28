# -*-coding:utf-8 -*-
from common.base.presenter import Presenter
from common.utility.UBTQToastTools import UBTQToastTools
import re


class NameInputDialogPresenter(Presenter):

    def __init__(self, view):
        super(NameInputDialogPresenter, self).__init__(view)
        self.view.ok_clicked.connect(self._on_ok_clicked)
        self.view.cancel_clicked.connect(self._on_cancel_clicked)
        self.view.text_changed.connect(self._on_text_changed)
        self.pattern = r"^[\u4E00-\u9FA5A-Za-z0-9 ]+$"
        self.all_space_pattern = r"^[ ]+$"
        self.max_len = self.view.text_max_len()

    def _on_ok_clicked(self):
        """ 检查输入

        """
        text = self.view.get_input_text()
        if not re.match(self.pattern, text):
            UBTQToastTools.showTip("请勿输入非法字符", self.view)
            return
        self.view.notify_input(text.replace(" ", ""))

    def _on_cancel_clicked(self):
        """ 关闭对话框

        """
        self.view.close()

    def _on_text_changed(self, text):
        """ 输入框文字内容发生变化

        :param text: 当前文字内容
        """
        text_valid = False

        if len(text) > 0 and self._check_text(text):
            text_valid = True

        self.view.enable_ok_button(text_valid)

    def _check_text(self, text):
        """ 检查文字格式是否合法

        :param text: 要检查格式的文字
        :return: 文字合法返回True, 否则返回False
        """
        text_bytes = str.encode(text, encoding='gbk')
        byte_len = len(text_bytes)
        if byte_len > self.max_len:
            self.view.backspace()
            return not re.match(self.all_space_pattern, text[:-1])

        return not re.match(self.all_space_pattern, text)
