# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QStyle,QStyleOption
from PyQt5.QtCore import QPropertyAnimation,QTimer

from PyQt5.QtGui import QFont,QPainter,QColor,QBrush,QGuiApplication,QPalette,QBrush

# import UBTQDevice

class UBTQToastTools(QWidget):
    def __init__(self,parent=None):
        super(UBTQToastTools, self).__init__(parent)


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #self.setStyleSheet("UBTQToastTools#toast_widget{background:rgba(20, 26, 48,153);}")

        self.alert_widget = QLabel(self)
        self.alert_widget.setFixedWidth(440)
        self.alert_widget.setFixedHeight(190)
        self.alert_widget.setObjectName("alert_widget")
        
        self.alert_widget.setStyleSheet("QWidget#alert_widget{background:rgba(0, 0, 0,153);border-radius: 8px;border-image: url(./resources/toast_mask.png)}")
        #self.alert_widget.setStyleSheet("QWidget#alert_widget{border-image: url(./resources/toast_mask.png)}")

        self.text_label = QLabel(self.alert_widget)
        self.text_label.adjustSize()
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        title_font = QFont("Source Han Sans CN")
        title_font.setPixelSize(28)
        self.text_label.setFont(title_font)
        self.text_label.setObjectName("text_label")

        self.text_label.setStyleSheet("QLabel{color:#ffffff;background-color:transparent;}")

    def showAnimation(self, timeout):

        self.animation = QPropertyAnimation(self,  b'windowOpacity')
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        self.show()
        QTimer.singleShot(timeout, self.closeWindow)

    def closeWindow(self):
        self.animation = QPropertyAnimation(self,  b'windowOpacity')
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

        self.animation.finished.connect(self.close)

    def paintEvent(self, event):
        self.alert_widget.move((self.width() - self.alert_widget.width()) / 2, (self.height() - self.alert_widget.height()) / 2);
        self.text_label.setGeometry(0, 0, self.alert_widget.width(), self.alert_widget.height())
        self.text_label.move((self.alert_widget.size().width() - self.text_label.width()) / 2, (self.alert_widget.size().height() - self.text_label.height()) / 2);
        
        painter = QPainter()
        painter.begin(self)
        #bg_color = QColor(0,0,0)
        #bg_color.setAlpha(0.2)
        #painter.setPen(QtCore.Qt.NoPen)
        #painter.setBrush(QBrush(bg_color,QtCore.Qt.SolidPattern))
        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        #painter.drawRect(0, 0, self.width(), self.height());
        painter.end();

    @classmethod
    def showTip(cls, message, parent):
        pScreen = QGuiApplication.primaryScreen()
        toast = UBTQToastTools(parent)
        #toast.setGeometry(0, 0, pScreen.size().width(), pScreen.size().height())
        toast.setObjectName("toast_widget")
        #toast.setStyleSheet("UBTQToastTools#toast_widget{background-color:transparent;}")
        #toast.setStyleSheet("UBTQToastTools#toast_widget{background-color:rgba(20, 26, 48,153);}")
        toast.setStyleSheet("QWidget#toast_widget{border-image: url(./resources/toast_mask.png);background-color:rgba(20, 26, 48,102);border-radius: 8px}")
        #toast.setWindowFlags(toast.windowFlags() | QtCore.Qt.X11BypassWindowManagerHint)
        toast.setWindowFlags(toast.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        toast.activateWindow()
        #toast.setWindowOpacity(0.2)
        toast.text_label.setText(message)
        
        toast.text_label.adjustSize()
        toast.adjustSize()

        toast.move((pScreen.size().width() - toast.width()) / 2, (pScreen.size().height() - toast.height()) / 2);
        toast.showAnimation(2000)



