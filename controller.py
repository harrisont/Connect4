import model
import view
import pygame
import sys

class Controller:
    _KEY_QUIT = pygame.K_ESCAPE
    _KEY_DROP_PIECE = pygame.K_DOWN
    _KEY_MOVE_LEFT = pygame.K_LEFT
    _KEY_MOVE_RIGHT = pygame.K_RIGHT

    _CONSECUTIVE_PIECES_TO_WIN = 4
    _BOARD_SIZE_X = 7
    _BOARD_SIZE_Y = 6

    def __init__(self):
        self._model = model.Model(self._CONSECUTIVE_PIECES_TO_WIN, (self._BOARD_SIZE_X, self._BOARD_SIZE_Y))
        self._drop_x = int(self._model.size_x / 2)

        pygame.init()

    def run(self):
        self._print_controls()
        self._view = view.View(self._model)

        while True:
            self._handle_events()
            self._tick()
            self._tick_view()
            self._draw()

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _print_controls(self):
        print('Controls:')
        print('\t{}: Quit'.format(pygame.key.name(self._KEY_QUIT)))
        print('\t{}: Drop Piece'.format(pygame.key.name(self._KEY_DROP_PIECE)))
        print('\t{}/{}: Move'.format(pygame.key.name(self._KEY_MOVE_LEFT), pygame.key.name(self._KEY_MOVE_LEFT)))

    def _handle_events(self):
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event):
        """
        >>> class MockEvent:
        ...     def __init__(self, type):
        ...         self.type = type
        ...         self.key = None

        >>> event_handler = Controller()
        >>> event = MockEvent(pygame.KEYDOWN)

        >>> event.key = event_handler._KEY_DROP_PIECE
        >>> event_handler._handle_event(event)

        >>> event.key = event_handler._KEY_MOVE_LEFT
        >>> event_handler._handle_event(event)

        >>> event.key = event_handler._KEY_MOVE_RIGHT
        >>> event_handler._handle_event(event)
        """
        if event.type == pygame.QUIT:
            self._quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == self._KEY_QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif self._is_game_playing():
                if event.key == self._KEY_DROP_PIECE:
                    self._attempt_to_drop_piece_for_current_player_at_current_location()
                elif event.key == self._KEY_MOVE_LEFT:
                    self._move(-1)
                elif event.key == self._KEY_MOVE_RIGHT:
                    self._move(1)

    def _attempt_to_drop_piece_for_current_player_at_current_location(self):
        self._attempt_to_drop_piece(self._get_current_player_piece(), self._drop_x)

    def _attempt_to_drop_piece(self, piece, x):
        """
        @param piece (model.Piece)
        @param x (Number) the column to drop the piece into
        """
        if self._model.is_column_full(x):
            return
        self._model.drop_piece(piece, x)
        self._model.end_turn()

    def _move(self, dx):
        self._drop_x = (self._drop_x + dx) % self._model.size_x

    def _tick(self):
        pass

    def _draw(self):
        self._view.draw(self._drop_x)

    def _tick_view(self):
        self._view.tick()

    def _get_current_player_piece(self):
        return self._model.current_player_piece

    def _is_game_playing(self):
        return self._model.winning_player is None

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[view])

if __name__ == '__main__':
    run_tests()