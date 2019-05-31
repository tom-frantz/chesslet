# tests/test_board.py

import unittest
from functools import partial

from chesslet.board import Board
from chesslet.board import InvalidMoveException
from chesslet.piece import Piece
from chesslet.player import Player
from chesslet.point import Point
from chesslet.session import Session

BOARD = Board(True)





class BoardTest(unittest.TestCase):
    def move_from(self, from_point):
        def inside(x, y):
            return partial(self.board.move_piece, True, from_point, Point(x, y))
        return inside

    def setUp(self):
        self.player_1 = Player("abc", "unsafe", "tom")
        self.player_2 = Player("yeet", "unsafe", "jashdjas")
        self.board = Board(Session("abc"), True)

    def test_move_rook(self):
        piece = self.board.add_piece({"Rook"}, Point(0, 0), player_1=True)
        self.board.add_piece({"Knight"}, Point(1, 0), player_1=False)
        rook_move = self.move_from(Point(0, 0))
        self.board.update_valid_move_positions()

        # Tests invalid movement outside of the board
        self.assertRaises(InvalidMoveException, rook_move(-1, 0))

        # Tests invalid diagonal movement
        self.assertRaises(InvalidMoveException, rook_move(1, 1))

        # Tests invalid movement over another piece
        self.assertRaises(InvalidMoveException, rook_move(2, 0))

        # Tests invalid orthogonal movement greater than 2 spaces
        self.assertRaises(InvalidMoveException, rook_move(0, 4))

        # Tests valid orthogonal movement
        rook_move(0, 2)()
        self.assertEqual(self.board.board[0][2], piece)

    def test_move_bishop(self):
        piece = self.board.add_piece({"Bishop"}, Point(3, 0), player_1=True)
        self.board.add_piece({"Rook"}, Point(4, 1), player_1=False)
        bishop_move = self.move_from(from_point=Point(3, 0))
        self.board.update_valid_move_positions()

        # Tests invalid orthogonal movement
        self.assertRaises(InvalidMoveException, bishop_move(3, 2))

        # Tests invalid movement over another piece
        self.assertRaises(InvalidMoveException, bishop_move(5, 2))

        # Tests invalid diagonal movement greater than 2 spaces
        self.assertRaises(InvalidMoveException, bishop_move(0, 3))

        # Tests valid orthogonal movement
        bishop_move(1, 2)()
        self.assertEqual(self.board.board[1][2], piece)

    def test_move_knight(self):
        piece = self.board.add_piece({"Knight"}, Point(3, 0), player_1=True)
        self.board.add_piece({"Bishop"}, Point(3, 1), player_1=False)
        self.board.add_piece({"Bishop"}, Point(3, 2), player_1=False)
        self.board.add_piece({"Bishop"}, Point(4, 1), player_1=False)
        knight_move = self.move_from(Point(3, 0))
        self.board.update_valid_move_positions()

        # Tests invalid non-L-shaped movement
        self.assertRaises(InvalidMoveException, knight_move(5, 0))

        # Tests valid L-shaped movement
        knight_move(1, 1)()
        self.assertEqual(self.board.board[1][1], piece)
        self.board.move_piece(True, Point(1, 1), Point(3, 0))

        # Tests valid L-shaped movement over other pieces
        knight_move(4, 2)()
        self.assertEqual(self.board.board[4][2], piece)

    def test_combine_piece(self):
        self.board.add_piece({"Bishop"}, Point(3, 0), player_1=True)
        self.board.add_piece({"Rook"}, Point(4, 1), player_1=True)
        self.board.update_valid_move_positions()

        # Tests combining the bishop into the rook
        self.board.move_piece(True, Point(3, 0), Point(4, 1))
        self.assertEqual(self.board.board[4][1].combination_state, {"Rook", "Bishop"})

    def test_move_combined_piece(self):
        piece = self.board.add_piece({"Rook", "Bishop"}, Point(3, 0), player_1=True)
        self.board.update_valid_move_positions()

        # Tests rook movement
        self.board.move_piece(True, Point(3, 0), Point(3, 2))

        # Test bishop movement
        self.board.move_piece(True, Point(3, 2), Point(5, 4))

        self.assertEqual(self.board.board[5][4], piece)

    def test_split_piece(self):
        self.board.add_piece({"Rook", "Bishop"}, Point(3, 0), player_1=True)
        self.board.update_valid_move_positions()

        # Splits rook out
        self.board.move_piece(True, Point(3, 0), Point(3, 2), {"Rook"})
        self.assertEqual(self.board.board[3][2].combination_state, {"Rook"})
        self.assertEqual(self.board.board[3][0].combination_state, {"Bishop"})

        # Test invalid rook movement by the bishop
        part = partial(self.board.move_piece, True, Point(3, 0), Point(3, 1))
        self.assertRaises(InvalidMoveException, part)


if __name__ == '__main__':
    unittest.main()
