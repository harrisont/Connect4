import model
import pygame

class ViewState:
    PLAYING = 1
    GAME_OVER = 2

class View:
    _WINDOW_SIZE_X = 1024
    _WINDOW_SIZE_Y = 768

    _FONT_SIZE = 36

    _BACKGROUND_COLOR = pygame.Color(128, 128, 128)

    _BOARD_COLOR = pygame.Color(0, 116, 179)
    _PIECE_COLORS = [
        _BACKGROUND_COLOR,
        pygame.Color(200, 0, 0),
        pygame.Color(10, 10, 10)]
    _POTENTIAL_PIECE_COLORS = [
        _BACKGROUND_COLOR,
        pygame.Color(164, 64, 64),
        pygame.Color(69, 69, 69)]
    _WINNING_PIECES_LINE_COLOR = pygame.Color(30, 200, 30)
    _BOARD_MARGIN = 50
    _BOARD_OPENING_RADIUS = 40
    _BOARD_OPENING_MARGIN = 15

    def __init__(self, view_model, key_map):
        self.reset()
        self._model = view_model
        self._key_map = key_map

        pygame.init()
        pygame.display.set_caption('Connect Four')
        self._fps_clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

        self._screen = pygame.display.set_mode((self._WINDOW_SIZE_X, self._WINDOW_SIZE_Y), pygame.DOUBLEBUF)

    def reset(self):
        self._state = ViewState.PLAYING

    def draw(self, drop_x):
        self._screen.fill(self._BACKGROUND_COLOR)

        self._draw_board()

        if self._state == ViewState.PLAYING:
            self._draw_drop_location(drop_x)
        elif self._state == ViewState.GAME_OVER:
            self._draw_won_message()

        pygame.display.flip()

    def _draw_board(self):
        board_rect = self._get_board_rect()
        pygame.draw.rect(self._screen, self._BOARD_COLOR, board_rect, 0)

        for x in range(self._model.size_x):
            for y in range(self._model.size_y):
                piece = self._model.get_piece_at_opening(x, y)
                self._draw_piece(piece, x, y)

    def _draw_piece(self, piece, x, y, potential_piece=False):
        """
        @param potential_piece (Boolean) if True, draws the piece as a potential piece
        """
        color = self._get_piece_color(piece, potential_piece)
        opening_center = self._get_opening_center(x, y)
        pygame.draw.circle(self._screen, color, opening_center, self._BOARD_OPENING_RADIUS)

    def _draw_drop_location(self, drop_x):
        self._draw_piece(self._model.current_player_piece, drop_x, self._model.size_y)

        drop_y = self._model.get_drop_row(drop_x)
        if drop_y >= 0:
            self._draw_piece(self._model.current_player_piece, drop_x, drop_y, potential_piece=True)

    def _get_board_position(self):
        return (self._BOARD_MARGIN, self._BOARD_MARGIN)

    def _get_board_rect(self):
        """Returns the (left, top, width, height) of the board."""
        board_x, board_y = self._get_board_position()
        size_per_opening = self._BOARD_OPENING_MARGIN + 2*self._BOARD_OPENING_RADIUS
        return (board_x,
                board_y,
                self._BOARD_OPENING_MARGIN + self._model.size_x * size_per_opening,
                self._BOARD_OPENING_MARGIN + self._model.size_y * size_per_opening)

    def _get_opening_center(self, x, y):
        board_x, board_y = self._get_board_position()
        flipped_y = self._model.size_y - y - 1
        return (board_x + (x+1) * self._BOARD_OPENING_MARGIN + (2*x + 1) * self._BOARD_OPENING_RADIUS,
                board_y + (flipped_y+1) * self._BOARD_OPENING_MARGIN + (2*flipped_y + 1) * self._BOARD_OPENING_RADIUS)

    def _get_piece_color(self, piece, potential_piece):
        if potential_piece:
            return self._POTENTIAL_PIECE_COLORS[piece]
        else:
            return self._PIECE_COLORS[piece]

    def _draw_won_message(self):
        self._draw_player_won_message()
        self._draw_winning_pieces(self._model.winning_piece_positions)

    def _draw_player_won_message(self):
        message = self._get_player_won_message()
        message_color = pygame.Color(255, 255, 255)
        message_surface = self._font.render(message, True, message_color)
        message_rect = message_surface.get_rect()
        message_rect.topleft = (5, 5)
        self._screen.blit(message_surface, message_rect)

    def _get_player_won_message(self):
        winning_player = self._model.winning_player
        return 'Player {} Won! Press "{}" to play again.'.format(
            winning_player,
            pygame.key.name(self._key_map['new_game']))

    def _draw_winning_pieces(self, winning_piece_positions):
        """
        @param winning_piece_positions [(winning_piece_1_x, winning_piece_1_y), (winning_piece_2_x, winning_piece_2_y), ...]
        """
        color = self._WINNING_PIECES_LINE_COLOR
        line_start = self._get_opening_center(*winning_piece_positions[0])
        line_end = self._get_opening_center(*winning_piece_positions[-1])
        line_width = self._BOARD_OPENING_RADIUS // 4
        pygame.draw.line(self._screen, color, line_start, line_end, line_width)

    def tick(self):
        # Wait long enough to run at 30 FPS.
        self._fps_clock.tick(30)

        winning_player = self._model.winning_player
        if winning_player:
            self._state = ViewState.GAME_OVER

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[model])

if __name__ == '__main__':
    run_tests()