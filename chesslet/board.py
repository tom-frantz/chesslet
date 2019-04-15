from chesslet.point import Point
from chesslet.piece import Piece

class InvalidMoveException(Exception):
    pass

class InvalidPieceSelectionException(Exception):
    pass

class Board:
    board_size = 6
    piece_types = {"Rook", "Bishop", "Knight"} # Will this preserve order?
    # Do we want to access the board with [x][y] or [y][x]?

    def __init__(self, empty=False):
        # Creates the board matrix and fills it with None
        self.board = []
        for i in range(self.board_size):
            self.board.append([None] * 5)
        if empty: return

        # Creates the pieces, adds them to the board and the player lists
        self.player_1_uuid = None
        self.player_2_uuid = None
        self.player_1_pieces = []
        self.player_2_pieces = []
        position_offset = 0
        for piece_type in self.piece_types:
            # Player 1
            for i in [0, 1]:
                new_piece = Piece({piece_type : 1})
                self.player_1_pieces.append(new_piece)
                position = position_offset if i == 0 else self.board_size - 1 - position_offset
                self.board[position][0] = new_piece
            # Player 2
            for i in [0, 1]:
                new_piece = Piece({piece_type : 1})
                self.player_2_pieces.append(new_piece)
                position = position_offset if i == 0 else self.board_size - 1 - position_offset
                self.board[position][self.board_size - 1] = new_piece

    def calculate_valid_move_positions(self, piece, pos):
        move_set = piece.get_move_set()
        valid_move_positions = []
        for move_ray in move_set:
            for offset in move_ray:
                # All previous positions in the ray must be valid for the current position to be valid
                new_pos = pos + offset
                if 0 <= new_pos.x <= self.board_size and 0 <= new_pos.y <= self.board_size \
                and self.board[new_pos.x][new_pos.y] == None:
                    valid_move_positions.append(new_pos)
                else: break

        return valid_move_positions

    def move_piece(self, player, curr_pos, new_pos):
        if curr_pos.x < 0 or curr_pos.x > self.board_size - 1 or new_pos.y < 0 or new_pos.y > self.board_size - 1:
            raise InvalidMoveException

        piece = self.board[curr_pos.x][curr_pos.y]
        if piece is None:
            raise InvalidMoveException

        player_piece_list = self.player_1_pieces if player.uuid == self.player_1_uuid else self.player_2_pieces

        if piece not in player_piece_list:
            raise InvalidPieceSelectionException

        move_positions = self.calculate_valid_move_positions(piece, curr_pos)
        if new_pos not in move_positions:
            raise InvalidMoveException

        other_piece = self.board[new_pos.x][new_pos.y]

        if other_piece is not None:
            if other_piece in player_piece_list:
                raise InvalidMoveException

        self.board[curr_pos.x][curr_pos.y] = None
        self.board[new_pos.x][new_pos.y] = piece

        return other_piece
