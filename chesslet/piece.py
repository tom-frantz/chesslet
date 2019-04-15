from chesslet.point import Point


class InvalidCombinationStateException(Exception):
    pass


class Piece:
    move_sets = {
        "Rook": [[Point(0, 1), Point(0, 2)], [Point(1, 0), Point(2, 0)], [Point(0, -1), Point(0, -2)], [Point(-1, 0), Point(-2, 0)]],
        "Bishop": [[Point(1, 1), Point(2, 2)], [Point(1, -1), Point(2, -2)], [Point(-1, -1), Point(-2, -2)], [Point(-1, 1), Point(-2, 2)]],
        "Knight": [[Point(1, 2)], [Point(2, 1)], [Point(2, -1)], [Point(1, -2)], [Point(-1, -2)], [Point(-2, -1)], [Point(-2, 1)], [Point(-1, 2)]]
    }

    def __init__(self, initial_combinations):
        # Checks to see if values within initial_combination are valid
        if not initial_combinations.keys() <= Piece.move_sets.keys(): raise InvalidCombinationStateException
        self.combination_state = {
            "Rook": 0,
            "Bishop": 0,
            "Knight": 0,
            **initial_combinations
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

    def combine_piece(self, piece_combination_state):
        for piece in piece_combination_state:
            self.combination_state[piece] += piece_combination_state[piece]

    def split_piece(self, piece_combination_state):
        # Checks the splitting state is contained within the current
        # state before altering 
        for piece in piece_combination_state:
            if self.combination_state[piece] == 0:
                raise InvalidCombinationStateException
        for piece in piece_combination_state:
            self.combination_state[piece] -= piece_combination_state[piece]        

    def get_move_set(self):
        move_set = []
        for piece in self.combination_state:
            if self.combination_state[piece] > 0:
                for move_ray in Piece.move_sets[piece]:
                    move_set.append(move_ray)
        return move_set


