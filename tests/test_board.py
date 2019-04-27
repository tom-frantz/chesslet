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

    def create_player_piece(self, piece, player_pieces, x, y):
        self.board.board[x][y] = piece
        player_pieces.append(piece)
        return piece

    def setUp(self):
        self.player_1 = Player("abc", "unsafe", "tom")
        self.player_2 = Player("yeet", "unsafe", "jashdjas")
        self.board = Board(Session("abc"), True)
    
    def test_move_rook(self):
        piece = self.create_player_piece(Piece({"Rook": 1}), self.board.player_1_pieces, 0, 0)
        self.create_player_piece(Piece({"Knight": 1}), self.board.player_2_pieces, 1, 0)
        rook_move = self.move_from(Point(0, 0))

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
        piece = self.create_player_piece(Piece({"Bishop": 1}), self.board.player_1_pieces, 3, 0)
        self.create_player_piece(Piece({"Rook": 1}), self.board.player_2_pieces, 4, 1)
        bishop_move = self.move_from(from_point=Point(3, 0))

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
        piece = self.create_player_piece(Piece({"Knight": 1}), self.board.player_1_pieces, 3, 0)
        create_bishop = partial(self.create_player_piece, Piece({"Bishop": 1}), self.board.player_2_pieces)
        create_bishop(3, 1)
        create_bishop(3, 2)
        create_bishop(4, 1)
        knight_move = self.move_from(Point(3, 0))

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
        self.create_player_piece(Piece({"Bishop": 1}), self.board.player_1_pieces, 3, 0)
        self.create_player_piece(Piece({"Rook": 1}), self.board.player_1_pieces, 4, 1)

        # Tests combining the bishop into the rook
        self.board.move_piece(True, Point(3, 0), Point(4, 1))
        self.assertEqual(self.board.board[4][1].combination_state, {"Rook": 1, "Bishop": 1, "Knight": 0})

    def test_move_combined_piece(self):
        piece = self.create_player_piece(Piece({"Rook": 1, "Bishop": 1}), self.board.player_1_pieces, 3, 0)

        # Tests rook movement
        self.board.move_piece(True, Point(3, 0), Point(3, 2))

        # Test bishop movement
        self.board.move_piece(True, Point(3, 2), Point(5, 4))

        self.assertEqual(self.board.board[5][4], piece)

    def test_split_piece(self):
        self.create_player_piece(Piece({"Rook": 1, "Bishop": 1}), self.board.player_1_pieces, 3, 0)

        # Splits rook out
        self.board.move_piece(True, Point(3, 0), Point(3, 2), {"Rook": 1})
        self.assertEqual(self.board.board[3][2].combination_state, {"Rook": 1, "Bishop": 0, "Knight": 0})
        self.assertEqual(self.board.board[3][0].combination_state, {"Rook": 0, "Bishop": 1, "Knight": 0})

        # Test invalid rook movement by the bishop
        part = partial(self.board.move_piece, True, Point(3, 0), Point(3, 1))
        self.assertRaises(InvalidMoveException, part)


if __name__ == '__main__':
    unittest.main()
