class Piece:
    none = 0
    player1 = 1
    player2 = 2

class Model:
    _SIZE_X = 7
    _SIZE_Y = 6

    def __init__(self):
        self.size_x = self._SIZE_X
        self.size_y = self._SIZE_Y
        self._initialize_board()

    def _initialize_board(self):
        self._openings = [[Piece.none for y in range(self.size_y)] for x in range(self.size_x)]

    def get_piece_at_opening(self, x, y):
        """
        >>> m = Model()
        >>> m.get_piece_at_opening(0, 0)
        0
        >>> m.get_piece_at_opening(m.size_x - 1, m.size_y - 1)
        0
        >>> m.get_piece_at_opening(-1, -1)
        Traceback (most recent call last):
        ValueError: Invalid position
        >>> m.get_piece_at_opening(m.size_x - 1, m.size_y)
        Traceback (most recent call last):
        ValueError: Invalid position
        """
        if not (0 <= x < self.size_x and 0 <= y < self.size_y):
            raise ValueError('Invalid position')
        return self._openings[x][y]

    def drop_piece(self, piece, x):
        """
        @param piece (Piece)

        >>> m = Model()
        >>> m.get_piece_at_opening(2, 0)
        0
        >>> m.drop_piece(Piece.player1, 2)
        >>> m.get_piece_at_opening(2, 0)
        1
        """
        # TODO: actually drop the piece
        self._openings[x][0] = piece

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()
