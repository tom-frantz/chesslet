import unittest
from functools import partial

from chesslet.board import Board
from chesslet.board import InvalidMoveException
from chesslet.piece import Piece
from chesslet.player import Player
from chesslet.point import Point

BOARD = Board(True)


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.player_1 = Player("abc", "unsafe", "tom")
        self.player_2 = Player("yeet", "unsafe", "jashdjas")
        self.board = Board(True)

    def test_move_rook(self):
        piece = Piece({"Rook": 1})
        self.board.board[0][0] = piece
        self.board.player_1_pieces.append(self.board.board[0][0])
        self.board.board[1][0] = Piece({"Knight": 1})

        # Tests invalid movement outside of the board
        outside_move = partial(self.board.move_piece, self.player_1.uuid, Point(0, 0), Point(-1, 0))
        self.assertRaises(InvalidMoveException, outside_move)

        # Tests invalid diagonal movement
        diagonal_move = partial(self.board.move_piece, self.player_1.uuid, Point(0, 0), Point(1, 1))
        self.assertRaises(InvalidMoveException, diagonal_move)

        # Tests invalid movement over another piece
        over_move = partial(self.board.move_piece, self.player_1.uuid, Point(0, 0), Point(2, 0))
        self.assertRaises(InvalidMoveException, over_move)

        # Tests invalid orthogonal movement greater than 2 spaces
        far_move = partial(self.board.move_piece, self.player_1.uuid, Point(0, 0), Point(0, 4))
        self.assertRaises(InvalidMoveException, far_move)

        # Tests valid orthogonal movement
        self.board.move_piece(self.player_1.uuid, Point(0, 0), Point(0, 2))
        self.assertEqual(self.board.board[0][2], piece)
    
    def test_move_bishop(self):
        piece = Piece({"Bishop": 1})

        self.board.board[3][0] = piece
        self.board.player_1_pieces.append(self.board.board[3][0])

        self.board.board[4][1] = Piece({"Rook": 1})
        self.board.player_2_pieces.append(self.board.board[4][1])

        # Tests invalid orthogonal movement
        part = partial(self.board.move_piece, self.player_1.uuid, Point(3, 0), Point(3, 2))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid movement over another piece
        part = partial(self.board.move_piece, self.player_1.uuid, Point(3, 0), Point(5, 2))
        self.assertRaises(InvalidMoveException, part)

        # Tests invalid diagonal movement greater than 2 spaces
        part = partial(self.board.move_piece, self.player_1.uuid, Point(3, 0), Point(0, 3))
        self.assertRaises(InvalidMoveException, part)

        # Tests valid orthogonal movement
        self.board.move_piece(self.player_1.uuid, Point(3, 0), Point(1, 2))
        self.assertEqual(self.board.board[1][2], piece)

    def test_move_knight(self):
        piece = Piece({"Knight": 1})
        self.board.board[3][0] = piece
        self.board.player_1_pieces.append(self.board.board[3][0])

        self.board.board[3][1] = Piece({"Bishop": 1})
        self.board.player_2_pieces.append(self.board.board[3][1])
        self.board.board[3][2] = Piece({"Bishop": 1})
        self.board.player_2_pieces.append(self.board.board[3][2])
        self.board.board[4][1] = Piece({"Bishop": 1})
        self.board.player_2_pieces.append(self.board.board[4][1])

        # Tests invalid non-L-shaped movement
        part = partial(self.board.move_piece, self.player_1.uuid, Point(3, 0), Point(5, 0))
        self.assertRaises(InvalidMoveException, part)

        # Tests valid L-shaped movement
        self.board.move_piece(self.player_1.uuid, Point(3, 0), Point(1, 1))
        self.assertEqual(self.board.board[1][1], piece)
        self.board.move_piece(self.player_1.uuid, Point(1, 1), Point(3, 0))

        # Tests valid L-shaped movement over other pieces
        self.board.move_piece(self.player_1.uuid, Point(3, 0), Point(4, 2))
        self.assertEqual(self.board.board[4][2], piece)


if __name__ == '__main__':
    unittest.main()
