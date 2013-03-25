# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *

import chess
import json

class GameTableModel(QAbstractTableModel):
    def __init__(self, games):
        super(GameTableModel, self).__init__()
        self.ecoLookup = json.load(open("dist/eco-lookup.json", "r"))
        self.games = games

    def rowCount(self, parent):
        return len(self.games)

    def columnCount(self, parent):
        return 11

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, self.games[row])

    def data(self, index, role=Qt.DisplayRole):
        game = self.games[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return game["White"]
            elif index.column() == 1:
                return game["WhiteElo"]
            elif index.column() == 2:
                return game["Black"]
            elif index.column() == 3:
                return game["BlackElo"]
            elif index.column() == 4:
                if game["Result"] == "1/2-1/2":
                    return u"½-½"
                else:
                    return game["Result"]
            elif index.column() == 5:
                return game["PlyCount"]
            elif index.column() == 6:
                return game["ECO"]
            elif index.column() == 7:
                return game["Event"]
            elif index.column() == 8:
                return game["Date"]
            elif index.column() == 9:
                return game["Site"]
            elif index.column() == 10:
                return game["Round"]
        elif role == Qt.ToolTipRole:
            if index.column() == 6:
                if game["ECO"] in self.ecoLookup:
                    return self.ecoLookup[game["ECO"]]["name"]
        elif role == Qt.ForegroundRole:
            if index.data(Qt.DisplayRole) == "?":
                return QBrush(Qt.gray)
        elif role == Qt.FontRole:
            font = QFont()
            font.setBold(index.column() <= 4)
            return font

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return _("White")
                elif section == 1:
                    return _("W Elo")
                elif section == 2:
                    return _("Black")
                elif section == 3:
                    return _("B Elo")
                elif section == 4:
                    return _("Result")
                elif section == 5:
                    return _("Moves")
                elif section == 6:
                    return _("ECO")
                elif section == 7:
                    return _("Event")
                elif section == 8:
                    return _("Date")
                elif section == 9:
                    return _("Site")
                elif section == 10:
                    return _("Round")
            else:
                return section + 1


if __name__ == "__main__":
    import chessboard
    import sys
    app = chessboard.ChessboardApplication(sys.argv)

    view = QTableView()
    reader = chess.PgnDatabaseReader("resources/games/kasparov-deep-blue-1997.pgn")
    reader.read_all()
    view.setModel(GameTableModel(reader.games))
    view.show()

    app.exec_()
