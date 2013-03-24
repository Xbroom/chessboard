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
        self.rotation = 20

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # Draw the background.
        backgroundBrush = QBrush(Qt.red, self.backgroundPixmap)
        backgroundBrush.setStyle(Qt.TexturePattern)
        painter.fillRect(QRect(QPoint(0, 0), self.size()), backgroundBrush)

        # Do the rotation.
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.rotation)

        # Draw the border.
        frameSize = min(self.width(), self.height()) - self.margin * 2
        painter.translate(-frameSize / 2, -frameSize / 2)
        painter.fillRect(QRect(0, 0, frameSize, frameSize), self.borderColor)
        painter.setPen(QPen(QBrush(self.borderColor.lighter()), self.shadowWidth))
        painter.drawLine(0, 0, 0, frameSize)
        painter.drawLine(0, 0, frameSize, 0)
        painter.setPen(QPen(QBrush(self.borderColor.darker()), self.shadowWidth))
        painter.drawLine(frameSize, 0, frameSize, frameSize)
        painter.drawLine(0, frameSize, frameSize, frameSize)

        # Draw the squares.
        painter.translate(self.margin, self.margin)
        squareSize = (frameSize - 2 * self.padding) / 8.0
        for x in range(0, 8):
            for y in range(0, 8):
                rect = QRect(x * squareSize, y * squareSize, squareSize, squareSize)
                if (x - y) % 2 == 0:
                     painter.fillRect(rect, QBrush(self.lightSquareColor))
                else:
                     painter.fillRect(rect, QBrush(self.darkSquareColor))

        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    board = Board()
    board.show()

    app.exec_()