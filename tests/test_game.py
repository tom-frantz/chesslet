# tests/test_game.py

import unittest

from chesslet.player import Player
from chesslet.point import Point
from chesslet.session import Session


class GameTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_game(self):
        session = Session("0123456789abcdef")

        player1 = Player("abc", "unsafe", "Tom")
        player2 = Player("def", "unsafe", "Jack")

        for player in [player1, player2]:
            player.login("unsafe")

        session.add_player(player1)
        session.add_player(player2)

        print(session.board)

        session.move_piece(player1.uuid, Point(2, 0), Point(3, 2))
        print(session.board)
        print("SCORES: Player 1:", str(session.player_1.score) + ", Player 2:", session.player_2.score)
        print()

        session.move_piece(player2.uuid, Point(5, 5), Point(5, 3))
        print(session.board)

        session.move_piece(player1.uuid, Point(3, 2), Point(5, 3))
        print(session.board)
        print("SCORES:", session.player_1.score, session.player_2.score)
        print()


if __name__ == '__main__':
    unittest.main()
