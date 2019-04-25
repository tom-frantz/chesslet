from chesslet.point import Point


class InvalidCombinationStateException(Exception):
    pass


class Piece:
    move_sets = {
        "Rook": [[Point(0, 1), Point(0, 2)], [Point(1, 0), Point(2, 0)], [Point(0, -1), Point(0, -2)], [Point(-1, 0), Point(-2, 0)]],
        "Bishop": [[Point(1, 1), Point(2, 2)], [Point(1, -1), Point(2, -2)], [Point(-1, -1), Point(-2, -2)], [Point(-1, 1), Point(-2, 2)]],
        "Knight": [[Point(1, 2)], [Point(2, 1)], [Point(2, -1)], [Point(1, -2)], [Point(-1, -2)], [Point(-2, -1)], [Point(-2, 1)], [Point(-1, 2)]]
    }

    def __init__(self, combination_state):
        # Checks to see if values within initial_combination are valid
        if not combination_state.keys() <= Piece.move_sets.keys(): raise InvalidCombinationStateException
        self.combination_state = {
            "Rook": 0,
            "Bishop": 0,
            "Knight": 0,
            **combination_state
        }

    def __str__(self):
        piece_key = None
        for key, value in self.combination_state.items():
            if value > 0:
                if piece_key is not None:
                    return "C"
                piece_key = key[0]
        return piece_key

    def __repr__(self):
        return str(self.combination_state)

    def contains_state(self, combination_state):
        for piece_type in combination_state:
            if self.combination_state[piece_type] < combination_state[piece_type]:
                return False
        return True

    def is_empty(self):
        for piece_type in self.combination_state:
            if self.combination_state[piece_type] > 0:
                return False
        return True

    def combine_piece(self, combination_state):
        for piece_type in combination_state:
            self.combination_state[piece_type] += combination_state[piece_type]

    def split_piece(self, combination_state):
        # Checks the splitting state is contained within the current
        # state before altering 
        for piece_type in combination_state:
            if self.combination_state[piece_type] < combination_state[piece_type]:
                raise InvalidCombinationStateException
        for piece_type in combination_state:
            self.combination_state[piece_type] -= combination_state[piece_type]
        return Piece(combination_state)    

    @classmethod
    def get_move_set(cls, combination_state):
        move_set = []
        for piece_type in combination_state:
            if combination_state[piece_type] > 0:
                for move_ray in Piece.move_sets[piece_type]:
                    move_set.append(move_ray)
        return move_set


