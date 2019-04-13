from chesslet.player import PlayerNotLoggedIn


class PlayerAlreadyAddedException(Exception):
    pass


class Board:
    def __init__(self, uuid):
        self.uuid = uuid
        self.game_board = []
        self.players = {}

    def add_player(self, player):
        # if expression
        if player.uuid in self.players:
            raise PlayerAlreadyAddedException

        if player.logged_in:
            self.players[player.uuid] = player
        else:
            raise PlayerNotLoggedIn("Cannot allow a not logged in player into game")

    def recieve_event(self):
        pass
