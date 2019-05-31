# chesslet/session.py

from chesslet.player import PlayerNotLoggedIn
from chesslet.board import Board
from chesslet.board import InvalidMoveException
from chesslet.board import InvalidPieceSelectionException
from chesslet.point import Point


class PlayerAlreadyAddedException(Exception):
    pass


class PlayerNotAddedException(Exception):
    pass


class NotCurrentPlayerTryingToMoveException(Exception):
    pass


class Session:
    def __init__(self, uuid):
        self.uuid = uuid
        self.player_1 = None
        self.player_2 = None
        self.player_1_turn = False
        self.board = Board(session=self)
        self.winner = None
        self.player_1_moves = 0
        self.player_2_moves = 0


    # Adds a player to the game, provided that the player is not already logged
    # in. Also checks that the player has not already been logged in as another
    # player.
    def add_player(self, player):
        if not player.logged_in:
            raise PlayerNotLoggedIn("Cannot allow a not logged in player into game")

        if self.player_1 is None:
            if self.player_2 is not None and player.uuid == self.player_2.uuid:
                raise PlayerAlreadyAddedException("Player already added")
            self.player_1 = player
        else:
            if self.player_1 is not None and player.uuid == self.player_1.uuid:
                raise PlayerAlreadyAddedException("Player already added")
            self.player_2 = player

        # TODO some sort of start game message here for the server.

    # Removes a player from the game. If the player is not already added to the
    # game, it raises a PlayerNotLoggedIn exception
    def remove_player(self, player):
        if player.uuid == self.player_1.uuid:
            self.player_1 = None
        elif player.uuid == self.player_2.uuid:
            self.player_2 = None
        else:
            raise PlayerNotLoggedIn("Cannot remove a player not added to game")

    # Recieves the current player, current piece position, new piece position
    # and its combination state (if it is a combined piece) and sends the required
    # info to the board object for validation. It then sends the outcome to the
    # function.
    # It also incrimens the moves for the player moving the piece and checks
    # that the endgame condition has been reached.
    def move_piece(self, requesting_player_uuid, curr_pos, new_pos, combination_state = None):
        player = self.player_1 if self.player_1_turn else self.player_2

        if player.uuid != requesting_player_uuid:
            raise NotCurrentPlayerTryingToMoveException("The wrong player was trying to move!")

        if self.player_1_turn:
            self.player_1_moves += 1
        else:
            self.player_2_moves += 1

        if self.player_2_moves == 10 and self.player_1_moves == 10:
            if self.player_1.score > self.player_2.score:
                self.winner = self.player_1.account_name
            else:
                self.winner = self.player_2.account_name

        self.board.move_piece(self.player_1_turn, curr_pos, new_pos, combination_state)
        self.player_1_turn = not self.player_1_turn

    # Allows the board to let the session know that a piece has been taken
    def piece_taken(self, piece):
        player = self.player_1 if self.player_1_turn else self.player_2
        player.score += 5

    # Send the current game state information to the front end.
    def get_game_state(self):
        # returns a list of players, their updated piece states and their scores
        game_state = self.board.get_board_state()

        game_state["player_1_uuid"] = self.player_1.uuid
        game_state["player_2_uuid"] = self.player_2.uuid

        game_state["current_player"] = self.player_1.uuid if self.player_1_turn else self.player_2.uuid

        game_state["player_1_score"] = self.player_1.score
        game_state["player_2_score"] = self.player_2.score

        game_state["winner"] = self.winner

        return game_state
