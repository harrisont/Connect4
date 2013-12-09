class Piece:
    NONE = 0
    PLAYER1 = 1
    PLAYER2 = 2

class GameState:
    PLAYING = 0
    PLAYER1_WON = 1
    PLAYER2_WON = 2

class Model:
    def __init__(self, consecutive_pieces_to_win, size):
        """
        @param size (columns, rows)
        """
        self.consecutive_pieces_to_win = consecutive_pieces_to_win
        self.size_x, self.size_y = size
        self._initialize_board()
        self._game_state = GameState.PLAYING

    def _initialize_board(self):
        self._openings = [[Piece.NONE for y in range(self.size_y)] for x in range(self.size_x)]

    def get_piece_at_opening(self, x, y):
        """
        >>> m = Model(4, (3, 3))
        >>> m.get_piece_at_opening(0, 0)
        0

        >>> m.get_piece_at_opening(m.size_x - 1, m.size_y - 1)
        0

        >>> m.get_piece_at_opening(-1, -1)
        Traceback (most recent call last):
        ValueError: Invalid position (-1,-1)

        >>> m.get_piece_at_opening(m.size_x - 1, m.size_y)
        Traceback (most recent call last):
        ValueError: Invalid position (2,3)
        """
        self._validate_opening(x, y)
        return self._openings[x][y]

    def is_column_full(self, x):
        """
        >>> m = Model(4, (2, 2))
        >>> m.is_column_full(0)
        False
        >>> m.drop_piece(Piece.PLAYER1, 0)
        >>> m.is_column_full(0)
        False
        >>> m.drop_piece(Piece.PLAYER2, 0)
        >>> m.is_column_full(0)
        True
        """
        top_row = self.size_y - 1
        return self.get_piece_at_opening(x, top_row) != Piece.NONE

    def drop_piece(self, piece, x):
        """
        @param piece (Piece)
        >>> m = Model(4, (4, 2))

        >>> m.drop_piece(Piece.NONE, 2)
        Traceback (most recent call last):
        ValueError: Invalid piece

        >>> m.drop_piece(Piece.PLAYER1, 2)
        >>> m.get_piece_at_opening(2, 0)
        1
        >>> m.get_piece_at_opening(2, 1)
        0
        >>> m.get_piece_at_opening(1, 0)
        0
        >>> m.get_piece_at_opening(3, 0)
        0

        >>> m.drop_piece(Piece.PLAYER2, 2)
        >>> m.get_piece_at_opening(2, 0)
        1
        >>> m.get_piece_at_opening(2, 1)
        2
        >>> m.get_piece_at_opening(1, 0)
        0
        >>> m.get_piece_at_opening(3, 0)
        0

        >>> m.drop_piece(Piece.PLAYER1, 1)
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

        >>> m.drop_piece(Piece.PLAYER1, 2)
        Traceback (most recent call last):
        RuntimeError: Cannot drop piece at column 2 because it is full.
        """
        if piece == Piece.NONE:
            raise ValueError('Invalid piece')

        y = self.get_drop_row(x)
        if y >= 0:
            self._set_piece_at_opening(piece, x, y)
        else:
            raise RuntimeError('Cannot drop piece at column {} because it is full.'.format(x))

    def get_drop_row(self, x):
        """
        @return the y-location that the piece would end up at, or -1 if the column is full
        """
        for y in range(self.size_y):
            if self.get_piece_at_opening(x, y) == Piece.NONE:
                return y
        return -1

    def _set_piece_at_opening(self, piece, x, y):
        """
        @param piece (Piece)
        """
        self._validate_opening(x, y)
        self._openings[x][y] = piece

    def _validate_opening(self, x, y):
        if not (0 <= x < self.size_x and 0 <= y < self.size_y):
            raise ValueError('Invalid position ({},{})'.format(x, y))

    def get_state(self):
        return self._game_state

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()
