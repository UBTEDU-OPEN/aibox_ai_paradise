# -*-coding:utf-8 -*-
from common.base.presenter import Presenter


class SliderPresenter(Presenter):

    def __init__(self, view):
        super(SliderPresenter, self).__init__(view)
        self.view.mouse_released.connect(self.on_mouse_released)

    def on_mouse_released(self):
        """ 处理鼠标释放事件

        鼠标释放时，如果滑块值发生了变化， 则发送value_changed信号
        :return:
        """
        if self.view.value != self.view.previous_value:
            self.view.value_changed.emit(self.view.value)
            self.view.previous_value = self.view.value

