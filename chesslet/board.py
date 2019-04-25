import itertools

from chesslet.point import Point
from chesslet.piece import Piece


class InvalidMoveException(Exception):
    pass

class InvalidPieceSelectionException(Exception):
    pass

class Board:
    board_size = 6
    piece_types = ("Rook", "Bishop", "Knight")

    def __init__(self, session, empty=False):
        # Creates the board matrix and fills it with None
        self.session = session
        self.board = []
        for i in range(self.board_size):
            self.board.append([None] * Board.board_size)

        self.player_1_pieces = []
        self.player_2_pieces = []

        if empty:
            return

        # Creates the pieces, adds them to the board and the player lists
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

    def calculate_valid_move_positions(self, combination_state, pos, player_piece_list):
        move_set = Piece.get_move_set(combination_state)
        valid_move_positions = []
        for move_ray in move_set:
            for offset in move_ray:
                new_pos = pos + offset
                # If the new_pos is outside the board, the ray ends before appending
                if 0 <= new_pos.x < self.board_size and 0 <= new_pos.y < self.board_size:
                    valid_move_positions.append(new_pos)
                    # If the new_pos contains a piece, the ray ends after appending
                    if self.board[new_pos.x][new_pos.y] is not None: break
                else: break
        return valid_move_positions

    def move_piece(self, player_1_turn, curr_pos, new_pos, combination_state = None):
        # Curr_pos within board bounds
        if curr_pos.x < 0 or curr_pos.x > self.board_size - 1 or new_pos.y < 0 or new_pos.y > self.board_size - 1:
            raise InvalidMoveException

        # Curr_pos contains a piece
        piece = self.board[curr_pos.x][curr_pos.y]
        if piece is None:
            raise InvalidPieceSelectionException

        # The combination_state (if supplied) is contained within piece's combintion_state
        if combination_state is None:
            combination_state = piece.combination_state.copy()
        else:
            if not piece.contains_state(combination_state):
                raise InvalidPieceSelectionException

        player_piece_list = self.player_1_pieces if player_1_turn else self.player_2_pieces

        # Piece is within the correct player list
        if piece not in player_piece_list:
            raise InvalidPieceSelectionException

        # New_pos is a valid move
        if new_pos not in self.calculate_valid_move_positions(combination_state, curr_pos, player_piece_list):
            raise InvalidMoveException

        other_piece = self.board[new_pos.x][new_pos.y]

        # If the supplied combination_state is not the same as
        # the piece's, it attempts to split the piece 
        moved_piece = None
        if piece.combination_state == combination_state:
            moved_piece = piece
            self.board[curr_pos.x][curr_pos.y] = None
        else:
            moved_piece = piece.split_piece(combination_state)
            player_piece_list.append(moved_piece)
                        
        if other_piece is None:
            self.board[new_pos.x][new_pos.y] = moved_piece
        else:
            # Checks whether move will result in a combination
            # or a piece taken
            if other_piece in player_piece_list:
                # Combines the piece into the other_piece
                other_piece.combine_piece(moved_piece.combination_state)
                player_piece_list.remove(moved_piece)
            else:
                self.board[new_pos.x][new_pos.y] = moved_piece

                # Other_piece gets taken
                (self.player_2_pieces if player_1_turn else self.player_1_pieces).remove(other_piece)
                self.session.piece_taken(other_piece)

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