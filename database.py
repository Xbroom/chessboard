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
        return 12

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, self.games[row])

    def data(self, index, role=Qt.DisplayRole):
        game = self.games[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return game["White"]
            elif index.column() == 1:
                if "WhiteElo" in game:
                    return game["WhiteElo"]
            elif index.column() == 2:
                return game["Black"]
            elif index.column() == 3:
                if "BlackElo" in game:
                    return game["BlackElo"]
            elif index.column() == 4:
                if game["Result"] == "1/2-1/2":
                    return u"½-½"
                else:
                    return game["Result"]
            elif index.column() == 5:
                if "PlyCount" in game:
                    return game["PlyCount"]
            elif index.column() == 6:
                if "ECO" in game:
                    return game["ECO"]
            elif index.column() == 7:
                return game["Event"]
            elif index.column() == 8:
                return game["Date"]
            elif index.column() == 9:
                if "Time" in game:
                    return game["Time"]
            elif index.column() == 10:
                return game["Site"]
            elif index.column() == 11:
                return game["Round"]
        elif role == Qt.ToolTipRole:
            if index.column() == 6:
                if "ECO" in game and game["ECO"] in self.ecoLookup:
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
                    return _("Time")
                elif section == 10:
                    return _("Site")
                elif section == 11:
                    return _("Round")
            else:
                return section + 1


class DatabaseMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(DatabaseMainWindow, self).__init__(parent)
        self.initUi()
        self.initActions()
        self.initMenu()

    def initUi(self):
        self.table = QTableView()
        self.setCentralWidget(self.table)

        self.setWindowTitle(_("New database"))

    def initActions(self):
        self.openAction = QAction(_("&Open..."), self)
        self.openAction.setShortcuts(QKeySequence.Open)
        self.openAction.setStatusTip(_("Open an existing database"))
        self.openAction.triggered.connect(self.onOpenAction)

    def initMenu(self):
        fileMenu = self.menuBar().addMenu(_("&File"))
        fileMenu.addAction(self.openAction)

    def loadFile(self, filename):
        reader = chess.PgnDatabaseReader(filename)
        reader.read_all()
        self.table.setModel(GameTableModel(reader.games))

    def onOpenAction(self):
        filename, pattern = QFileDialog.getOpenFileName(self)
        if filename:
            self.loadFile(filename)


if __name__ == "__main__":
    import chessboard
    import sys
    app = chessboard.ChessboardApplication(sys.argv)

    window = DatabaseMainWindow()
    window.show()

    app.exec_()
