import unittest
from functools import partial

from chesslet.board import Board
from chesslet.board import InvalidMoveException
from chesslet.piece import Piece
from chesslet.point import Point

class BoardTest(unittest.TestCase):
    def test_move_rook(self):
        board = Board(True)
        piece = Piece({"Rook": 1})
        board.board[0][0] = piece
        board.board[1][0] = Piece({"Knight": 1})

        # Tests invalid movement outside of the board
        part = partial(board.move_piece, Point(0, 0), Point(-1, 0))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid diagonal movement
        part = partial(board.move_piece, Point(0, 0), Point(1, 1))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid movement over another piece
        part = partial(board.move_piece, Point(0, 0), Point(2, 0))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid orthogonal movement greater than 2 spaces
        part = partial(board.move_piece, Point(0, 0), Point(0, 4))
        self.assertRaises(InvalidMoveException, part)

        # Tests valid orthogonal movement
        board.move_piece(Point(0, 0), Point(0, 2))
        self.assertEqual(board.board[0][2], piece)
    
    def test_move_bishop(self):
        board = Board(True)
        piece = Piece({"Bishop": 1})
        board.board[3][0] = piece
        board.board[4][1] = Piece({"Rook": 1})

        # Tests invalid orthogonal movement
        part = partial(board.move_piece, Point(3, 0), Point(3, 2))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid movement over another piece
        part = partial(board.move_piece, Point(3, 0), Point(5, 2))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid diagonal movement greater than 2 spaces
        part = partial(board.move_piece, Point(3, 0), Point(0, 3))
        self.assertRaises(InvalidMoveException, part)

        # Tests valid orthogonal movement
        board.move_piece(Point(3, 0), Point(1, 2))
        self.assertEqual(board.board[1][2], piece)

    def test_move_knight(self):
        board = Board(True)
        piece = Piece({"Knight": 1})
        board.board[3][0] = piece
        board.board[3][1] = Piece({"Bishop": 1})
        board.board[3][2] = Piece({"Bishop": 1})
        board.board[4][1] = Piece({"Bishop": 1})

        # Tests invalid non-L-shaped movement
        part = partial(board.move_piece, Point(3, 0), Point(5, 0))
        self.assertRaises(InvalidMoveException, part)

        # Tests valid L-shaped movement
        board.move_piece(Point(3, 0), Point(1, 1))
        self.assertEqual(board.board[1][1], piece)
        board.move_piece(Point(1, 1), Point(3, 0))

        # Tests valid L-shaped movement over other pieces
        board.move_piece(Point(3, 0), Point(4, 2))
        self.assertEqual(board.board[4][2], piece)

if __name__ == '__main__':
    unittest.main()