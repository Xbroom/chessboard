#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PySide.QtCore import *
from PySide.QtGui import *

class Board(QWidget):
    def __init__(self, parent=None):
        super(Board, self).__init__(parent)
        self.backgroundPixmap = QPixmap("resources/background.png")

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        backgroundBrush = QBrush(Qt.red, self.backgroundPixmap)
        backgroundBrush.setStyle(Qt.TexturePattern)
        painter.fillRect(QRect(QPoint(0, 0), self.size()), backgroundBrush)
        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    board = Board()
    board.show()

    app.exec_()