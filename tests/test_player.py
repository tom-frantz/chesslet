# tests/test_player.py

import unittest

from chesslet.player import Player
from chesslet.player import PlayerNotLoggedIn


class PlayerTest(unittest.TestCase):
    def test_user_login(self):
        # Get username and password
        uuid = input("\nPlease enter your username: ")
        password = input("Please enter your password: ")

        # Instantiate the required objects
        player = Player(uuid, password, "Grace")
        player.login(password)

        # This test needs a way to assert, or to check, that the test has passed.

    def test_set_highscore(self):
        player = Player("12893829", "password", "Grace")
        player.highscore = 23

        self.assertEqual(23, player.highscore)

    def test_user_log_out_fail(self):
        # Testing
        player = Player("12893829", "password", "Grace")

        self.assertRaises(PlayerNotLoggedIn, player.logout)

    def test_user_log_out_success(self):
        # Testing the player logout with success
        player = Player("12893829", "password", "Grace")
        player.login("password")
        self.assertTrue(player.logout())


if __name__ == '__main__':
    unittest.main()
