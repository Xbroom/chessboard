import unittest
import chess


class PgnDatabaseReaderTestCase(unittest.TestCase):

    def test(self):
        reader = chess.PgnDatabaseReader("resources/games/kasparov-deep-blue-1997.pgn")
        reader.read_all()
        self.assertEqual(len(reader.games), 6)
