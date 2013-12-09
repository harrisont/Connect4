import model
import pygame
import sys

class ViewState:
    PLAYING = 1
    GAME_OVER = 2

class View:
    _WINDOW_SIZE_X = 1024
    _WINDOW_SIZE_Y = 768

    _FONT_SIZE = 36

    _BACKGROUND_COLOR = pygame.Color(128, 128, 128)

    _BOARD_SIZE_X = 7
    _BOARD_SIZE_Y = 6
    _BOARD_COLOR = pygame.Color(0, 116, 179)
    _PIECE_COLORS = [
        _BACKGROUND_COLOR,
        pygame.Color(200, 0, 0),
        pygame.Color(10, 10, 10)]
    _POTENTIAL_PIECE_COLORS = [
        _BACKGROUND_COLOR,
        pygame.Color(164, 64, 64),
        pygame.Color(69, 69, 69)]
    _BOARD_MARGIN = 50
    _BOARD_OPENING_RADIUS = 40
    _BOARD_OPENING_MARGIN = 15

    _KEY_QUIT = pygame.K_ESCAPE
    _KEY_DROP_PIECE = pygame.K_DOWN
    _KEY_MOVE_LEFT = pygame.K_LEFT
    _KEY_MOVE_RIGHT = pygame.K_RIGHT

    def __init__(self):
        self._state = ViewState.PLAYING
        self._model = model.Model((self._BOARD_SIZE_X, self._BOARD_SIZE_Y))

        self._current_player_piece = model.Piece.PLAYER1
        self._drop_x = int(self._model.size_x / 2)

        pygame.init()
        pygame.display.set_caption('Connect Four')
        self._fps_clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

    def run(self):
        self.print_controls()

        self._screen = pygame.display.set_mode((self._WINDOW_SIZE_X, self._WINDOW_SIZE_Y), pygame.DOUBLEBUF)

        while True:
            self._handle_events()
            self._tick()
            self._draw()

            # Wait long enough to run at 30 FPS.
            self._fps_clock.tick(30)

    def print_controls(self):
        print('Controls:')
        print('\t{}: Quit'.format(pygame.key.name(self._KEY_QUIT)))
        print('\t{}: Drop Piece'.format(pygame.key.name(self._KEY_DROP_PIECE)))
        print('\t{}/{}: Move'.format(pygame.key.name(self._KEY_MOVE_LEFT), pygame.key.name(self._KEY_MOVE_LEFT)))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == self._KEY_QUIT:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif self._state == ViewState.PLAYING:
                    if event.key == self._KEY_DROP_PIECE:
                        self._attempt_to_drop_piece(self._current_player_piece, self._drop_x)
                    elif event.key == self._KEY_MOVE_LEFT:
                        self._move(-1)
                    elif event.key == self._KEY_MOVE_RIGHT:
                        self._move(1)

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _attempt_to_drop_piece(self, piece, x):
        """
        @param piece (model.Piece)
        @param x (Number) the column to drop the piece into
        """
        if self._model.is_column_full(x):
            return
        self._model.drop_piece(piece, x)
        self._end_turn()

    def _end_turn(self):
        if self._current_player_piece == model.Piece.PLAYER1:
            self._current_player_piece = model.Piece.PLAYER2
        elif self._current_player_piece == model.Piece.PLAYER2:
            self._current_player_piece = model.Piece.PLAYER1
        else:
            raise RuntimeError('Invalid current player piece')

    def _check_for_win(self):
        winning_player = None
        game_state = self._model.get_state()
        if game_state == model.GameState.PLAYER1_WON:
            winning_player = 1
        elif game_state == model.GameState.PLAYER2_WON:
            winning_player = 2

        if winning_player:
            self._state = ViewState.GAME_OVER
            winning_player_name = 'Player {}'.format(winning_player)
            self._draw_player_won_message(winning_player_name)

    def _move(self, dx):
        self._drop_x = (self._drop_x + dx) % self._model.size_x

    def _tick(self):
        pass

    def _draw(self):
        self._screen.fill(self._BACKGROUND_COLOR)

        self._draw_board()

        if self._state == ViewState.PLAYING:
            self._draw_drop_location()

        self._check_for_win()

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

    def _draw_drop_location(self):
        self._draw_piece(self._current_player_piece, self._drop_x, self._model.size_y)

        drop_y = self._model.get_drop_row(self._drop_x)
        if drop_y >= 0:
            self._draw_piece(self._current_player_piece, self._drop_x, drop_y, potential_piece=True)

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

    def _draw_player_won_message(self, winning_player_name):
        message = '{} Won!'.format(winning_player_name)
        message_color = pygame.Color(255, 255, 255)
        message_surface = self._font.render(message, True, message_color)
        message_rect = message_surface.get_rect()
        message_rect.topleft = (5, 5)
        self._screen.blit(message_surface, message_rect)

def main():
    view = View()
    view.run()

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[model])

if __name__ == '__main__':
    failure_count, test_count = run_tests()
    if failure_count == 0:
        main()