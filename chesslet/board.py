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
                position = Point(position_offset if i == 0 else self.board_size - 1 - position_offset, self.board_size - 1)
                self.add_piece({piece_type}, position, True)
            # Player 2
            for i in range(2):
                position = Point(position_offset if i == 0 else self.board_size - 1 - position_offset, 0)
                self.add_piece({piece_type}, position, False)

        self.update_valid_move_positions()

    def add_piece(self, combination_state, position, player_1):
        new_piece = Piece(combination_state, position)
        (self.player_1_pieces if player_1 else self.player_2_pieces).append(new_piece)
        self.board[position.x][position.y] = new_piece
        return new_piece

    def update_valid_move_positions(self):
        for piece in (self.player_1_pieces + self.player_2_pieces):
            # Clears all previous valid positions
            for piece_type in self.piece_types:
                piece.valid_move_positions[piece_type].clear()
            # Generates new valid positions based on updated board
            # and piece combination state
            for piece_type in piece.combination_state:
                for move_ray in piece.move_sets[piece_type]:
                    for offset in move_ray:
                        new_pos = piece.position + offset
                        # If the new_pos is outside the board, the ray ends before appending
                        if 0 <= new_pos.x < self.board_size and 0 <= new_pos.y < self.board_size:
                            piece.valid_move_positions[piece_type].append(new_pos)
                            # If the new_pos contains a piece, the ray ends after appending
                            if self.board[new_pos.x][new_pos.y] is not None: break
                        else: break

    def move_piece(self, player_1_turn, curr_pos, new_pos, combination_state = None):
        # Curr_pos within board bounds
        if curr_pos.x < 0 or curr_pos.x > self.board_size - 1 or new_pos.y < 0 or new_pos.y > self.board_size - 1:
            raise InvalidMoveException

        # Curr_pos contains a piece
        piece = self.board[curr_pos.x][curr_pos.y]
        if piece is None:
            raise InvalidPieceSelectionException

        # The combination_state (if supplied) is contained within piece's combination_state
        if combination_state is None:
            combination_state = piece.combination_state.copy()
        else:
            if not piece.combination_state >= combination_state:
                raise InvalidPieceSelectionException

        player_piece_list = self.player_1_pieces if player_1_turn else self.player_2_pieces

        # Piece is within the correct player list
        if piece not in player_piece_list:
            raise InvalidPieceSelectionException

        # New_pos is a valid move
        found = False
        for piece_type in combination_state:
            if new_pos in piece.valid_move_positions[piece_type]:
                found = True
                break
        if not found:
            raise InvalidMoveException

        other_piece = self.board[new_pos.x][new_pos.y]

        # If the supplied combination_state is not the same as
        # the piece's, it attempts to split the piece 
        moved_piece = None
        if piece.combination_state == combination_state:
            moved_piece = piece
            moved_piece.position = new_pos
            self.board[curr_pos.x][curr_pos.y] = None
        else:
            moved_piece = piece.split_piece(combination_state, new_pos)
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
        
        self.update_valid_move_positions()

    def get_board_state(self):
        board_state = {"player_1": [], "player_2": []}
        for piece in self.player_1_pieces:
            board_state["player_1"].append({"position": piece.position,
            "combination_state": piece.combination_state,
            "valid_move_positions": piece.valid_move_positions})

        for piece in self.player_2_pieces:
            board_state["player_2"].append({"position": piece.position,
            "combination_state": piece.combination_state,
            "valid_move_positions": piece.valid_move_positions})

        return board_state

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