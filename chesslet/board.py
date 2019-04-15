import itertools

from chesslet.point import Point
from chesslet.piece import Piece


class InvalidMoveException(Exception):
    pass

class InvalidPieceSelectionException(Exception):
    pass

class Board:
    board_size = 6
    piece_types = ("Rook", "Bishop", "Knight") # Will this preserve order?
    # Do we want to access the board with [x][y] or [y][x]?

    def __init__(self, empty=False):
        # Creates the board matrix and fills it with None
        self.board = []
        for i in range(self.board_size):
            self.board.append([None] * Board.board_size)
        
        # Creates the pieces, adds them to the board and the player lists
        self.player_1_uuid = None
        self.player_2_uuid = None
        self.player_1_pieces = []
        self.player_2_pieces = []

        if empty:
            return

        for position_offset, piece_type in enumerate(self.piece_types):
            # Player 1
            for i in range(2):
                new_piece = Piece({piece_type: 1})
                self.player_1_pieces.append(new_piece)
                position = position_offset if i == 0 else self.board_size - 1 - position_offset
                self.board[position][0] = new_piece
            # Player 2
            for i in range(2):
                new_piece = Piece({piece_type: 1})
                self.player_2_pieces.append(new_piece)
                position = position_offset if i == 0 else self.board_size - 1 - position_offset
                self.board[position][self.board_size - 1] = new_piece

    def calculate_valid_move_positions(self, piece, pos, player_move_list):
        move_set = piece.get_move_set()
        valid_move_positions = []
        for move_ray in move_set:
            for offset in move_ray:
                # All previous positions in the ray must be valid for the current position to be valid
                new_pos = pos + offset
                in_board = 0 <= new_pos.x < self.board_size and 0 <= new_pos.y < self.board_size
                try:
                    target_pos = self.board[new_pos.x][new_pos.y]
                    if in_board and (target_pos is None or target_pos not in player_move_list):
                        valid_move_positions.append(new_pos)
                        if target_pos is not None and target_pos not in player_move_list:
                            break
                    else:
                        break
                except Exception as e:
                    pass

        return valid_move_positions

    def move_piece(self, player_uuid, curr_pos, new_pos):
        if curr_pos.x < 0 or curr_pos.x > self.board_size - 1 or new_pos.y < 0 or new_pos.y > self.board_size - 1:
            raise InvalidMoveException

        piece = self.board[curr_pos.x][curr_pos.y]
        if piece is None:
            raise InvalidMoveException

        player_piece_list = self.player_1_pieces if player_uuid == self.player_1_uuid else self.player_2_pieces

        if piece not in player_piece_list:
            raise InvalidPieceSelectionException

        move_positions = self.calculate_valid_move_positions(piece, curr_pos, player_piece_list)
        if new_pos not in move_positions:
            raise InvalidMoveException

        other_piece = self.board[new_pos.x][new_pos.y]

        if other_piece is not None:
            if other_piece in player_piece_list:
                raise InvalidMoveException

        self.board[curr_pos.x][curr_pos.y] = None
        self.board[new_pos.x][new_pos.y] = piece

        return other_piece

    def __str__(self):
        """
        Return a string representation of the board.
        Player 1 should be lowercase.
        Player 2 should be uppercase.

        :return:
        """
        board = """  0 1 2 3 4 5\n"""

        for y in range(Board.board_size):
            board += str(y) + " "
            for x in range(Board.board_size):
                piece = self.board[x][y] if self.board[x][y] is not None else "."

                piece = str(piece).lower() if piece in self.player_1_pieces else str(piece)

                board += piece
                board += " "
            board += "\n"
        return board