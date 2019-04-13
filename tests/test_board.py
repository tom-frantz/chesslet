import unittest
from functools import partial

from chesslet.board import Board, PlayerAlreadyAddedException
from chesslet.player import Player


class BoardTest(unittest.TestCase):
    def test_add_player(self):
        # Instantiate the required objects
        board = Board("1234")
        player = Player(
            uuid="a",
            password="b",
            account_name="c"
        )
        player.logged_in = True

        # Add a player to the board
        board.add_player(player)

        # Check to see if board.players is equivalent to an array with the player in it
        self.assertEqual(board.players, {"a": player})

    def test_no_double_players(self):
        # Instantiate the required objects
        board = Board("1234")
        player = Player(
            uuid="a",
            password="b",
            account_name="c"
        )
        player.logged_in = True

        # Add a player to the board
        board.add_player(player)
        part = partial(board.add_player, player)


        self.assertRaises(
            PlayerAlreadyAddedException,
            part
        )

        # Check to see if board.players is equivalent to an array with the player in it
        self.assertEqual(board.players, {"a": player})


if __name__ == '__main__':
    unittest.main()
