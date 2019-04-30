from chesslet.player import PlayerNotLoggedIn
from chesslet.board import Board
from chesslet.board import InvalidMoveException
from chesslet.board import InvalidPieceSelectionException
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
        self.board = Board(session=self)

    def add_player(self, player):
        if not player.logged_in:
            raise PlayerNotLoggedIn("Cannot allow a not logged in player into game")

        if self.player_1 is None:
            if self.player_2 is not None and player.uuid == self.player_2.uuid:
                raise PlayerAlreadyAddedException
            self.player_1 = player
        else:
            if self.player_1 is not None and player.uuid == self.player_1.uuid:
                raise PlayerAlreadyAddedException
            self.player_2 = player

    def remove_player(self, player):
        if player.uuid == self.player_1.uuid:
            self.player_1 = None
        elif player.uuid == self.player_2.uuid:
            self.player_2 = None
        else:
            raise PlayerNotLoggedIn("Cannot remove a player not added to game")

    def move_piece(self, requesting_player_uuid, curr_pos, new_pos, combination_state = None):
        player = self.player_1 if self.player_1_turn else self.player_2

        if player.uuid != requesting_player_uuid:
            raise Exception("TODO")

        try:
            self.board.move_piece(self.player_1_turn, curr_pos, new_pos, combination_state)
            self.player_1_turn = not self.player_1_turn
        except InvalidMoveException:
            pass #TODO
        except InvalidPieceSelectionException:
            pass #TODO

    # Allows the board to let the session know that a piece has been taken
    def piece_taken(self, piece):
        player = self.player_1 if self.player_1_turn else self.player_2
        player.score += 5
