from types import ModuleType
from typing import Set, Tuple


class Piece:
    NONE = 0
    PLAYER1 = 1
    PLAYER2 = 2


class Model:
    def __init__(self, consecutive_pieces_to_win, size):
        """
        @param size (columns, rows)
        """
        self.consecutive_pieces_to_win = consecutive_pieces_to_win
        self.size_x, self.size_y = size
        self.reset_game()

    def reset_game(self):
        self.current_player_piece = Piece.PLAYER1
        self.winning_player = None
        self.winning_piece_positions = None
        self.drop_history = []
        self._initialize_board()

    def _initialize_board(self):
        self._openings = [[Piece.NONE for _ in range(self.size_y)] for _ in range(self.size_x)]

    def initialize_from_picture(self, pieces):
        """
        @param pieces (Piece[])
        """
        index = 0
        for y in range(self.size_y - 1, -1, -1):
            for x in range(self.size_x):
                piece = pieces[index]
                self._set_piece_at_opening(piece, x, y)
                index += 1

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
        model.initialize_from_picture(pieces)
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
        if y < 0:
            raise RuntimeError('Cannot drop piece at column {} because it is full.'.format(x))

        self._set_piece_at_opening(piece, x, y)
        self.drop_history.append((piece, x, y))

        winning_piece_positions = self._check_for_win(piece, x, y)
        if winning_piece_positions:
            self._on_player_won(piece, winning_piece_positions)

        if self._is_tie():
            self._on_tie()

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

    def end_turn(self):
        """
        End the current player's turn and move on to the next player.
        """
        if self.current_player_piece == Piece.PLAYER1:
            self.current_player_piece = Piece.PLAYER2
        elif self.current_player_piece == Piece.PLAYER2:
            self.current_player_piece = Piece.PLAYER1
        else:
            raise RuntimeError('Invalid current player piece')

    def _check_for_win(self, piece, piece_x, piece_y):
        """
        Checks for a win caused by a piece being placed at (piece_x, piece_y).
        @param piece (Piece) The piece being placed.
        @param piece_x,piece_y (Numbers) The position of the piece.
        @return [(winning_piece_1_x, winning_piece_1_y), (winning_piece_2_x, winning_piece_2_y), ...]
            if the player of the piece wins.  False otherwise.

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
        [(0, 0), (1, 0), (2, 0)]

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 0, 1, 1, 0])
        >>> m._check_for_win(Piece.PLAYER1, 3, 0)
        [(1, 0), (2, 0), (3, 0)]

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
        [(0, 0), (1, 0), (2, 0)]

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 1, 0, 0])
        >>> m._check_for_win(Piece.PLAYER1, 2, 0)
        [(0, 0), (1, 0), (2, 0)]

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 0,
        ... 1, 1, 0, 1])
        >>> m._check_for_win(Piece.PLAYER1, 2, 0)
        [(0, 0), (1, 0), (2, 0), (3, 0)]

        >>> m = Model._create_from_picture(3, (5, 3), [
        ... 0, 0, 0, 0, 0,
        ... 0, 0, 0, 0, 0,
        ... 1, 1, 0, 1, 1])
        >>> m._check_for_win(Piece.PLAYER1, 2, 0)
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]

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
        [(0, 0), (0, 1), (0, 2)]

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 0, 0,
        ... 0, 0, 0, 2,
        ... 0, 0, 0, 2])
        >>> m._check_for_win(Piece.PLAYER2, 3, 2)
        [(3, 0), (3, 1), (3, 2)]

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
        [(0, 0), (1, 1), (2, 2)]

        >>> m = Model._create_from_picture(3, (4, 3), [
        ... 0, 0, 1, 0,
        ... 0, 1, 2, 0,
        ... 0, 2, 2, 1])
        >>> m._check_for_win(Piece.PLAYER1, 0, 0)
        [(0, 0), (1, 1), (2, 2)]

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
        [(1, 2), (2, 1), (3, 0)]

        >>> m = Model._create_from_picture(3, (4, 4), [
        ... 2, 0, 0, 0,
        ... 1, 0, 1, 0,
        ... 1, 2, 2, 0,
        ... 2, 1, 1, 2])
        >>> m._check_for_win(Piece.PLAYER2, 1, 2)
        [(0, 3), (1, 2), (2, 1), (3, 0)]

        >>> m = Model._create_from_picture(3, (4, 4), [
        ... 2, 0, 0, 2,
        ... 1, 1, 0, 1,
        ... 1, 2, 2, 1,
        ... 2, 1, 1, 2])
        >>> m._check_for_win(Piece.PLAYER2, 2, 2)
        [(0, 0), (1, 1), (2, 2), (3, 3)]
        """
        for slope_x, slope_y in ((1,0), (0,1), (1,1), (1,-1)):
            for start_x, start_y in ((piece_x - slope_x*i, piece_y - slope_y*i) for i in range(self.consecutive_pieces_to_win)):
                winning_piece_positions = []
                for x, y in ((start_x + slope_x*i, start_y + slope_y*i)
                             for i in range(self.consecutive_pieces_to_win)):
                    winning_piece_positions.append((x, y))
                    # Don't need to check the piece that is being placed
                    if (x, y) == (piece_x, piece_y):
                        continue
                    current_piece = self._get_piece_at_opening_or_none(x, y)
                    if current_piece != piece:
                        winning_piece_positions = None
                        break
                if winning_piece_positions:
                    # Check if there are additional winning pieces that exceed the number required to win.
                    # e.g. a 5-in-a-row when only 4 are required
                    if slope_x != 0:
                        num_previous_pieces_to_check = self.consecutive_pieces_to_win + (start_x - piece_x)
                        for x, y in ((start_x - slope_x*i, start_y - slope_y*i)
                                     for i in range(1, 1 + num_previous_pieces_to_check)):
                            current_piece = self._get_piece_at_opening_or_none(x, y)
                            if current_piece == piece:
                                winning_piece_positions.insert(0, (x, y))
                            else:
                                break
                    return winning_piece_positions

        return False

    def _is_tie(self):
        """
        @return True if the current board state is a tie.  This is the same as the board being full.  False otherwise.

        >>> m = Model._create_from_picture(3, (3, 3), [
        ... 0, 0, 0,
        ... 0, 0, 0,
        ... 0, 0, 0])
        >>> m._is_tie()
        False

        >>> m = Model._create_from_picture(3, (3, 3), [
        ... 1, 1, 0,
        ... 2, 2, 1,
        ... 1, 1, 2])
        >>> m._is_tie()
        False

        >>> m = Model._create_from_picture(3, (3, 3), [
        ... 1, 1, 2,
        ... 2, 2, 1,
        ... 1, 1, 2])
        >>> m._is_tie()
        True
        """
        for y in range(self.size_y):
            for x in range(self.size_x):
                piece = self.get_piece_at_opening(x, y)
                if piece == Piece.NONE:
                    return False
        return True

    def _on_player_won(self, piece, winning_piece_positions):
        """
        @param winning_piece_positions [(winning_piece_1_x, winning_piece_1_y), (winning_piece_2_x, winning_piece_2_y), ...]
        """
        self.winning_player = piece
        self.winning_piece_positions =  winning_piece_positions

    def _on_tie(self):
        self.winning_player = Piece.NONE

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


def run_tests(headless: bool) -> Tuple[Tuple[int, int], Set[ModuleType]]:
    """
    @return ((failure_count, test_count), tested_modules)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[], headless=headless)


if __name__ == '__main__':
    run_tests(headless=False)
