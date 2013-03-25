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


class EcoFileParserTestCase(unittest.TestCase):

    def test(self):
        parser = chess.EcoFileParser()
        parser.tokenize("resources/tiny.eco")
        parser.read_all()

        self.assertEqual(parser.lookup["C00"]["name"], "French")
        self.assertEqual(parser.lookup["E00"]["fen"], "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3")

        position = chess.Position()
        position.make_move(chess.Move.from_uci("e2e4"))
        self.assertEqual(parser.classification[hash(position)]["eco"], "B00")
