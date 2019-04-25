import unittest
from functools import partial

from chesslet.point import Point
from chesslet.piece import Piece
from chesslet.piece import InvalidCombinationStateException

class TestPiece(unittest.TestCase):
    def test_create_piece(self):
        # Ensures a piece can be successfully created
        piece = Piece({"Bishop": 1})
        self.assertEqual(piece.combination_state, {"Rook": 0, "Bishop": 1, "Knight": 0})

        # Ensures that an invalid combination state will not be processed
        part = partial(Piece, {"Queen": 1})
        self.assertRaises(InvalidCombinationStateException, part)

    def test_get_move_set(self):
        # Ensures that the move_set is correctly calculated
        correct_move_set = [[Point(0, 1), Point(0, 2)], [Point(1, 0), Point(2, 0)], 
        [Point(0, -1), Point(0, -2)], [Point(-1, 0), Point(-2, 0)], [Point(1, 2)], 
        [Point(2, 1)], [Point(2, -1)], [Point(1, -2)], [Point(-1, -2)], [Point(-2, -1)], 
        [Point(-2, 1)], [Point(-1, 2)]]
        piece = Piece({"Rook": 1, "Knight": 1})
        self.assertEqual(Piece.get_move_set(piece.combination_state), correct_move_set)

if __name__ == '__main__':
    unittest.main()