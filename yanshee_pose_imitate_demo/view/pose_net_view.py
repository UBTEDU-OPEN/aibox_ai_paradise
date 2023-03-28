#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys

from PyQt5 import QtCore

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from R import R
from common.utility.configure_string_single import ConfigureStringSingle
from view.comm_btn import CommonBtn
from view.rotate_icon import RotateIcon
from view.guide_item import GuideItem
from view.device_item import DeviceItem
from yanshee import Ui_Base
from dialogplaymotion_ui import Ui_DialogPlayMotion
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QDialog, QHBoxLayout

from common.ui.widget.buttonlabel import ButtonLabel
import subprocess


class PoseNetView(QWidget):
    produceSignal = QtCore.pyqtSignal()
    signal_show_full = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_count)
        self.common_cfg = ConfigureStringSingle.get_common_string_cfg()
        self.parent = parent
        self.widget = Ui_Base()
        self.widget.setupUi(parent)
        self.btn_close = None
        self.export_btn = None
        self.produce_result_state = 0
        self.widget_device_list = []
        self.latest_devices = []

        self.widget.dev_list.viewport().installEventFilter(self)

        self.init_ui(parent)

        self.is_loading = False

    def init_ui(self, widget):
        # 设置qss样式
        with open(R.qss_style) as fp:
            qss = fp.read()
            widget.setStyleSheet(qss)
        # 设置窗口背景
        self.widget.root.setStyleSheet("QFrame#root{border-image:url(%s);"
                                       "border: 0rem outset pink;"
                                       "outline: 0rem solid khaki;"
                                       "margin: 0rem;padding: 0rem;outline-offset: 0rem;}" % R.imgs_img_bg)
        # 设置左侧icon
        self.widget.card_icon.setPixmap(QPixmap(R.imgs_img_logo_demonstrate))

        # 设置顶部标题
        self.widget.top_title.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_imitate_title'))
        self.widget.sub_title.setText(
            self.common_cfg.get_value_for_key('ubt_yanshee_pose_imitate_subtitle').replace("\\n", "\n"))

        # 初始化流程说明
        self.init_guide_inst()

        # 初始化device
        self.init_device()

        # 初始化动作
        self.init_motion()

        # 添加使用按钮
        self.add_enter_btn(self.widget.motion.layout())

        # 添加关闭按钮
        btn_close = ButtonLabel()
        self.btn_close = btn_close
        btn_close.set_selector(R.imgs_ic_close, R.imgs_ic_close_press)
        btn_close.setPixmap(QPixmap(R.imgs_ic_close))
        btn_close.setObjectName(u"btn_close")
        btn_close.setMinimumSize(QSize(42, 42))
        btn_close.setAlignment(Qt.AlignCenter)
        self.widget.root.layout().addWidget(btn_close, 0, Qt.AlignTop)
        btn_close.clicked.connect(self.parent.show_exit)
        # 设置全屏播放页面
        self.dialog = QDialog()
        self.dialog_ui = Ui_DialogPlayMotion()
        self.dialog_ui.setupUi(self.dialog)
        self.dialog_ui.pb_back.clicked.connect(self.exitFullPlay)
        self.dialog_ui.label.hide()
        # labelExit = QLabel("exit")
        # self.dialog_ui.widget.layout().addWidget(labelExit,0,Qt.AlignTop)
        # screen = QGuiApplication::primaryScreen()
        # mm = screen.availableGeometry()
        # screen_width = mm.width()
        # screen_height = mm.height()

    def exitFullPlay(self):
        self.dialog.accept()

    def init_guide_inst(self):
        layout = self.widget.dev_guide.layout()
        item = GuideItem(self.common_cfg)
        layout.addWidget(item)

    def openhotspot(self):

        cmd = 'python3 /usr/local/UBTTools/hotspot/hotspot.py &'
        self.do_cmd(cmd)
        hotspot_set_value = self.common_cfg.get_value_for_key('ubt_yanshee_hotspot_set')
        showcmd = f'wmctrl -a \"{hotspot_set_value}\"'
        self.do_cmd(showcmd)

    def do_cmd(self, cmd):
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        peers = {}
        try:
            child.wait(5)
        except Exception as e:
            child.kill()
            print(f'do cmd = {cmd} error')
        else:
            print(f'do cmd = {cmd} success')

    def init_device(self):
        # self.widget.dev_tit.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_step_one'))

        self.widget.dev_tit.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel()
        # icon.setFixedSize(36, 36)
        # icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(QPixmap(R.imgs_ic_step1))
        layout.addWidget(icon, 0)

        txt = QLabel()
        txt.setContentsMargins(0, 8, 0, 0)
        # txt.setText("<div style='font-size:18px;padding:80px;'><span>将一个或多个Yanshee接入AI box的</span> <a style='color:orange' href=\"热点\">热点</a></div>")
        txt.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_step_one'))
        # txt.setText("<h4 ><i>将一个或多个Yanshee接入AI box的</i> <a href=\"热点\">热点</a></h4>")
        txt.setObjectName("dev_title")
        txt.linkActivated.connect(self.openhotspot)
        # txt.setAlignment(Qt.AlignCenter)
        layout.addWidget(txt, 1)
        self.widget.dev_tit.setLayout(layout)

        self.init_device_list()

    def init_device_list(self):
        list_widget = self.widget.dev_list
        list_widget.setFlow(QListWidget.LeftToRight)
        # list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget.setStyleSheet('background-color:#00000000;')

        for goods in range(8):
            widget = DeviceItem()

            item = QListWidgetItem()
            # item.setFlags(~Qt.ItemIsEnabled)
            item.setFlags(Qt.ItemIsUserCheckable)
            item.setSizeHint(QSize(88, 80))
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)
            self.widget_device_list.append(widget)

    def init_motion(self):
        # self.widget.mot_tit.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_step_two'))

        self.widget.mot_tit.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignVCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel()
        # icon.setFixedSize(36, 36)
        # icon.setAlignment(Qt.AlignLeft)
        icon.setPixmap(QPixmap(R.imgs_ic_step2))
        layout.addWidget(icon, 0)

        txt = QLabel()
        txt.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_step_two'))
        txt.setObjectName("mot_title")
        # txt.setAlignment(Qt.AlignVCenter)
        layout.addWidget(txt, 1)
        self.widget.mot_tit.setLayout(layout)

        self.init_def_icon()
        self.init_camera_mask()
        self.add_motion_ope_btn()
        self.add_motion_reset_btn()

    def init_def_icon(self):
        self.widget.mot_icon.setPixmap(QPixmap(R.imgs_img_robot_default))
        self.widget.mot_txt.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_text'))

        label_load_icon = RotateIcon(R.imgs_img_loading, 44, 44)
        label_load_icon.setParent(self.widget.load_icon)
        self.widget.load_txt.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_loading'))
        self.widget.mot_load.hide()

        label_title_icon = RotateIcon(R.imgs_img_loading, 28, 28)
        label_title_icon.setParent(self.widget.mot_tit_icon)

        self.widget.mot_robot.setPixmap(QPixmap(R.imgs_img_robot_mask))
        self.widget.mot_title.setText(
            self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_title').replace("\\n", "\n"))

    def init_camera_mask(self):
        mask = QLabel(self.widget.camera)
        pix = QPixmap(R.imgs_ic_rc_camera)
        mask.setPixmap(pix)
        self.widget.camera.setFixedSize(640, 480)

    def add_motion_ope_btn(self):
        self.initial_btn = CommonBtn(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_initial'))
        self.initial_btn.clicked.connect(self.operate)
        self.widget.mot_oper.layout().addWidget(self.initial_btn, 0, Qt.AlignRight)
        self.initial_btn.set_click_enable(False)

    def add_motion_reset_btn(self):
        self.reset_btn = CommonBtn(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_reset'), style=3)
        self.reset_btn.clicked.connect(self.reset)
        self.widget.mot_reset.layout().addWidget(self.reset_btn, 0, Qt.AlignRight)
        self.reset_btn.set_click_enable(True)

    def reset(self):
        self.reset_btn.set_click_enable(False)
        self.enter_btn.set_click_enable(False)
        self.widget.mot_initial.hide()
        self.start_timer()

    def operate(self):
        self.initial_btn.set_click_enable(False)
        self.show_load()
        self.initial()
        # self.do_send_stop()
        # self.widget.motion_stack.setCurrentIndex(1)

    def add_enter_btn(self, layout):
        self.enter_btn = CommonBtn(self.common_cfg.get_value_for_key('ubt_yanshee_pose_full_screen_demo'),
                                   R.imgs_ic_full_screen, 2)
        self.enter_btn.clicked.connect(self.enter)
        layout.addWidget(self.enter_btn, 0, Qt.AlignRight)
        self.enter_btn.set_click_enable(False)

    def enter(self):
        self.signal_show_full.emit()

    def setSingal(self, initial, reset, do_send_stop, do_send_start1, do_send_start2, show_devices_loss_dialog):
        self.initial = initial
        self.reset = reset

        self.do_send_stop = do_send_stop
        self.do_send_start1 = do_send_start1
        self.do_send_start2 = do_send_start2
        self.show_devices_loss_dialog = show_devices_loss_dialog

    def update_device_list(self, devices):
        if len(devices) == 0:
            if len(self.latest_devices) == 0:
                pass
            else:
                self.latest_devices.clear()
                self.show_devices_loss_dialog()
                self.initial_btn.set_click_enable(False)
                for item in self.widget_device_list:
                    item.show_default()
        else:
            if not self.is_loading:
                self.initial_btn.set_click_enable(True)
            self.latest_devices.clear()
            for widget, name in zip(self.widget_device_list, devices):
                self.latest_devices.append(widget)
                widget.update_widget(name)
            for item in list(set(self.widget_device_list) - set(self.latest_devices)):
                item.show_default()

    def start_timer(self):
        self.do_send_stop()
        self.widget.mot_initial.hide()
        self.count = 5
        self.widget.mot_count.setText(str(self.count))
        self.widget.mot_load.hide()
        self.widget.motion_stack.setCurrentIndex(1)

        self.widget.mot_title.show()
        self.widget.mot_tit_icon.hide()
        self.widget.mot_title.setText(
            self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_title').replace("\\n", "\n"))

        # self.timer.setInterval(2000)
        # self.timer.timeout.connect(self.show_count)
        self.timer.start(1000)

    def show_count(self):
        import time
        print("show_count @@@@@@@@@@", self.count, time.time())
        if self.count <= 0:
            self.timer.stop()
            self.widget.mot_count.setText('')
            self.show_initial()
            self.do_send_start2()
        else:
            self.count -= 1
            self.widget.mot_count.setText(str(self.count))
            self.do_send_start1()

    def show_initial(self):
        # self.widget.mot_initial.show()
        # self.widget.mot_initial.setStyleSheet("background-color: rgba(0, 0, 0, 255);")
        # layout = self.widget.mot_initial.layout()
        # for i in range(layout.count()):
        #     layout.itemAt(i).widget().deleteLater()
        # label_empty_icon = RotateIcon(R.imgs_img_loading, 50, 50)
        # label_empty_icon.setStyleSheet('margin-bottom:10px;background-color:#00000000;')
        # layout.addWidget(label_empty_icon, 3, Qt.AlignHCenter | Qt.AlignBottom)
        #
        # label_empty_txt = QLabel(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_initialing'))
        # label_empty_txt.setStyleSheet(
        #     'font-family: Source Han Sans CN;font-weight: bold;font-size: 16px;margin-top:10px;'
        #     'color: #FFFFFF;text-align: center;line-height: 20px;background-color:#00000000;')
        # layout.addWidget(label_empty_txt, 2, Qt.AlignHCenter | Qt.AlignTop)
        # self.widget.mot_initial.show()

        self.widget.mot_tit_icon.show()
        self.widget.mot_title.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_initialing'))

        self.count_last = 5
        self.ftimer = QTimer()
        self.ftimer.setInterval(1000)
        # self.ftimer.setSingleShot(True)
        # self.ftimer.timeout.connect(self.show_initial_finish)
        self.ftimer.timeout.connect(self.xxx)
        self.ftimer.start()

    def xxx(self):
        if self.count_last <= 0:
            self.ftimer.stop()
            self.show_initial_finish()
        else:
            self.count_last -= 1
            self.do_send_start2()

    def stopTimer(self):
        print("stop Timer do @@@@@@@@@@")
        if self.timer.isActive():
            self.timer.stop()
            return True
        else:
            return False

    def show_initial_finish(self):
        self.enter_btn.set_click_enable(True)
        self.reset_btn.set_click_enable(True)
        self.widget.mot_initial.show()
        self.widget.mot_title.hide()
        self.widget.mot_tit_icon.hide()

        self.widget.ini_icon.setPixmap(QPixmap(R.imgs_ic_successful))
        self.widget.ini_result.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_initial_finish'))
        self.widget.ini_tip.setText(self.common_cfg.get_value_for_key('ubt_yanshee_pose_motion_initial_tip'))

        self.ftimer = QTimer()
        self.ftimer.setInterval(2000)
        self.ftimer.setSingleShot(True)
        self.ftimer.timeout.connect(self.dismiss_initial_finish)
        self.ftimer.start()

    def dismiss_initial_finish(self):
        self.widget.mot_initial.hide()
        self.is_loading = False

    def show_load(self):
        self.is_loading = True
        self.widget.mot_load.show()

    def eventFilter(self, ob: QtCore.QObject, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.Wheel:
            return True
        return False
