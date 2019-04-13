class Piece:
    move_sets = {
        "Rook": [(1, 1), ...],
        "Knight": [(1, 1), ...],
        "Bishop": [(1, 1), ...]
    }

    def __init__(self, initial_combinations):
        self.combination_states = {
            "Rook": 0,
            "Knight": 0,
            "Bishop": 0,
            **initial_combinations
        }
