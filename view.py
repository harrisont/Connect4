import model
import pygame
import sys

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
        pygame.Color(255, 0, 0),
        pygame.Color(0, 0, 0)]
    _BOARD_MARGIN = 50
    _BOARD_OPENING_RADIUS = 40
    _BOARD_OPENING_MARGIN = 15

    _KEY_QUIT = pygame.K_ESCAPE

    def __init__(self):
        self._model = model.Model((self._BOARD_SIZE_X, self._BOARD_SIZE_Y))

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

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == self._KEY_QUIT:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _tick(self):
        pass

    def _draw(self):
        self._screen.fill(self._BACKGROUND_COLOR)

        self._draw_board()

        pygame.display.flip()

    def _draw_board(self):
        board_rect = self._get_board_rect()
        pygame.draw.rect(self._screen, self._BOARD_COLOR, board_rect, 0)

        for x in range(self._model.size_x):
            for y in range(self._model.size_y):
                opening_center = self._get_opening_center(x, y)
                piece = self._model.get_piece_at_opening(x, y)
                color = self._get_piece_color(piece)
                pygame.draw.circle(self._screen, color, opening_center, self._BOARD_OPENING_RADIUS)

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
        return (board_x + (x+1) * self._BOARD_OPENING_MARGIN + (2*x + 1) * self._BOARD_OPENING_RADIUS,
                board_y + (y+1) * self._BOARD_OPENING_MARGIN + (2*y + 1) * self._BOARD_OPENING_RADIUS)

    def _get_piece_color(self, piece):
        return self._PIECE_COLORS[piece]

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