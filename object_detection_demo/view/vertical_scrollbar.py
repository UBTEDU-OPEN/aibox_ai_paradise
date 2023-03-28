from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QScrollBar, QStyleOptionSlider


class UbtVerticalScrollBar(QScrollBar):
    def __init__(self, *args, **kwargs):
        QScrollBar.__init__(self, *args, **kwargs)
        self.baseSheet = '''
            QScrollBar {{
                border: none;
                width: 6px;
                margin: 0px 0 0px 0;
                background: #00123456;
            }}
                
            QScrollBar::handle:vertical {{ 
                border-image: url("resource/images/img_scrollbar.png");
                border-radius: 3px;
                min-height: 166px;
            }}

            QScrollBar::add-line:vertical {{
                border: none;
                background: none ;
                height: 0px;
            }}

            QScrollBar::sub-line:vertical {{
                border: none;
                background: none ;
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical {{
                border: none;
                background: transparent ;
                height: 0px;
            }}

            QScrollBar::sub-page:vertical {{
                border: none;
                background: transparent ;
                height: 0px;
            }}

            '''
        self.arrowNormal = '''
                border: none;
                background: none ;
                height: 0px;
            '''
        self.arrowPressed = '''
                border: 5px solid #00000000;
            '''
        self.setStyleSheet(self.baseSheet.format(
            upArrow=self.arrowNormal,
            downArrow=self.arrowNormal,
            leftArrow=self.arrowNormal,
            rightArrow=self.arrowNormal))

    def mousePressEvent(self, event):
        QScrollBar.mousePressEvent(self, event)
        opt = QStyleOptionSlider()
        opt.initFrom(self)

        subControl = self.style().hitTestComplexControl(self.style().CC_ScrollBar, opt, event.pos(), self)
        if subControl == self.style().SC_ScrollBarAddLine:
            if self.orientation() == QtCore.Qt.Vertical:
                downArrow = self.arrowPressed
                upArrow = leftArrow = rightArrow = self.arrowNormal
            else:
                rightArrow = self.arrowPressed
                upArrow = downArrow = leftArrow = self.arrowNormal
        elif subControl == self.style().SC_ScrollBarSubLine:
            if self.orientation() == QtCore.Qt.Vertical:
                upArrow = self.arrowPressed
                downArrow = leftArrow = rightArrow = self.arrowNormal
            else:
                leftArrow = self.arrowPressed
                rightArrow = upArrow = downArrow = self.arrowNormal
        self.setStyleSheet(
            self.baseSheet.format(upArrow=upArrow, downArrow=downArrow, leftArrow=leftArrow, rightArrow=rightArrow))

    def mouseReleaseEvent(self, event):
        QtWidgets.QScrollBar.mouseReleaseEvent(self, event)
        self.setStyleSheet(self.baseSheet.format(
            upArrow=self.arrowNormal,
            downArrow=self.arrowNormal,
            leftArrow=self.arrowNormal,
            rightArrow=self.arrowNormal))
