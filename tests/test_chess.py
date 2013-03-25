import unittest
import chess
import random


class GameHeaderBagTestCase(unittest.TestCase):
    """Tests for the GameHeaderBag class."""

    def test_contains(self):
        """Tests checking if a key is in the bag."""
        bag = chess.GameHeaderBag()
        self.assertTrue("Site" in bag)
        self.assertTrue("Round" in bag)
        self.assertFalse("PlyCount" in bag)
        self.assertFalse("FEN" in bag)
        self.assertFalse("SetUp" in bag)

        bag["FEN"] = chess.START_FEN
        self.assertFalse("FEN" in bag)

        bag["FEN"] = "8/8/8/1kr5/4KR2/5N2/8/8 w - - 0 1"
        self.assertTrue("FEN" in bag)
        self.assertTrue("SetUp" in bag)

        bag["UnknownHeader"] = "foo"
        self.assertTrue("UnknownHeader" in bag)
        self.assertFalse("OtherHeader" in bag)

    def test_iterating(self):
        """Tests iterating over a bag."""
        bag = chess.GameHeaderBag()
        bag["Lorem"] = "Ipsum"
        bag["Annotator"] = "Awesome annotator"

        order = []
        for key in bag:
            order.append(key)

        self.assertEqual(order[0], "Event")
        self.assertEqual(order[6], "Result")
        self.assertEqual(order[7], "Annotator")
        self.assertEqual(order[8], "Lorem")


class MoveTestCase(unittest.TestCase):
    """Tests the Move class."""

    def test_equality(self):
        """Tests the custom equality behaviour of the move class."""
        a = chess.Move(chess.Square("a1"), chess.Square("a2"))
        b = chess.Move(chess.Square("a1"), chess.Square("a2"))
        c = chess.Move(chess.Square("h7"), chess.Square("h8"), "b")
        d = chess.Move(chess.Square("h7"), chess.Square("h8"))

        self.assertEqual(a, b)
        self.assertEqual(b, a)

        self.assertNotEqual(a, c)
        self.assertNotEqual(c, d)
        self.assertNotEqual(b, d)

    def test_uci_parsing(self):
        """Tests the UCI move parsing."""
        self.assertEqual(chess.Move.from_uci('b5c7').uci, 'b5c7')
        self.assertEqual(chess.Move.from_uci('e7e8q').uci, 'e7e8q')


class PieceTestCase(unittest.TestCase):
    """Tests the Piece class."""

    def test_equality(self):
        """Tests the overriden equality behavior of the Piece class."""
        a = chess.Piece.from_color_and_type(type='b', color='w')
        b = chess.Piece.from_color_and_type(type='k', color='b')
        c = chess.Piece.from_color_and_type(type='k', color='w')
        d = chess.Piece.from_color_and_type(type='b', color='w')

        self.assertEqual(a, d)
        self.assertEqual(d, a)

        self.assertEqual(repr(a), repr(d))

        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)
        self.assertNotEqual(b, d)
        self.assertNotEqual(a, c)

        self.assertNotEqual(a, None)
        self.assertFalse(a == None)

    def test_simple_properties(self):
        """Tests simple properties."""
        white_knight = chess.Piece('N')

        self.assertEqual(white_knight.color, 'w')
        self.assertEqual(white_knight.full_color, 'white')

        self.assertEqual(white_knight.type, 'n')
        self.assertEqual(white_knight.full_type, 'knight')


class PositionTestCase(unittest.TestCase):
    """Tests the position class."""

    def test_default_position(self):
        """Tests the default position."""
        pos = chess.Position()
        self.assertEqual(pos[chess.Square('b1')], chess.Piece('N'))
        self.assertEqual(pos.fen, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(pos.turn, "w")

    def test_scholars_mate(self):
        """Tests the scholars mate."""
        pos = chess.Position()
        self.assertTrue(pos.get_castling_right("q"))

        e4 = chess.Move.from_uci('e2e4')
        self.assertTrue(e4 in pos.get_legal_moves())
        pos.make_move(e4)
        self.assertTrue(pos.get_castling_right("q"))

        e5 = chess.Move.from_uci('e7e5')
        self.assertTrue(e5 in pos.get_legal_moves())
        self.assertFalse(e4 in pos.get_legal_moves())
        pos.make_move(e5)
        self.assertTrue(pos.get_castling_right("q"))

        Qf3 = chess.Move.from_uci('d1f3')
        self.assertTrue(Qf3 in pos.get_legal_moves())
        pos.make_move(Qf3)
        self.assertTrue(pos.get_castling_right("q"))

        Nc6 = chess.Move.from_uci('b8c6')
        self.assertTrue(Nc6 in pos.get_legal_moves())
        pos.make_move(Nc6)
        self.assertTrue(pos.get_castling_right("q"))

        Bc4 = chess.Move.from_uci('f1c4')
        self.assertTrue(Bc4 in pos.get_legal_moves())
        pos.make_move(Bc4)
        self.assertTrue(pos.get_castling_right("q"))

        Rb8 = chess.Move.from_uci('a8b8')
        self.assertTrue(Rb8 in pos.get_legal_moves())
        pos.make_move(Rb8)
        self.assertFalse(pos.get_castling_right("q"))

        self.assertFalse(pos.is_check())
        self.assertFalse(pos.is_checkmate())
        self.assertFalse(pos.is_game_over())
        self.assertFalse(pos.is_stalemate())

        Qf7_mate = chess.Move.from_uci('f3f7')
        self.assertTrue(Qf7_mate in pos.get_legal_moves())
        pos.make_move(Qf7_mate)

        self.assertTrue(pos.is_check())
        self.assertTrue(pos.is_checkmate())
        self.assertTrue(pos.is_game_over())
        self.assertFalse(pos.is_stalemate())

        self.assertEqual(pos.fen, "1rbqkbnr/pppp1Qpp/2n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQk - 0 4")

    def test_move_info(self):
        """Tests move info generation."""
        pos = chess.Position()
        e4 = pos.get_move_info(chess.Move.from_uci('e2e4'))
        self.assertEqual(e4.san, 'e4')
        self.assertFalse(e4.is_check)
        self.assertFalse(e4.is_checkmate)
        self.assertFalse(e4.is_castle)

    def test_pawn_captures(self):
        """Tests pawn captures in the kings gambit."""
        pos = chess.Position()
        pos.make_move(pos.get_move_from_san("e4"))
        pos.make_move(pos.get_move_from_san("e5"))
        pos.make_move(pos.get_move_from_san("f4"))

        accepted = pos.copy()
        self.assertTrue(chess.Move.from_uci("e5f4") in accepted.get_pseudo_legal_moves())
        self.assertTrue(chess.Move.from_uci("e5f4") in accepted.get_legal_moves())
        accepted.make_move(accepted.get_move_from_san("exf4"))

        wierd_declined = pos.copy()
        wierd_declined.make_move(wierd_declined.get_move_from_san("d5"))
        wierd_declined.make_move(wierd_declined.get_move_from_san("exd5"))


    def test_single_step_pawn_move(self):
        """Tests that single step pawn moves are possible."""
        pos = chess.Position()
        a3 = chess.Move.from_uci('a2a3')
        self.assertTrue(a3 in pos.get_pseudo_legal_moves())
        self.assertTrue(a3 in pos.get_legal_moves())
        pos.get_move_info(a3)
        pos.make_move(a3)

    def test_pawn_move_generation(self):
        """Tests pawn move generation in a specific position from a
Kasparov vs. Deep Blue game."""
        pos = chess.Position("8/2R1P3/8/2pp4/2k1r3/P7/8/1K6 w - - 1 55")
        list(pos.get_pseudo_legal_moves())

    def test_get_set(self):
        """Tests the get and set methods."""
        pos = chess.Position()
        self.assertEqual(pos["b1"], chess.Piece("N"))

        del pos["e2"]
        self.assertEqual(pos[chess.Square("e2")], None)

        pos[chess.Square("e4")] = chess.Piece("r")
        self.assertEqual(pos["e4"], chess.Piece("r"))

    def test_ep_file(self):
        pos = chess.Position("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2")
        self.assertEqual(pos.ep_file, "d")

    def test_san_moves(self):
        """Tests making moves from SANs."""
        pos = chess.Position()

        pos.make_move(pos.get_move_from_san('Nc3'))
        pos.make_move(pos.get_move_from_san('c5'))

        pos.make_move(pos.get_move_from_san('e4'))
        pos.make_move(pos.get_move_from_san('g6'))

        pos.make_move(pos.get_move_from_san('Nge2'))
        pos.make_move(pos.get_move_from_san('Bg7'))

        pos.make_move(pos.get_move_from_san('d3'))
        pos.make_move(pos.get_move_from_san('Bxc3'))

        pos.make_move(pos.get_move_from_san('bxc3'))

        self.assertEqual(pos.fen, 'rnbqk1nr/pp1ppp1p/6p1/2p5/4P3/2PP4/P1P1NPPP/R1BQKB1R b KQkq - 0 5')


class SquareTestCase(unittest.TestCase):
    """Tests the Square class."""

    def test_equality(self):
        """Tests the overriden equality behaviour of the Square class."""
        a = chess.Square("b4")
        b = chess.Square("b4")
        c = chess.Square("b3")
        d = chess.Square("f3")

        self.assertEqual(a, b)
        self.assertEqual(b, a)

        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(c, d)

    def test_simple_properties(self):
        """Tests simple properties of Square objects."""
        f7 = chess.Square("f7")
        self.assertFalse(f7.is_dark())
        self.assertTrue(f7.is_light())
        self.assertEqual(f7.rank, 7)
        self.assertEqual(f7.file, 'f')
        self.assertEqual(f7.name, 'f7')
        self.assertEqual(f7.x88, 21)
        self.assertEqual(f7.x, 5)
        self.assertEqual(f7.y, 6)
        self.assertFalse(f7.is_backrank())

    def test_creation(self):
        """Tests creation of Square instances."""
        self.assertEqual(chess.Square.from_x_and_y(3, 5), chess.Square("d6"))
        self.assertEqual(chess.Square.from_x88(2), chess.Square("c8"))
        self.assertEqual(chess.Square.from_rank_and_file(rank=2, file="g"), chess.Square("g2"))

    def test_iteration(self):
        """Tests iteration over all squares."""
        self.assertTrue(chess.Square("h8") in chess.Square.get_all())
        self.assertTrue(chess.Square("b1") in chess.Square.get_all())


class UtilTestCase(unittest.TestCase):
    """Tests utility functions."""

    def test_opposite_color(self):
        """Tests the opposite color function."""
        self.assertEqual(chess.opposite_color("w"), "b")
        self.assertEqual(chess.opposite_color("b"), "w")


class ZobristHasherTestCase(unittest.TestCase):
    """Tests the ZobristHasher class."""

    def test_polyglot_hashing(self):
        """Tests zobrist hashing against the polyglot reference examples given
on http://hardy.uhasselt.be/Toga/book_format.html."""
        hasher = chess.ZobristHasher(chess.ZobristHasher.POLYGLOT_RANDOM_ARRAY)

        pos = chess.Position()
        self.assertEqual(hasher.hash_position(pos), 0x463b96181691fc9c)

        pos = chess.Position("rnbqkbnr/p1pppppp/8/8/P6P/R1p5/1P1PPPP1/1NBQKBNR b Kkq - 0 4")
        self.assertEqual(hasher.hash_position(pos), 0x5c3f9b829b279560)

        pos = chess.Position("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        self.assertEqual(hasher.hash_position(pos), 0x823c9b50fd114196)

        pos = chess.Position("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2")
        self.assertEqual(hasher.hash_position(pos), 0x0756b94461c50fb0)

        pos = chess.Position("rnbq1bnr/ppp1pkpp/8/3pPp2/8/8/PPPPKPPP/RNBQ1BNR w - - 0 4")
        self.assertEqual(hasher.hash_position(pos), 0x00fdd303c946bdd9)

        # Real en-passant possible.
        pos = chess.Position("rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3")
        self.assertEqual(hasher.hash_position(pos), 0x22a48b5a8e47ff78)

    def test_random_hasher(self):
        """Tests zobrist hashing with a random field."""
        random.seed(3456789)
        hasher = chess.ZobristHasher.create_random()

        a = chess.Position()

        b = chess.Position()
        b.make_move(chess.Move.from_uci("e2e4"))

        self.assertNotEqual(hasher.hash_position(a), hasher.hash_position(b))


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
