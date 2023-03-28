# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QListView, QLabel, QPushButton, \
    QStackedWidget, QStyle, QStyleOption
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont,QPainter
from PyQt5.QtCore import pyqtSignal as Signal

from enum import Enum

from face_recognize_demo.com import ubt_device
from face_recognize_demo.sample.ubt_listview_model import MyListModel
from face_recognize_demo.sample.sample_item_delegate import SampleItemDelegate, ItemData

k_width = 680

class Type(Enum):
    COMMON_ITEM = 1
    BUTTON_ITEM = 2

class FaceSampleList(QWidget):

    # signals
    button_item_clicked = Signal()
    delete_item_clicked = Signal(str)
    clear_item_clicked = Signal()

    def __del__(self):
        print("已经释放smaple")

    def paintEvent(self, event):
        self.clear_btn.setGeometry(k_width * ubt_device.scale_width - 30 - 30, 15, 30, 30)
        self.stack.setGeometry(0, 70, k_width * ubt_device.scale_width, 475 * ubt_device.scale_height)

        painter = QPainter()
        painter.begin(self)

        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        # painter.drawRect(0, 0, self.width(), self.height());
        painter.end();

    def configure_string(self,conf):
        if conf is not None:
            self.tip_label.setText(conf.get_value_for_key("k_zero_smaple_tip"))
            self.sample_label.setText(conf.get_value_for_key("k_face_sample"))
            self.sample_label.adjustSize()
            self.sample_label.setGeometry(30, 0, self.sample_label.width(), 60)
            self.count_label.setGeometry(self.sample_label.width() + 30 + 10, 27, 200, 20)
            self.add_btn.setText(conf.get_value_for_key("k_input_face"))


    def __init__(self, parent, configure_object, addSampleEvent=None):
        super(FaceSampleList, self).__init__(parent)

        self.configure = configure_object

        self.list_data = []

        self.addSampleEvent = addSampleEvent

        self.setObjectName("sample")

        self.setStyleSheet("QWidget#sample{border-image: url(:/resource/sample_bg.png)}")

        self.sample_label = QLabel(self)
        self.sample_label.setGeometry(30, 0, 200, 60)

        smaple_font = QFont("Source Han Sans CN")
        smaple_font.setWeight(QFont.Bold)
        smaple_font.setPixelSize(24)
        self.sample_label.setFont(smaple_font)
        self.sample_label.setObjectName("sample_title_label")
        self.sample_label.setStyleSheet("QLabel#sample_title_label{color:#ffffff;}")
        # self.sample_label.adjustSize()

        # 显示计数
        self.count_label = QLabel(self)
        # self.count_label.setGeometry(160, 27, 112, 20)
        self.count_label.setAlignment(QtCore.Qt.AlignLeft)
        self.count_label.setStyleSheet("QLabel{opacity: 0.5; font-family: SourceHanSansCN; font-size: 20px; \
            color:#FFFFFF; line-height:36px;}")

        self.clear_btn = QPushButton("", self)

        self.clear_btn.clicked.connect(self.clear_item_clicked)
        self.clear_btn.setStyleSheet("QPushButton{border-image: url(:/resource/ic_delete.png)}")

        self.stack = QStackedWidget(self)

        self.sample_list_widget = self._sample_list()
        self.stack.addWidget(self.sample_list_widget)
        self.stack.addWidget(self.empty_list())

        # 添加列表中的按钮
        add_button_icon = QtGui.QPixmap(":/resource/ic_add_big.png")
        self.add_item(add_button_icon, configure_object.get_value_for_key('k_input_face'), 2)

        self.set_status_for_empty_list()

        self.configure_string(configure_object)

    def empty_list(self):
        empty = QWidget()
        empty.setGeometry(0, 0, k_width * ubt_device.scale_width, 475 * ubt_device.scale_height)

        width = empty.width()
        height = empty.height()

        icon_label = QLabel(empty)
        icon_label.setGeometry((width - 110 * ubt_device.scale_width) * 0.5, 120, 110 * ubt_device.scale_width, 80)
        icon_label.setPixmap(QtGui.QPixmap(":/resource/empty_icon.png"))

        self.tip_label = QLabel(empty)
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.setGeometry((width - 240 * ubt_device.scale_width) * 0.5, 230, 240 * ubt_device.scale_width, 20)

        tip_font = QFont("Source Han Sans CN")
        tip_font.setPixelSize(16)
        tip_font.setWeight(QFont.Normal)
        self.tip_label.setFont(tip_font)
        self.tip_label.setObjectName("tip_label")
        self.tip_label.setStyleSheet("QLabel#tip_label{color:#ffffff;}")

        self.add_btn = QPushButton(empty)
        self.add_btn.setGeometry((width - 180 * ubt_device.scale_width) * 0.5, 300, 180 * ubt_device.scale_width, 50)
        self.add_btn.setObjectName("add_sample_button")

        add_btn_font = QFont("Source Han Sans CN")
        add_btn_font.setWeight(QFont.Bold)
        add_btn_font.setPixelSize(20)
        self.add_btn.setFont(add_btn_font)
        self.add_btn.setIcon(QtGui.QIcon("../resource/ic_add_small.png"))
        self.add_btn.setStyleSheet("QPushButton#add_sample_button{background-color:#9189FE;border-radius:8px;color:#ffffff;}")
        self.add_btn.clicked.connect(self.addSample)

        return empty

    def _sample_list(self):
        delegate = SampleItemDelegate(self,delete_clourse=self.delete_test, add_clourse=self.addSample)

        self.model = MyListModel(self.list_data, self)

        self.list_view = QListView()
        self.list_view.setGeometry(0, 0, k_width * ubt_device.scale_width, 475 * ubt_device.scale_height)
        self.list_view.setSpacing(18.5 * ubt_device.scale_width)
        self.list_view.setModel(self.model)
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setItemDelegate(delegate)
        self.list_view.setMouseTracking(True)

        self.list_view.setStyleSheet("QWidget{background-color:transparent}")

        return self.list_view

    def delete_test(self,index):
        data = self.model.index_data(index)
        self.model.deleteItem(index)
        self.delete_item_clicked.emit(data.name)

    def addSample(self):
        if self.addSampleEvent != None:
            self.addSampleEvent()

    def add_item(self, image, name, item_type=1):
        """

        :param image: (QPixmape) item 图标
        :param name: (string) item 名字
        :param item_type: (SamepleItem._Type) item类型, 普通或者按键
        """
        item = ItemData(icon=image, name=name, type=item_type)
        self.model.addItem(item)
        self._update_sample_count()

    def delete_item(self, name):
        """

        :param name: (str) item name
        """
        # item_count = self.model.rowCount()
        # if 1 == item_count:
        #     return
        self._update_sample_count()

    def delete_all_items(self):
        """

        :return:
        """
        self.model.clearItems()

        self._update_sample_count()

    def get_item_count(self):
        """

        :return:  (int) item count
        """
        return self.model.rowCount()

    def set_status_for_empty_list(self):
        """

        :return:
        """
        self.stack.setCurrentIndex(1)
        self.clear_btn.setDisabled(True)

    def set_status_for_item_added(self):
        """

        :return:
        """
        self.stack.setCurrentIndex(0)
        self.clear_btn.setDisabled(False)

    def _update_sample_count(self):
        """ 更新样本记录个数

        """
        # self.sample_list_widget.setCurrentRow(0)
        # 减1,除去添加按钮
        count = self.get_item_count() - 1
        text = str(count) + " " + self.configure.get_value_for_key('k_count')
        self.count_label.setText(text)
        self.count_label.adjustSize()
        # self.sample_list_widget.update()

