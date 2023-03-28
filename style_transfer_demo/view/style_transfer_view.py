#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File:style_transfer_view.py
# Created:2020/9/14 下午16:27
# Author:zzj
# CopyRight 2020-2020 Ubtech Robotics Corp. All rights reserved.
# Description:风格迁移View
import math
import os
import sys
import numpy as np
from PIL import Image

from PyQt5 import QtWidgets, QtCore

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from rotate_icon import RotateIcon
from palette_btn import PaletteButton
from common.ui.commonDialog.BaseDialog import BaseDialogView
from config.config_util import StyleUtils
from view.scene_item import SceneItem
from view.vertical_scrollbar import UbtVerticalScrollBar
from common.ui.gallery.gallery_window import GalleryWindow
from canvas import Canvas

from R import R
from common.utility.configure_string_single import ConfigureStringSingle
from it_btn import IconAndTextButton
from style import Ui_Base
import random

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QVBoxLayout, QListWidgetItem, QGridLayout, \
    QScrollArea, QFileDialog

from common.ui.widget.buttonlabel import ButtonLabel
from functools import wraps


def opera_interceptor(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        o = args[0]
        # print('state', o.produce_result_state)
        if not o.produce_result_state == 1:
            return func(*args, **kwargs)

    return wrap


class StyleTransferView(QWidget):
    produceSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()
        self.parent = parent
        self.widget = Ui_Base()
        self.widget.setupUi(parent)
        self.btn_close = None
        self.export_btn = None
        self.produce_result_state = 0

        self.init_ui(parent)

    def init_ui(self, widget):
        with open(R.qss_style) as fp:
            qss = fp.read()
            widget.setStyleSheet(qss)

        self.widget.root.setStyleSheet("QFrame#root{border-image:url(%s);"
                                       "border: 0rem outset pink;"
                                       "outline: 0rem solid khaki;"
                                       "margin: 0rem;padding: 0rem;outline-offset: 0rem;}" % R.imgs_img_bg)
        self.produce_result_state = 0
        self.add_export_btn(self.widget.btn_export.layout())
        self.util = StyleUtils()
        self.init_style()
        self.init_sample()
        self.init_canvas()
        self.init_product()

        real_content = self.widget
        real_content.card_icon.setPixmap(QPixmap(R.imgs_img_logo_fenggeqianyi))

        self.init_palette_buttons(self.widget.palette.layout())

        self.widget.img_handle.setStyleSheet("background-color:#4F5A7E;"
                                             "border-top-left-radius: 8px;border-top-right-radius: 8px;")
        orig_label = QLabel(self.common_cfg.get_value_for_key('ubt_style_original_img'))
        # orig_label.setFixedSize(150,80)
        orig_label.setStyleSheet(
            "font-family: Source Han Sans CN;font-weight: bold;margin-left:30px;"
            "font-size: 26px;color: #FFFFFF;line-height: 48px;")
        self.widget.img_handle.layout().addWidget(orig_label)

        self.scBtn = IconAndTextButton(self.common_cfg.get_value_for_key('ubt_style_produce'),
                                       R.imgs_ic_shengcheng)
        self.scBtn.setMinimumSize(QSize(120, 50))
        self.scBtn.clicked.connect(self.produce)

        self.widget.img_handle.layout().addWidget(self.scBtn)
        self.widget.img_handle.setFixedSize(640, 80)

        self.widget.img.layout().addWidget(self.canvas)
        self.widget.img.setGeometry(0, 80, 640, 480)

        # palette = QPalette()
        # palette.setBrush(self.backgroundRole(), QBrush(QPixmap(R.imgs_img_bg)))
        # self.parent.setPalette(palette)

        real_content.top_title.setText(self.common_cfg.get_value_for_key('ubt_style_transfer_title'))
        real_content.sub_title.setText(
            self.common_cfg.get_value_for_key('ubt_style_transfer_subtitle').replace("\\n", "\n"))

        # real_content.operate.setStyleSheet(
        #     "QWidget{background-color:#665B6995;border-bottom-left-radius: 8px;border-bottom-right-radius: 8px;"
        #     "border-top-left-radius: 8px;border-top-right-radius: 8px;}")

        btn_close = ButtonLabel()
        self.btn_close = btn_close
        btn_close.set_selector(R.imgs_ic_close, R.imgs_ic_close_press)
        btn_close.setPixmap(QPixmap(R.imgs_ic_close))
        btn_close.setObjectName(u"btn_close")
        btn_close.setMinimumSize(QSize(42, 42))
        btn_close.setAlignment(Qt.AlignCenter)

        real_content.root.layout().addWidget(btn_close, 0, Qt.AlignTop)
        btn_close.clicked.connect(self.parent.show_exit)

    def init_style(self):
        layout = self.widget.img_style.layout()

        style_list = self.util.getStyles()
        self.cur_style = style_list[0][0]

        self.left_style = QLabel()
        self.left_style.setFixedSize(115, 90)
        style_icon = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.util.getImgForStyle(self.cur_style))
        pm = QPixmap(style_icon)
        pm = pm.scaled(115, 86)
        self.left_style.setPixmap(pm)

        # add mask
        mask = QLabel(self.left_style)
        pix = QPixmap(R.imgs_ic_grey_border)
        mask.setPixmap(pix)

        layout.addWidget(self.left_style, 0, Qt.AlignCenter)

        rb = ButtonLabel()
        rb.setAlignment(Qt.AlignCenter)
        rb.setFixedSize(28, 90)
        rb.setStyleSheet("background-color:#7385BA;border-top-right-radius: 8px;border-bottom-right-radius: 8px;")
        rb.setPixmap(QPixmap(R.imgs_ic_pull_down))
        rb.set_selector(R.imgs_ic_pull_down, R.imgs_ic_pull_down)
        rb.clicked.connect(self.show_style_select_pop)
        self.scene_pop = GalleryWindow(rb, parent=self.parent)
        self.handle_scene_style(self.scene_pop.content.layout(), style_list)
        layout.addWidget(rb)

    def init_canvas(self):
        self.cur_style_sample = self.util.getSampleForStyle(self.cur_style).split(",")[0]
        self.canvas = Canvas(self.cur_style_sample)
        self.canvas.change_signal.connect(self.canvas_change)

        self.sample_scenes[0].update(self.cur_style_sample)

    @opera_interceptor
    def canvas_change(self):
        self.produce_empty()
        self.export_btn.set_click_enable(False)
        self.update_revokeBtn()

    def init_product(self):
        name = self.util.getNameForStyle(self.cur_style)
        txt = self.common_cfg.get_value_for_key('ubt_style_transfer')
        self.style_name_label = QLabel(f'{txt}：《{name}》')
        self.widget.result_label.setStyleSheet(
            "background-color:#4F5A7E;border-top-left-radius: 8px;border-top-right-radius: 8px;"
            "font-family: Source Han Sans CN;font-weight: bold;padding-left:20px;"
            "font-size: 26px;color: #FFFFFF;line-height: 48px;")
        self.widget.result_label.layout().addWidget(self.style_name_label)
        self.widget.result_label.setFixedSize(640, 80)

        self.produce_empty()

    def handle_scene_style(self, layout, style_list):
        grid = QGridLayout()
        grid.setVerticalSpacing(10)
        grid.setRowMinimumHeight(1, 90)

        line = len(style_list) / 2

        line = line + 0.1

        height = round(line) * 90 + 10 * (round(line) + 1)

        if height <= 280:
            height = 280
        topfilter = QWidget()
        # topfilter.setStyleSheet(
        #     "QWidget{background-color:#ff0;border-bottom-left-radius: 8px;border-bottom-right-radius: 8px;}")
        topfilter.setMinimumSize(260, height)
        topfilter.setLayout(grid)

        scroll = QScrollArea()

        scroll.setWidget(topfilter)
        scroll.setAlignment(Qt.AlignCenter)
        scroll.setVerticalScrollBar(UbtVerticalScrollBar(Qt.Vertical))
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(scroll)

        positions = [(i, j) for i in range(math.ceil(len(style_list) / 2)) for j in range(2)]

        for position, style in zip(positions, style_list):
            widget = SceneItem(style[0], style[1], False)
            widget.updateSelectSignal.connect(self.style_select)
            grid.addWidget(widget, *position)

    @opera_interceptor
    def style_select(self, scene):
        if self.cur_style == scene.name:
            return
        if self.canvas.can_revoke():
            self.show_switch_confirm_dialog(scene, True)
        else:
            self.temp_scene = scene
            self.do_real_switch_style()

    def do_real_switch_style(self):
        self.cur_style = self.temp_scene.name
        self.sample_list = self.util.getSampleForStyle(self.cur_style).split(",")
        self.cur_style_sample = self.sample_list[0]

        # update palette
        palette_layout = self.widget.palette.layout()
        for i in range(palette_layout.count()):
            palette_layout.itemAt(i).widget().deleteLater()
        self.init_palette_buttons(palette_layout)

        # update style name
        name = self.util.getNameForStyle(self.cur_style)
        txt = self.common_cfg.get_value_for_key('ubt_style_transfer')
        self.style_name_label.setText(f'{txt}：《{name}》')

        # remove product
        self.produce_empty()

        # enable produce btn clicked, not immediately for enable
        # self.scBtn.set_click_enable(True)

        # update style
        pm = QPixmap(self.temp_scene.resid)
        pm = pm.scaled(115, 86)
        self.left_style.setPixmap(pm)
        self.scene_pop.show_pop()

        # update sample
        layout = self.widget.img_sample.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()
        self.init_sample()

        # update canvas
        self.canvas.select(self.cur_style_sample)

        self.sample_scenes[0].update(self.cur_style_sample)

        # do not release model,only do it before load next model
        # self.release()

    @opera_interceptor
    def show_style_select_pop(self):
        self.scene_pop.show_pop()

    def init_sample(self):
        self.widget.img_sample.setStyleSheet('background-color:transparent;margin-left:0px;')
        layout = self.widget.img_sample.layout()

        # add left scroll
        self.lb = ButtonLabel()
        self.lb.setFixedSize(28, 90)
        self.lb.setPixmap(QPixmap(R.imgs_ic_left_enable))
        self.lb.set_selector(R.imgs_ic_left_enable, R.imgs_ic_left_disable)
        layout.addWidget(self.lb)
        self.lb.clicked.connect(self.move_left)

        self.add_sample_scene(layout)

        # add right scroll
        self.rb = ButtonLabel()
        self.rb.setFixedSize(28, 90)
        self.rb.setPixmap(QPixmap(R.imgs_ic_right_enable))
        self.rb.set_selector(R.imgs_ic_right_enable, R.imgs_ic_right_disable)
        layout.addWidget(self.rb)
        self.rb.clicked.connect(self.move_right)

        self.left_scroll_visible_item = self.sample_list_widget.item(0)
        self.right_scroll_visible_item = self.sample_list_widget.item(3)

        if len(self.sample_list) <= 4:
            self.lb.hide()
            self.rb.hide()
        else:
            self.lb.show()
            self.rb.show()
            self.lb.set_click_enable(False)
            self.rb.set_click_enable(True)

    @opera_interceptor
    def move_left(self):
        index = self.sample_list_widget.indexFromItem(self.left_scroll_visible_item).row()
        print(index)
        index -= 1
        item = self.sample_list_widget.item(index)
        if item is not None:
            self.sample_list_widget.scrollToItem(item)
            self.left_scroll_visible_item = item
            self.right_scroll_visible_item = self.sample_list_widget.item(index + 3)
            self.rb.set_click_enable(True)

        n_item = self.sample_list_widget.item(index - 1)
        if n_item is None:
            self.lb.set_click_enable(False)

    @opera_interceptor
    def move_right(self):
        index = self.sample_list_widget.indexFromItem(self.right_scroll_visible_item).row()
        print(index)
        index += 1
        item = self.sample_list_widget.item(index)
        if item is not None:
            self.sample_list_widget.scrollToItem(item)
            self.right_scroll_visible_item = item
            self.left_scroll_visible_item = self.sample_list_widget.item(index - 3)
            self.lb.set_click_enable(True)

        n_item = self.sample_list_widget.item(index + 1)
        if n_item is None:
            self.rb.set_click_enable(False)

    def add_sample_scene(self, layout):

        """
            add sample scene
        :param layout:
        :return:w mei
        """
        list_widget = QListWidget()
        self.sample_list_widget = list_widget

        # list_widget.setMinimumSize(480, 86)
        # list_widget.setMaximumSize(480, 86)
        list_widget.setFlow(QListWidget.LeftToRight)
        # list_widget.setSpacing(2)
        list_widget.setWrapping(False)
        list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget.setHorizontalScrollMode(QListWidget.ScrollPerPixel)

        layout.addWidget(list_widget, 0, Qt.AlignCenter)

        self.sample_list = self.util.getSampleForStyle(self.cur_style).split(",")

        sample_count = len(self.sample_list)

        list_width = sample_count * 129
        if list_width > 508:
            list_width = 518
        list_widget.setFixedSize(list_width, 94)
        self.sample_scenes = []
        for sample in self.sample_list:
            widget = SceneItem(self.cur_style, sample, True)
            widget.updateSelectSignal.connect(self.select_sample)

            item = QListWidgetItem()
            # item.setFlags(~Qt.ItemIsEnabled)
            item.setFlags(Qt.ItemIsUserCheckable)
            item.setSizeHint(QSize(129, 90))
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)
            self.sample_scenes.append(widget)

    @opera_interceptor
    def select_sample(self, scene):
        if self.cur_style_sample == scene.resid:
            return
        if self.canvas.can_revoke():
            self.show_switch_confirm_dialog(scene, False)
        else:
            self.temp_scene = scene
            self.do_switch_sample()

    def show_switch_confirm_dialog(self, scene, is_style):
        """
        切换弹窗确认
        :param scene:
        :param is_style:True:切换风格;False:切换预制图
        :return:
        """
        desc = self.common_cfg.get_value_for_key('ubt_style_transfer_dialog_tip').replace("\\n", "\n")
        sure = self.common_cfg.get_value_for_key('ubt_sure')

        self.confirm_dialog = BaseDialogView(title=desc, ok_txt=sure,
                                             sure_button_action=self.do_real_switch_style if is_style else self.do_switch_sample,
                                             parent=self.parent)
        self.confirm_dialog.show()
        self.temp_scene = scene

    def do_switch_sample(self):
        self.cur_style_sample = self.temp_scene.resid
        self.canvas.select(self.cur_style_sample)

        self.produce_empty()

        for item in self.sample_scenes:
            item.update(self.temp_scene.resid)

    @opera_interceptor
    def revoke(self):
        if self.canvas.can_revoke():
            self.canvas.revoke()
            self.update_revokeBtn()

    def update_revokeBtn(self):
        self.revokeBtn.set_click_enable(self.canvas.can_revoke())
        # if self.canvas.can_revoke():
        #     self.revokeBtn.setPixmap(QPixmap(R.imgs_ic_back))
        #     self.revokeBtn.set_selector(R.imgs_ic_back, R.imgs_ic_back_click)
        # else:
        #     self.revokeBtn.setPixmap(QPixmap(R.imgs_ic_back_click))
        #     self.revokeBtn.set_selector(R.imgs_ic_back_click, R.imgs_ic_back_click)

    def get_file_name(self, file_path, file_name):
        str_copy = self.common_cfg.get_value_for_key('ubt_style_copy')
        f = os.path.join(file_path, file_name)
        num = -1
        try:
            if os.path.exists(f):
                files = os.listdir(file_path)
                for sf in files:
                    if file_name[:-4] in sf:
                        left = sf[:-4].replace(file_name[:-4], "")
                        if left == "":
                            if num == -1:
                                num = 0
                        else:
                            tmp = int(left[len(str_copy) + 1:])
                            if tmp > num:
                                num = tmp
        except:
            pass
        finally:
            if num == -1:
                return f
            else:
                str_list = list(f)
                content = f'-{str_copy}{str(num + 1)}'
                str_list.insert(-4, content)
                return "".join(str_list)

    @opera_interceptor
    def save(self, filepath='/home/oneai/styletransfer'):
        if not self.produce_result_state == 2:
            return

        name = self.util.getNameForStyle(self.cur_style)
        title = self.common_cfg.get_value_for_key('ubt_style_transfer_title')
        file_name = f'{title}《{name}》.jpg'

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        target_file = self.get_file_name(filepath, file_name)

        file, suffix = QFileDialog.getSaveFileName(self, self.common_cfg.get_value_for_key('ubt_style_file_save'),
                                                   target_file[:-4], '.jpg;;.png')
        result = file + suffix
        if not len(result) == 0:
            self.widget.left.hide()
            self.widget.operate.hide()
            self.scBtn.hide()
            self.btn_close.hide()

            # threading.Thread(target=self.real).start()
            self.widget.root.grab().save(result)

            data = np.array(Image.open(result))
            data[200:913, :, :] = data[350:1063, :, :]
            im = Image.fromarray(data[0:883, :, :])
            im.save(result)

            self.widget.left.show()
            self.widget.operate.show()
            self.scBtn.show()
            self.btn_close.show()

    def init_palette_buttons(self, layout):
        """
        add palette
        """
        colors = self.util.getColorForStyle(self.cur_style).split(",")
        self.palettes = []
        for c in colors:
            b = PaletteButton(c)
            b.pressed.connect(lambda c=c: self.select_color(c))
            layout.addWidget(b)
            self.palettes.append(b)

        self.select_color(colors[0])

        self.revokeBtn = ButtonLabel()
        self.revokeBtn.setFixedSize(50, 51)
        self.revokeBtn.setPixmap(QPixmap(R.imgs_ic_back))
        self.revokeBtn.set_selector(R.imgs_ic_back, R.imgs_ic_back_click)
        self.revokeBtn.clicked.connect(self.revoke)
        self.update_revokeBtn()
        label = QLabel()
        label.setFixedWidth(20)
        layout.addWidget(label)
        # layout.addItem(QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addWidget(self.revokeBtn)

    @opera_interceptor
    def select_color(self, c):
        self.canvas.set_pen_color(c)

        # update palette select state
        for palette in self.palettes:
            palette.update(c)

    def add_export_btn(self, layout):
        self.export_btn = IconAndTextButton(self.common_cfg.get_value_for_key('ubt_style_export'), R.imgs_ic_daochu)
        self.export_btn.clicked.connect(self.save)
        layout.addWidget(self.export_btn)
        self.export_btn.set_click_enable(False)

    @opera_interceptor
    def produce(self):
        if not self.produce_result_state == 0:
            return
        layout = self.widget.img_result.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()

        sid = self.cur_style.replace("style", "")
        img_path = self.canvas_scrap()
        self.produce_load()
        self.fun(int(sid), img_path)
        self.produceSignal.emit()
        self.scBtn.set_click_enable(False)

    def canvas_scrap(self):
        self.tmp_path = '/home/oneai/style_tmp.png'
        self.widget.img.grab().scaled(480, 320).save(self.tmp_path)
        return self.tmp_path

    def load_model(self):
        self.label_empty_txt.setText(self.common_cfg.get_value_for_key('ubt_style_load_model'))
        
    def load_model_finish(self):
        self.label_empty_txt.setText(self.common_cfg.get_value_for_key('ubt_style_generate'))

    def show_result(self, showImg):
        self.scBtn.set_click_enable(True)
        if not self.produce_result_state == 1:
            return
        self.canvas.set_can_draw(True)
        self.produce_result_state = 2
        os.remove(self.tmp_path)
        layout = self.widget.img_result.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()

        img = QPixmap.fromImage(showImg)
        img = img.scaled(640, 480)
        lab = QLabel()
        lab.setPixmap(img)
        self.widget.img_result.layout().addWidget(lab)

        mask = QLabel(lab)
        pix = QPixmap(R.imgs_ic_bottom_round_border)
        mask.setPixmap(pix)
        self.export_btn.set_click_enable(True)

    @opera_interceptor
    def produce_load(self):
        self.canvas.set_can_draw(False)
        self.produce_result_state = 1
        layout = self.widget.img_result.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()
        default = QWidget()
        layout = QVBoxLayout()
        label_empty_icon = RotateIcon(R.imgs_img_loading, 72, 72)
        # label_empty_icon.show()

        # label_empty_icon.runAnim()
        # label_empty_icon.setPixmap(QPixmap(R.imgs_img_loading))
        label_empty_icon.setStyleSheet('margin-bottom:30px;')
        layout.addWidget(label_empty_icon, 0, Qt.AlignCenter)

        self.label_empty_txt = QLabel(self.common_cfg.get_value_for_key('ubt_style_generate'))
        self.label_empty_txt.setMinimumHeight(50)
        self.label_empty_txt.setStyleSheet(
            'font-family: Source Han Sans CN;font-weight: bold;font-size: 16px;margin-top:20px;'
            'color: #FFFFFF;text-align: center;line-height: 20px;')
        layout.addWidget(self.label_empty_txt, 1, Qt.AlignCenter)

        self.tip = QtWidgets.QLabel(self.get_loading_tip())
        self.tip.setMinimumSize(QtCore.QSize(400, 60))
        # self.tip.setMaximumSize(QtCore.QSize(400, 16777215))
        self.tip.setWordWrap(True)
        self.tip.adjustSize()
        self.tip.setScaledContents(True)
        self.tip.setStyleSheet('font-family: Source Han Sans CN;font-weight: normal;font-size: 14px;color: #66FFFFFF;margin-top:0px;')
        self.tip.setMinimumHeight(80)
        layout.addWidget(self.tip, 1, QtCore.Qt.AlignHCenter)

        default.setLayout(layout)
        self.widget.img_result.layout().addWidget(default, Qt.AlignCenter)

    def get_loading_tip(self):
        cfg = ConfigureStringSingle.get_common_string_cfg()
        idx = random.randint(1, 10)
        return cfg.get_value_for_key(f'ubt_style_loading_tip{idx}')

    def produce_empty(self):
        self.canvas.set_can_draw(True)
        self.produce_result_state = 0
        layout = self.widget.img_result.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()
        default = QWidget()
        layout = QVBoxLayout()
        label_empty_icon = QLabel()
        label_empty_icon.setPixmap(QPixmap(R.imgs_img_yulanqu))
        label_empty_icon.setStyleSheet('margin-bottom:30px;')
        layout.addWidget(label_empty_icon, 0, Qt.AlignCenter)

        label_empty_txt = QLabel(self.common_cfg.get_value_for_key('ubt_style_preview'))
        label_empty_txt.setStyleSheet('font-family: Source Han Sans CN;font-weight: bold;font-size: 16px;'
                                      'color: #FFFFFF;text-align: center;line-height: 20px;')
        layout.addWidget(label_empty_txt, 1, Qt.AlignCenter)

        default.setLayout(layout)
        self.widget.img_result.layout().addWidget(default)
        if self.export_btn is not None:
            self.export_btn.set_click_enable(False)

    def setSingal(self, fun, release):
        self.fun = fun
        self.release = release
