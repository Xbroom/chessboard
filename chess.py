# -*- coding: utf-8 -*-

def opposite_color(color):
    if color == "w":
        return "b"
    elif color == "white":
        return "black"
    elif color == "b":
        return "w"
    elif color == "black":
        return "white"
    else:
        raise ValueError("Expected w, b, white or black, got: %s." % color)


class Piece(object):

    __cache = dict()

    def __new__(cls, symbol):
        try:
            return cls.__cache[symbol]
        except KeyError:
            cls.__cache[symbol] = super(Piece, cls).__new__(cls, symbol)
            return cls.__cache[symbol]

    def __init__(self, symbol):
        self.__symbol = symbol

        self.__color = "w" if symbol != symbol.lower() else "b"
        self.__full_color = "white" if self.__color == "w" else "black"

        self.__type = symbol.lower()
        if self.__type == "p":
            self.__full_type = "pawn"
        elif self.__type == "n":
            self.__full_type = "knight"
        elif self.__type == "b":
            self.__full_type = "bishop"
        elif self.__type == "r":
            self.__full_type = "rook"
        elif self.__type == "q":
            self.__full_type = "queen"
        elif self.__type == "k":
            self.__full_type = "king"
        else:
            raise ValueError("Expected valid piece symbol, got: %s." % symbol)

        self.__hash = ord(self.__symbol)

    @classmethod
    def from_color_and_type(cls, color, type):
        if type == "p" or type == "pawn":
            symbol = "p"
        elif type == "n" or type == "knight":
            symbol = "n"
        elif type == "b" or type == "bishop":
            symbol = "b"
        elif type == "r" or type == "rook":
            symbol = "r"
        elif type == "q" or type == "queen":
            symbol = "q"
        elif type == "k" or type == "king":
            symbol = "k"
        else:
            raise ValueError("Expected piece type, got: %s." % type)

        if color == "w" or color == "white":
            return cls(symbol.upper())
        elif color == "b" or color == "black":
            return cls(symbol)
        else:
            raise ValueError("Expected w, b, white or black, got: %s." % color)

    @property
    def symbol(self):
        return self.__symbol

    @property
    def color(self):
        return self.__color

    @property
    def full_color(self):
        return self.__full_color

    @property
    def type(self):
        return self.__type

    @property
    def full_type(self):
        return slef.__full_type

    def __str__(self):
        return self.__symbol

    def __repr__(self):
        return "Piece('%s')" % self.__symbol

    def __eq__(self, other):
        return isinstance(other, Piece) and self.__symbol == other.symbol

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return __hash


class Square(object):

    __cache = dict()

    def __init__(self, name):
        if not len(name) == 2:
            raise ValueError("Expected square name, got: %s." % repr(name))
        self.__name = name

        if not name[0] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            raise ValueError("Expected file, got: %s." % repr(name[0]))
        self.__file = name[0]
        self.__x = ord(self.__name[0]) - ord("a")

        if not name[1] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            raise ValueError("Expected rank, got: %s." % repr(name[1]))
        self.__rank = name[1]
        self.__y = ord(self.__name[1]) - ord("1")

        self.__x88 = self.__x + 16 * (7 - self.__y)

    @classmethod
    def __new__(cls, name):
        try:
            return cls.__cache[name]
        except KeyError:
            cls.__cache[name] = super(cls, self).__new__(cls, name)
            return cls.__cache[name]

    @classmethod
    def from_x88(cls, x88):
        if x88 < 0 or x88 > 128:
            raise ValueError("x88 index is out of range: %s." % repr(x88))

        if x88 & 0x88:
            raise ValueError("x88 is not on the board: %s." % repr(x88))

        return cls("abcdefgh"[x88 & 7] + "87654321"[x88 >> 4])

    @classmethod
    def from_rank_and_file(cls, rank, file):
         if rank < 1 or rank > 8:
             raise ValueError("Expected rank to be between 1 and 8: %s." % repr(rank))

         if not file in ["a", "b", "c", "d", "e", "f", "g", "h"]:
             raise ValueError("Expected the file to be a letter between 'a' and 'h': %s." % repr(file))

         return cls(file + str(rank))

    @classmethod
    def from_x_and_y(cls, x, y):
        return cls("abcdefgh"[x] + "12345678"[y])

    @property
    def name(self):
        return self.__name

    @property
    def file(self):
        return self.__file

    @property
    def x(self):
        return self.__x

    @property
    def rank(self):
        return self.__rank

    @property
    def y(self):
        return self.__y

    @property
    def x88(self):
        return self.__x88

    def is_dark(self):
        return (self.__x - self.__y % 2) == 0

    def is_light(self):
        return not self.is_dark()

    def is_backrank(self):
        return self.__y == 0 or self.__y == 7

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "Square('%s')" % self.__name

    def __eq__(self, other):
        return isinstance(other, Square) and self.__name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.__x88


class Move(object):

    __uci_move_regex = re.compile(r"^([a-h][1-8])([a-h][1-8])([rnbq]?)$")

    def __init__(self, source, target, promotion=None):
        if not isinstance(source, Square):
            raise TypeError("Expected source to be a Square.")
        self.__source = source

        if not isinstance(target, Square):
            raise TypeError("Expected target to be a Square.")
        self.__target = target

        if not promotion:
            self.__promotion = None
            self.__full_promotion = None
        else:
            promotion = promotion.lower()
            if promotion == "n" or promotion == "knight":
                self.__promotion = "n"
                self.__full_promotion = "knight"
            elif promotion == "b" or promotion == "bishop":
                self.__promotion = "b"
                self.__full_promotion = "bishop"
            elif promotion == "r" or promotion == "rook":
                self.__promotion = "r"
                self.__full_promotion = "rook"
            elif promotion == "q" or promotion == "queen":
                self.__promotion = "q"
                self.__full_promotion = "queen"
            else:
                raise ValueError("Expected promotion type, got: %s." % repr(promotion))

    @classmethod
    def from_uci(cls, uci):
        if uci == "0000":
            return cls.get_null()

        match = cls.__uci_move_regex.match(uci)

        return cls(
            source=Square(match.group(1)),
            target=Square(match.group(2)),
            promotion=match.group(3) or None)

    @classmethod
    def get_null(cls):
        return cls(Square("a1"), Square("a1"))

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @property
    def promotion(self):
        return self.__promotion

    @property
    def full_promotion(self):
        return self.__full_promotion

    @property
    def uci(self):
        if self.is_null():
            return "0000"
        else:
            if self.__promotion:
                return self.__source.name + self.__target.name + self.__promotion
            else:
                return self.__source.name + self.__target.name

    def is_null(self):
        return self.__source == self.__target

    def __nonzero__(self):
        return not self.is_null()

    def __str__(self):
        return self.uci

    def __repr__(self):
        return "Move.from_uci(%s)" % repr(self.uci)

    def __eq__(self, other):
        return isinstance(other, Move) and self.uci == other.uci

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.uci)
