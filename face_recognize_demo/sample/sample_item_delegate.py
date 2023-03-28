from PyQt5.QtCore import Qt, QRect, QEvent, QSize, QTimer
from PyQt5.QtGui import QPen, QPixmap, QFont, QFontMetrics, QCursor
from PyQt5.QtWidgets import QItemDelegate, QStyle

from face_recognize_demo.com import ubt_device
from face_recognize_demo.view.name_tooltip_view import NameTooltip


class ItemData:
    def __init__(self, icon=None,name=None, type=None):
        '''

        :param icon: (QPixmape) 样本图片
        :param name: (str) 名字
        :param type: (int) item类型:1->表示的是样本item; 2->表示添加item
        '''
        self.icon = icon
        self.name = name
        self.item_type = type


class SampleItemDelegate(QItemDelegate):
    def __init__(self, parent=None, *args, add_clourse=None, delete_clourse=None):
        '''

        :param parent:
        :param args:
        :param add_clourse: 响应添加按钮的闭包
        :param delete_clourse: 响应删除按钮的闭包
        '''
        QItemDelegate.__init__(self, parent, *args)
        self.parent = parent
        parent.installEventFilter(self)
        self.delete_rect = None
        self.add_rect = None
        self.item_type = None
        self.text_rect = None
        self.tooltip_owner = ""
        self.tooltip = None
        self.tooltip_timer = QTimer()
        self.tooltip_timer.setSingleShot(True)
        self.tooltip_timer.timeout.connect(self.close_tooltip)
        self.font = QFont("Source Han Sans CN")
        self.font.setWeight(QFont.Bold)
        self.font.setPixelSize(19)
        self.font_metrics = QFontMetrics(self.font)

        self.delete_clourse=delete_clourse
        self.add_clourse = add_clourse

    def paint(self, painter, option, index):
        '''

        :param painter:
        :param option:
        :param index:
        :return:
        '''
        option_topleft = option.rect.topLeft()
        painter.save()

        # set background color
        painter.setPen(QPen(Qt.NoPen))
        # if option.state & QStyle.State_Selected:
        #     painter.setBrush(QBrush(Qt.white))
        # else:
        #     painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        # set text color
        painter.setPen(QPen(Qt.black))
        item_data = index.data(Qt.DisplayRole)
        self.item_type = item_data.item_type

        icon_rect = QRect(option.rect.x(), option.rect.top(), option.rect.width(), 110 * ubt_device.scale_height)
        self.add_rect = icon_rect
        painter.drawPixmap(icon_rect,item_data.icon)

        name_rect = QRect(option.rect.x(),(option.rect.top()+110) * ubt_device.scale_height,option.rect.width(),35)
        self.text_rect = name_rect
        # name_rect = option.rect
        name_rect.setTop(icon_rect.bottom())
        painter.setPen(QPen(Qt.white))
        painter.setFont(self.font)
        text = self.font_metrics.elidedText(item_data.name, Qt.ElideMiddle, option.rect.width())
        # painter.drawText(name_rect, Qt.AlignCenter, item_data.name)
        painter.drawText(name_rect, Qt.AlignCenter, text)

        if item_data.item_type == 1:
            hover_in = False
            if option.state & QStyle.State_MouseOver:
                # print(index.row())
                if self.tooltip_owner != text:
                    self.tooltip_owner = text
                    hover_in = True

                icon_rect = QRect(option.rect.x() + 40 * ubt_device.scale_width,
                                  (option.rect.top() + 40) * ubt_device.scale_height, 30, 30)
                self.delete_rect = icon_rect
                painter.drawPixmap(icon_rect, QPixmap(":/resource/ic_delete.png"))

            if hover_in:
                if self.tooltip_timer.isActive():
                    self.tooltip_timer.stop()
                    self.tooltip.close()

                if text != item_data.name:
                    self.tooltip = NameTooltip(item_data.name, self.parent)
                    self.tooltip.move(name_rect.center().x() - self.tooltip.width()/2,
                                      option.rect.bottom())
                    self.tooltip.show()
                    self.tooltip_timer.start(1000)

            if self.tooltip_timer.isActive():
                self.tooltip_timer.start(1000)



        painter.restore()

    def sizeHint(self, QStyleOptionViewItem, QModelIndex):
        '''

        :param QStyleOptionViewItem:
        :param QModelIndex:
        :return:
        '''
        return QSize(110 * ubt_device.scale_width,145 * ubt_device.scale_height)

    def editorEvent(self, event: QEvent, model, option, index):
        '''

        :param event:
        :param model:
        :param option:
        :param index:
        :return:
        '''
        if event.type() == QEvent.MouseButtonPress:

            if self.item_type == 1:
                if self.delete_rect.contains(event.pos()):
                    self.delete_clourse(index.row())
                    self.close_tooltip()
            elif self.item_type == 2:
                if self.add_rect.contains(event.pos()):
                    self.add_clourse()

        return False

    def close_tooltip(self):
        if self.tooltip_timer.isActive():
            self.tooltip_timer.stop()

        try:
            self.tooltip.close()
        except Exception:
            pass
        self.tooltip_owner = ""

