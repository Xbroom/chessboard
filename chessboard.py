#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PySide.QtCore import *
from PySide.QtGui import *

class Board(QWidget):
    def __init__(self, parent=None):
        super(Board, self).__init__(parent)
        self.backgroundPixmap = QPixmap("resources/background.png")
        self.margin = 10
        self.padding = 10
        self.showCoordinates = True
        self.lightSquareColor = QColor(255, 255, 255)
        self.darkSquareColor = QColor(100, 100, 255)
        self.borderColor = QColor(100, 100, 200)
        self.shadowWidth = 2

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # Draw the background.
        backgroundBrush = QBrush(Qt.red, self.backgroundPixmap)
        backgroundBrush.setStyle(Qt.TexturePattern)
        painter.fillRect(QRect(QPoint(0, 0), self.size()), backgroundBrush)

        # Draw the border.
        painter.translate(self.width() / 2.0, self.height() / 2.0)
        frameSize = min(self.width(), self.height()) - self.margin
        painter.fillRect(QRect(-frameSize / 2, -frameSize / 2, frameSize, frameSize), self.borderColor)
        painter.setPen(QPen(QBrush(self.borderColor.lighter()), self.shadowWidth))
        painter.drawLine(-frameSize / 2, -frameSize / 2, -frameSize / 2, frameSize / 2)
        painter.drawLine(-frameSize / 2, -frameSize / 2, frameSize / 2, -frameSize / 2)
        painter.setPen(QPen(QBrush(self.borderColor.darker()), self.shadowWidth))
        painter.drawLine(frameSize / 2, -frameSize / 2, frameSize / 2, frameSize / 2)
        painter.drawLine(-frameSize / 2, frameSize / 2, frameSize / 2, frameSize / 2)

        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    board = Board()
    board.show()

    app.exec_()