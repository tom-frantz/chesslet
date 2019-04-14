from chesslet.player import PlayerNotLoggedIn
from chesslet.board import Board
from chesslet.point import Point

# -Session class has a function called by the server, which takes from pos,
#  to pos, player id, and a name of a piece if it's being split off


class PlayerAlreadyAddedException(Exception):
    pass


class PlayerNotAddedException(Exception):
    pass


class Session:
    def __init__(self, uuid):
        self.uuid = uuid
        self.players = {}
        self.board = Board(self.uuid)

    def add_player(self, player):
        # if expression
        if player.uuid in self.players:
            raise PlayerAlreadyAddedException

        if player.logged_in:
            self.players[player.uuid] = player
        else:
            raise PlayerNotLoggedIn("Cannot allow a not logged in player into game")

    def remove_player(self, player):
        if player.uuid in self.players:
            del self.players[player.uuid]
        else:
            raise PlayerNotLoggedIn("Cannot remove a player not added to game")

    # Simple move piece without being able to split or combine piece
    def move_piece(self, player, curr_pos_x, curr_pos_y, new_pos_x, new_pos_y):
        if player.uuid not in self.players:
            raise PlayerNotAddedException("Player not added cannot move piece")

        curr_pos = Point(curr_pos_x, curr_pos_y)
        new_pos = Point(new_pos_x, new_pos_y)
        self.board.move_piece(player, curr_pos, new_pos)
