import unittest
from functools import partial

from chesslet.player import Player, InvalidPasswordException, AlreadyLoggedInException
from webserver import ServerState, PlayerAlreadyExistsException


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server_state = ServerState("./tests/testUsers.json")
        self.players = {
            "1234567890abcdef": Player(
                uuid="1234567890abcdef",
                password="unsafe",
                account_name="Tom"
            ),
            "1234567890abcdf0": Player(
                uuid="1234567890abcdf0",
                password="unsafe",
                account_name="Grace"
            ),
            "1234567890abcdf1": Player(
                uuid="1234567890abcdf1",
                password="unsafe",
                account_name="Jack"
            ),
            "1234567890abcdf2": Player(
                uuid="1234567890abcdf2",
                password="unsafe",
                account_name="Flynn"
            ),
        }

    def test_load_players(self):
        self.assertEqual(self.players, self.server_state.players)

    def test_add_new_player(self):
        uuid = "abcdef1234567890"
        password = "unsafe"
        name = "Matt"

        self.server_state.register_user(
            uuid=uuid,
            password=password,
            account_name=name,
        )

        new_players = dict(self.players)
        new_players[uuid] = Player(
            uuid=uuid,
            password=password,
            account_name=name
        )

        self.assertEqual(new_players, self.server_state.players)

    def test_cant_add_new_player(self):
        uuid = "1234567890abcdef"
        password = "unsafe"
        name = "Matt"

        self.assertRaises(
            PlayerAlreadyExistsException,
            partial(
                self.server_state.register_user,
                uuid=uuid,
                password=password,
                account_name=name
            )
        )

        self.assertEqual(self.players, self.server_state.players)

    def test_login_player(self):
        self.server_state.login_player("1234567890abcdef", "unsafe")

        self.assertTrue(
            self.server_state.players["1234567890abcdef"].logged_in
        )

    def test_cant_login_player(self):
        self.assertRaises(
            InvalidPasswordException,
            partial(
                self.server_state.login_player,
                uuid="1234567890abcdef",
                password="dorito"
            )
        )

        self.assertFalse(
            self.server_state.players["1234567890abcdef"].logged_in,
        )

    def test_no_double_login(self):
        login = partial(
            self.server_state.login_player,
            uuid="1234567890abcdef",
            password="unsafe"
        )

        login()
        self.assertRaises(
            AlreadyLoggedInException,
            login
        )

        self.assertTrue(
            self.server_state.players["1234567890abcdef"].logged_in,
        )


if __name__ == '__main__':
    unittest.main()
