import unittest

from chesslet.player import Player


class PlayerTest(unittest.TestCase):
    def test_user_login(self):
        # Get username and password
        uuid = input ("Please enter your username")
        password = input("Please enter your password")

        # Instantiate the required objects
        player = Player(uuid, password)
        Player.login(player, uuid, password)

    def test_set_highscore(self):
        player1 = Player("abc", "123")
        player1.setHighscore(23)


if __name__ == '__main__':
    unittest.main()
