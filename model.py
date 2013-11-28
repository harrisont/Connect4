class ColumnFullError(Exception):
    pass

class Piece:
    none = 0
    player1 = 1
    player2 = 2

class Model:
    def __init__(self, size):
        """
        @param size (columns, rows)
        """
        self.size_x, self.size_y = size
        self._initialize_board()

    def _initialize_board(self):
        self._openings = [[Piece.none for y in range(self.size_y)] for x in range(self.size_x)]

    def get_piece_at_opening(self, x, y):
        """
        >>> m = Model((3, 3))
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
        self._validate_opening(x, y)
        return self._openings[x][y]

    def drop_piece(self, piece, x):
        """
        @param piece (Piece)

        >>> m = Model((4, 2))
        >>> m.drop_piece(Piece.player1, 2)
        >>> m.get_piece_at_opening(2, 0)
        1
        >>> m.get_piece_at_opening(2, 1)
        0
        >>> m.get_piece_at_opening(1, 0)
        0
        >>> m.get_piece_at_opening(3, 0)
        0
        >>> m.drop_piece(Piece.player2, 2)
        >>> m.get_piece_at_opening(2, 0)
        1
        >>> m.get_piece_at_opening(2, 1)
        2
        >>> m.get_piece_at_opening(1, 0)
        0
        >>> m.get_piece_at_opening(3, 0)
        0
        >>> m.drop_piece(Piece.player1, 1)
        >>> m.get_piece_at_opening(1, 0)
        1
        >>> m.get_piece_at_opening(1, 1)
        0
        >>> m.get_piece_at_opening(2, 0)
        1
        >>> m.get_piece_at_opening(2, 1)
        2
        >>> m.get_piece_at_opening(3, 0)
        0
        >>> m.drop_piece(Piece.player1, 2)
        Traceback (most recent call last):
        ColumnFullError
        """
        for y in range(self.size_y):
            if self.get_piece_at_opening(x, y) == Piece.none:
                self._set_piece_at_opening(piece, x, y)
                return
        raise ColumnFullError

    def _set_piece_at_opening(self, piece, x, y):
        """
        @param piece (Piece)
        """
        self._validate_opening(x, y)
        self._openings[x][y] = piece

    def _validate_opening(self, x, y):
        if not (0 <= x < self.size_x and 0 <= y < self.size_y):
            raise ValueError('Invalid position')

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()
