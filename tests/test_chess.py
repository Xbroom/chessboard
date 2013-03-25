import unittest
import chess


class PgnDatabaseReaderTestCase(unittest.TestCase):

    def test(self):
        reader = chess.PgnDatabaseReader("resources/games/kasparov-deep-blue-1997.pgn")
        reader.read_all()
        self.assertEqual(len(reader.games), 6)

        second_game = reader.games[1]
        self.assertEqual(second_game["White"], "Deep Blue (Computer)")
        self.assertEqual(second_game["Result"], "1-0")
        self.assertEqual(second_game["ECO"], "C93")
