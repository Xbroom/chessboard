#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *

import chess


class Board(QWidget):

    def __init__(self, parent=None):
        super(Board, self).__init__(parent)
        self.margin = 0.1
        self.padding = 0.06
        self.showCoordinates = True
        self.lightSquareColor = QColor(255, 255, 255)
        self.darkSquareColor = QColor(100, 100, 255)
        self.borderColor = QColor(100, 100, 200)
        self.shadowWidth = 2
        self.rotation = 0
        self.backgroundPixmap = QPixmap("resources/background.png")

        self.draggedSquare = None
        self.dragPosition = None

        self.position = chess.Position()
        self.position.make_move(chess.Move.from_uci("e2e4"))

        # Load piece set.
        self.pieceRenderers = dict()
        for symbol in "PNBRQKpnbrqk":
            piece = chess.Piece(symbol)
            self.pieceRenderers[piece] = QSvgRenderer("resources/classic-pieces/%s-%s.svg" % (piece.full_color, piece.full_type))

    def mousePressEvent(self, e):
        self.dragPosition = e.pos()
        square = self.squareAt(e.pos())
        if self.canDragSquare(square):
            self.draggedSquare = square

    def mouseMoveEvent(self, e):
        if self.draggedSquare:
            self.dragPosition = e.pos()
            self.repaint()

    def mouseReleaseEvent(self, e):
        if self.draggedSquare:
            dropSquare = self.squareAt(e.pos())
            if dropSquare == self.draggedSquare:
                self.onSquareClicked(self.draggedSquare)
            elif dropSquare:
                move = self.moveFromDragDrop(self.draggedSquare, dropSquare)
                if move:
                    self.position.make_move(move)
            self.draggedSquare = None
            self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # Light shines from upper left.
        if math.cos(math.radians(self.rotation)) >= 0:
            lightBorderColor = self.borderColor.lighter()
            darkBorderColor = self.borderColor.darker()
        else:
            lightBorderColor = self.borderColor.darker()
            darkBorderColor = self.borderColor.lighter()

        # Draw the background.
        backgroundBrush = QBrush(Qt.red, self.backgroundPixmap)
        backgroundBrush.setStyle(Qt.TexturePattern)
        painter.fillRect(QRect(QPoint(0, 0), self.size()), backgroundBrush)

        # Do the rotation.
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.rotation)

        # Draw the border.
        frameSize = min(self.width(), self.height()) * (1 - self.margin * 2)
        borderSize = min(self.width(), self.height()) * self.padding
        painter.translate(-frameSize / 2, -frameSize / 2)
        painter.fillRect(QRect(0, 0, frameSize, frameSize), self.borderColor)
        painter.setPen(QPen(QBrush(lightBorderColor), self.shadowWidth))
        painter.drawLine(0, 0, 0, frameSize)
        painter.drawLine(0, 0, frameSize, 0)
        painter.setPen(QPen(QBrush(darkBorderColor), self.shadowWidth))
        painter.drawLine(frameSize, 0, frameSize, frameSize)
        painter.drawLine(0, frameSize, frameSize, frameSize)

        # Draw the squares.
        painter.translate(borderSize, borderSize)
        squareSize = (frameSize - 2 * borderSize) / 8.0
        for x in range(0, 8):
            for y in range(0, 8):
                rect = QRect(x * squareSize, y * squareSize, squareSize, squareSize)
                if (x - y) % 2 == 0:
                     painter.fillRect(rect, QBrush(self.lightSquareColor))
                else:
                     painter.fillRect(rect, QBrush(self.darkSquareColor))

        # Draw the inset.
        painter.setPen(QPen(QBrush(darkBorderColor), self.shadowWidth))
        painter.drawLine(0, 0, 0, squareSize * 8)
        painter.drawLine(0, 0, squareSize * 8, 0)
        painter.setPen(QPen(QBrush(lightBorderColor), self.shadowWidth))
        painter.drawLine(squareSize * 8, 0, squareSize * 8, squareSize * 8)
        painter.drawLine(0, squareSize * 8, squareSize * 8, squareSize * 8)

        # Display coordinates.
        if self.showCoordinates:
            painter.setPen(QPen(QBrush(self.borderColor.lighter()), self.shadowWidth))
            coordinateSize = min(borderSize, squareSize)
            font = QFont()
            font.setPixelSize(coordinateSize * 0.6)
            painter.setFont(font)
            for i, rank in enumerate(["8", "7", "6", "5", "4", "3", "2", "1"]):
                pos = QRect(-borderSize, squareSize * i, borderSize, squareSize).center()
                painter.save()
                painter.translate(pos.x(), pos.y())
                painter.rotate(-self.rotation)
                painter.drawText(QRect(-coordinateSize / 2, -coordinateSize / 2, coordinateSize, coordinateSize), Qt.AlignCenter, rank)
                painter.restore()
            for i, file in enumerate(["a", "b", "c", "d", "e", "f", "g", "h"]):
                pos = QRect(squareSize * i, squareSize * 8, squareSize, borderSize).center()
                painter.save()
                painter.translate(pos.x(), pos.y())
                painter.rotate(-self.rotation)
                painter.drawText(QRect(-coordinateSize / 2, -coordinateSize / 2, coordinateSize, coordinateSize), Qt.AlignCenter, file)
                painter.restore()

        # Draw pieces.
        for x in range(0, 8):
            for y in range(0, 8):
                square = chess.Square.from_x_and_y(x, 7 - y)
                piece = self.position[square]
                if piece and square != self.draggedSquare:
                    painter.save()
                    painter.translate((x + 0.5) * squareSize, (y + 0.5) * squareSize)
                    painter.rotate(-self.rotation)
                    self.pieceRenderers[piece].render(painter, QRect(-squareSize / 2, -squareSize / 2, squareSize, squareSize))
                    painter.restore()

        # Draw a floating piece.
        painter.restore()
        if self.draggedSquare:
            piece = self.position[self.draggedSquare]
            if piece:
                painter.save()
                painter.translate(self.dragPosition.x(), self.dragPosition.y())
                painter.rotate(-self.rotation)
                self.pieceRenderers[piece].render(painter, QRect(-squareSize / 2, -squareSize / 2, squareSize, squareSize))
                painter.restore()

        painter.end()

    def squareAt(self, point):
        # Undo the rotation.
        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.rotate(self.rotation)
        logicalPoint = transform.inverted()[0].map(point)

        frameSize = min(self.width(), self.height()) * (1 - self.margin * 2)
        borderSize = min(self.width(), self.height()) * self.padding
        squareSize = (frameSize - 2 * borderSize) / 8.0
        x = int(logicalPoint.x() / squareSize + 4)
        y = 7 - int(logicalPoint.y() / squareSize + 4)
        try:
            return chess.Square.from_x_and_y(x, y)
        except IndexError:
            return None

    def canDragSquare(self, square):
        for move in self.position.get_legal_moves():
            if move.source == square:
                return True
        return False

    def onSquareClicked(self, square):
        pass

    def moveFromDragDrop(self, source, target):
        for move in self.position.get_legal_moves():
            if move.source == source and move.target == target:
                assert not move.promotion # TODO: Allow promotions.
                return move

if __name__ == "__main__":
    app = QApplication(sys.argv)

    board = Board()
    board.show()

    app.exec_()
