import unittest

from chesslet.player import Player


class PlayerTest(unittest.TestCase):
    def test_user_login(self):
        # Get username and password
        uuid = input("Please enter your username")
        password = input("Please enter your password")

        # Instantiate the required objects
        player = Player(uuid, password, "Grace")
        player.login(password)

        # This test needs a way to assert, or to check, that the test has passed.

    def test_set_highscore(self):
        player = Player("12893829", "password", "Grace")
        player.highscore = 23

        self.assertEqual(23, player.highscore)


if __name__ == '__main__':
    unittest.main()
