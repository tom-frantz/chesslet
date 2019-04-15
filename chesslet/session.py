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
        self.player_1 = None
        self.player_2 = None
        self.player_1_turn = True
        self.board = Board()

    def add_player(self, player):
        # if expression
        if not player.logged_in:
            raise PlayerNotLoggedIn("Cannot allow a not logged in player into game")

        if self.player_1 is None:
            if self.player_2 is not None and player.uuid == self.player_2.uuid:
                raise PlayerAlreadyAddedException
            self.player_1 = player
            self.board.player_1_uuid = player.uuid
        else:
            if self.player_1 is not None and player.uuid == self.player_1.uuid:
                raise PlayerAlreadyAddedException
            self.player_2 = player
            self.board.player_2_uuid = player.uuid

    def remove_player(self, player):
        if player.uuid == self.player_1.uuid:
            self.player_1 = None
        elif player.uuid == self.player_2.uuid:
            self.player_2 = None
        else:
            raise PlayerNotLoggedIn("Cannot remove a player not added to game")

    # Simple move piece without being able to split or combine piece
    def move_piece(self, requesting_player_uuid, curr_pos, new_pos):
        player = self.player_1 if self.player_1_turn else self.player_2

        if player.uuid != requesting_player_uuid:
            raise Exception("TODO")

        self.player_1_turn = not self.player_1_turn

        other_piece = self.board.move_piece(player.uuid, curr_pos, new_pos)
        player.score += 5 if other_piece is not None else 0
