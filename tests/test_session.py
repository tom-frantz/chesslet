import unittest
from functools import partial

from chesslet.session import Session, PlayerAlreadyAddedException
from chesslet.player import Player


class SessionTest(unittest.TestCase):
    def test_add_player(self):
        # Instantiate the required objects
        session = Session("1234")
        player = Player(
            uuid="a",
            password="b",
            account_name="c"
        )
        player.logged_in = True

        # Add a player to the session
        session.add_player(player)

        # Check to see if session.players is equivalent to an array with the player in it
        self.assertEqual(session.players, {"a": player})

    def test_no_double_players(self):
        # Instantiate the required objects
        session = Session("1234")
        player = Player(
            uuid="a",
            password="b",
            account_name="c"
        )
        player.logged_in = True

        # Add a player to the session
        session.add_player(player)
        part = partial(session.add_player, player)


        self.assertRaises(
            PlayerAlreadyAddedException,
            part
        )

        # Check to see if session.players is equivalent to an array with the player in it
        self.assertEqual(session.players, {"a": player})


if __name__ == '__main__':
    unittest.main()
