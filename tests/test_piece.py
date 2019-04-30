import unittest
from functools import partial

from chesslet.point import Point
from chesslet.piece import Piece
from chesslet.piece import InvalidCombinationStateException

class TestPiece(unittest.TestCase):
    def test_create_piece(self):
        # Tests standard piece creation
        piece = Piece({"Bishop"}, Point(0, 0))
        self.assertEqual(piece.combination_state, {"Bishop"})

        # Tests an invalid combination state
        part = partial(Piece, {"Queen"}, Point(0, 0))
        self.assertRaises(InvalidCombinationStateException, part)

    def test_combine_piece(self):
        piece = Piece({"Bishop"}, Point(0, 0))

        # Tests an invalid combination state
        part = partial(piece.combine_piece, {"Queen"})
        self.assertRaises(InvalidCombinationStateException, part)

        # Tests an attempt to combine a combination state with a
        # piece that already contains that state
        part = partial(piece.combine_piece, {"Bishop", "Knight"})
        self.assertRaises(InvalidCombinationStateException, part)

        # Tests valid piece combination
        piece.combine_piece({"Knight"})
        self.assertEqual(piece.combination_state, {"Bishop", "Knight"})

    def test_split_piece(self):
        piece = Piece({"Bishop", "Knight"}, Point(0, 0))

        # Tests an invalid combination state
        part = partial(piece.split_piece, {"Rook"}, Point(1, 1))
        self.assertRaises(InvalidCombinationStateException, part)

        # Tests valid piece split
        other_piece = piece.split_piece({"Bishop"}, Point(1, 1))
        self.assertEqual(piece.combination_state, {"Knight"})
        self.assertEqual(other_piece.combination_state, {"Bishop"})

if __name__ == '__main__':
    unittest.main()