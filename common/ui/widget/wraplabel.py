import sys
from PyQt5 import QtWidgets, QtGui


class AutoScaleQLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kargs):
        super(AutoScaleQLabel, self).__init__(*args, **kargs)

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored,
                                                 QtWidgets.QSizePolicy.Ignored))

        self.setMinSize(14)

    def setMinSize(self, minfs):

        f = self.font()
        f.setPixelSize(minfs)
        br = QtGui.QFontMetrics(f).boundingRect(self.text())

        self.setMinimumSize(br.width(), br.height())

    def resizeEvent(self, event):
        super(AutoScaleQLabel, self).resizeEvent(event)

        if not self.text():
            return

        # --- fetch current parameters ----

        f = self.font()
        cr = self.contentsRect()

        # --- find the font size that fits the contentsRect ---

        fs = 1
        while True:

            f.setPixelSize(fs)
            br = QtGui.QFontMetrics(f).boundingRect(self.text())

            if br.height() <= cr.height() and br.width() <= cr.width():
                fs += 1
            else:
                f.setPixelSize(max(fs - 1, 1))  # backtrack
                break

                # --- update font size ---

        self.setFont(f)


class myApplication(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        # ---- Prepare a Layout ----

        grid = QtWidgets.QGridLayout()

        for i in range(3):
            grid.addWidget(AutoScaleQLabel('some text'), i, 0)
            grid.setRowStretch(i, i + 1)
            grid.setRowMinimumHeight(i, 25)

        self.setLayout(grid)
        self.resize(500, 300)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    instance = myApplication()
    instance.show()

    sys.exit(app.exec_())
