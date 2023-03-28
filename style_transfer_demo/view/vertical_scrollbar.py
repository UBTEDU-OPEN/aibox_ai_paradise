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
                background: transparent;
            }}
                
            QScrollBar::handle {{ 
                background: #664F5A7E;
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
