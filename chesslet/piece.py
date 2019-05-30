from chesslet.point import Point


class InvalidCombinationStateException(Exception):
    pass


class Piece:
    move_sets = {
        "Rook": [[Point(0, 1), Point(0, 2)], [Point(1, 0), Point(2, 0)], [Point(0, -1), Point(0, -2)], [Point(-1, 0), Point(-2, 0)]],
        "Bishop": [[Point(1, 1), Point(2, 2)], [Point(1, -1), Point(2, -2)], [Point(-1, -1), Point(-2, -2)], [Point(-1, 1), Point(-2, 2)]],
        "Knight": [[Point(1, 2)], [Point(2, 1)], [Point(2, -1)], [Point(1, -2)], [Point(-1, -2)], [Point(-2, -1)], [Point(-2, 1)], [Point(-1, 2)]]
    }

    def __init__(self, combination_state, position):
        # Checks to see if values within combination_state are valid
        if not combination_state <= Piece.move_sets.keys():
            raise InvalidCombinationStateException

        # Ensures the combination_state is not empty
        if len(combination_state) == 0:
            raise InvalidCombinationStateException

        self.combination_state = combination_state
        self.position = position  # Point object
        self.valid_move_positions = {"Rook": [], "Bishop": [], "Knight": []}

    def __str__(self):
        piece_key = None
        for piece_type in self.combination_state:
            if piece_key is not None:
                return "C"
            piece_key = piece_type[0]
        return piece_key

    def __repr__(self):
        return str(self.combination_state)

    def combine_piece(self, combination_state):
        # Makes sure the combination state is valid
        if not combination_state < Piece.move_sets.keys():
            raise InvalidCombinationStateException

        # Makes sure the piece types in both combination states are different
        if not self.combination_state.isdisjoint(combination_state):
            raise InvalidCombinationStateException

        self.combination_state.update(combination_state)

    def split_piece(self, combination_state, new_pos):
        # Checks the splitting state is contained within the current
        # state before altering 
        if not self.combination_state > combination_state:
            raise InvalidCombinationStateException
        self.combination_state -= combination_state
        return Piece(combination_state, new_pos)


