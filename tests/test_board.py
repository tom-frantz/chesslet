import unittest

from chesslet.board import Board


class BoardTest(unittest.TestCase):
    def test_add_player(self):
        # Instantiate the required objects
        board = Board("1234")
        player = {}  # TODO

        # Add a player to the board
        board.add_player(player)

        # Check to see if board.players is equivalent to an array with the player in it
        self.assertEqual(board.players, [player])


if __name__ == '__main__':
    unittest.main()
