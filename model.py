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

    @staticmethod
    def _create_from_picture(consecutive_pieces_to_win, size, pieces):
        """
        @param size (columns, rows)
        @param pieces (Piece[])

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 2, 0,
        ... 0, 1, 1, 0,
        ... 1, 2, 2, 1])
        >>> print(m)
        0020
        0110
        1221
        >>> m.get_piece_at_opening(0, 0)
        1
        """
        model = Model(consecutive_pieces_to_win, size)
        index = 0
        for y in range(model.size_y - 1, -1, -1):
            for x in range(model.size_x):
                piece = pieces[index]
                model._set_piece_at_opening(piece, x, y)
                index += 1
        return model

    def get_piece_at_opening(self, x, y):
        """
        >>> m = Model(4, (3, 3))
        >>> m.get_piece_at_opening(0, 0)
        0

        >>> m.get_piece_at_opening(m.size_x - 1, m.size_y - 1)
        0

        >>> m._set_piece_at_opening(Piece.PLAYER1, 1, 0)
        >>> m.get_piece_at_opening(1, 0)
        1

        >>> m.get_piece_at_opening(-1, -1)
        Traceback (most recent call last):
        ValueError: Invalid position (-1,-1)

        >>> m.get_piece_at_opening(m.size_x - 1, m.size_y)
        Traceback (most recent call last):
        ValueError: Invalid position (2,3)
        """
        self._validate_opening(x, y)
        return self._openings[x][y]

    def _get_piece_at_opening_or_none(self, x, y):
        """
        Same as get_piece_at_opening, but returns Piece.NONE if (x,y) is an invalid position.

        >>> m = Model(4, (3, 3))
        >>> m._get_piece_at_opening_or_none(0, 0)
        0

        >>> m._get_piece_at_opening_or_none(m.size_x - 1, m.size_y - 1)
        0

        >>> m._set_piece_at_opening(Piece.PLAYER1, 1, 0)
        >>> m._get_piece_at_opening_or_none(1, 0)
        1

        >>> m._get_piece_at_opening_or_none(-1, -1)
        0

        >>> m._get_piece_at_opening_or_none(m.size_x - 1, m.size_y)
        0
        """
        if self._is_valid_opening(x, y):
            return self._openings[x][y]
        else:
            return Piece.NONE

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
            if self._check_for_win(piece, x, y):
                self._on_player_won(piece)
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

    def _is_valid_opening(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def _validate_opening(self, x, y):
        if not self._is_valid_opening(x, y):
            raise ValueError('Invalid position ({},{})'.format(x, y))

    def _check_for_win(self, piece, piece_x, piece_y):
        """
        Checks for a win caused by a piece being placed at (piece_x, piece_y).
        @param piece (Piece) The piece being placed.
        @param piece_x,piece_y (Numbers) The position of the piece.
        @return True if the player of the piece wins.

        Horizontal checks:
        -----------------------------------------------------------------------
        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 0, 0)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 1, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 0, 0)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 1, 1, 0])
        >>> m._check_for_win(Piece.PLAYER1, 0, 0)
        True

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 1, 1, 0])
        >>> m._check_for_win(Piece.PLAYER1, 3, 0)
        True

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 1, 1, 0])
        >>> m._check_for_win(Piece.PLAYER2, 0, 0)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 1, 0)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 0, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 1, 0)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 0, 1, 0])
        >>> m._check_for_win(Piece.PLAYER1, 1, 0)
        True

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 1, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 2, 0)
        True

        Vertical checks:
        -----------------------------------------------------------------------
        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 0, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 0, 1)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 2, 0, 0, 0,
        ... 1, 0, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 0, 2)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 1, 0, 0, 0,
        ... 1, 0, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 0, 2)
        True

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 2,
        ... 0, 0, 0, 2])
        >>> m._check_for_win(Piece.PLAYER2, 3, 2)
        True

        Diagonal checks:
        -----------------------------------------------------------------------
        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 2, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 1, 1)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 1, 2, 0,
        ... 1, 2, 2, 1])
        >>> m._check_for_win(Piece.PLAYER1, 2, 2)
        True

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 1, 0,
        ... 0, 1, 2, 0,
        ... 0, 2, 2, 1])
        >>> m._check_for_win(Piece.PLAYER1, 0, 0)
        True

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 1, 0, 0,
        ... 0, 2, 0, 0,
        ... 0, 1, 2, 1])
        >>> m._check_for_win(Piece.PLAYER1, 0, 1)
        False

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 1, 0, 0,
        ... 0, 2, 0, 0,
        ... 0, 1, 2, 1])
        >>> m._check_for_win(Piece.PLAYER1, 2, 1)
        True
        """
        for slope_x, slope_y in ((1,0), (0,1), (1,1), (1,-1)):
            for start_x, start_y in ((piece_x - slope_x*i, piece_y - slope_y*i) for i in range(self.consecutive_pieces_to_win)):
                won = True
                for delta_x, delta_y in ((slope_x*i, slope_y*i) for i in range(self.consecutive_pieces_to_win)):
                    x = start_x + delta_x
                    y = start_y + delta_y
                    # Don't need to check the piece that is being placed
                    if (x, y) == (piece_x, piece_y):
                        continue
                    current_piece = self._get_piece_at_opening_or_none(x, y)
                    if current_piece != piece:
                        won = False
                        break
                if won:
                    return True

        return False

    def _on_player_won(self, piece):
        if piece == Piece.PLAYER1:
            self._game_state = GameState.PLAYER1_WON
        else:
            self._game_state = GameState.PLAYER2_WON

    def get_state(self):
        return self._game_state

    def __str__(self):
        """
        >>> m = Model(3, (4, 3))
        >>> print(m)
        0000
        0000
        0000

        >>> m._set_piece_at_opening(Piece.PLAYER1, 0, 0)
        >>> m._set_piece_at_opening(Piece.PLAYER2, 1, 0)
        >>> m._set_piece_at_opening(Piece.PLAYER2, 2, 0)
        >>> m._set_piece_at_opening(Piece.PLAYER1, 3, 0)
        >>> m._set_piece_at_opening(Piece.PLAYER1, 1, 1)
        >>> m._set_piece_at_opening(Piece.PLAYER1, 2, 1)
        >>> m._set_piece_at_opening(Piece.PLAYER2, 2, 2)
        >>> print(m)
        0020
        0110
        1221
        """
        string = ''
        for y in range(self.size_y-1, -1, -1):
            for x in range(self.size_x):
                piece = self._openings[x][y]
                string += str(piece)
            if y > 0:
                string += '\n'
        return string

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()
