import key_binding_manager
import model
import view
import pygame
import sys

class Controller:
    """
    >>> controller = Controller()
    >>> controller._attempt_to_drop_piece_for_current_player_at_current_location()
    >>> controller._move(-1)
    >>> controller._move(1)
    """

    _CONSECUTIVE_PIECES_TO_WIN = 4
    _BOARD_SIZE_X = 7
    _BOARD_SIZE_Y = 6

    def __init__(self):
        self._model = model.Model(self._CONSECUTIVE_PIECES_TO_WIN, (self._BOARD_SIZE_X, self._BOARD_SIZE_Y))
        self._view = None
        self._reset_game()
        self._key_binding_manager = key_binding_manager.KeyBindingManager()

        pygame.init()

    def _reset_game(self):
        # This needs to be done before the model is reset.
        if self._view:
            self._view.drop_all_pieces_off_of_board_from_current_location()

        self._drop_x = int(self._model.size_x / 2)
        self._model.reset_game()
        if self._view:
            self._view.reset()

    def run(self):
        self._key_binding_manager.print_controls()
        self._view = view.View(self._model, self._key_binding_manager)

        while True:
            self._handle_events()
            self._tick()
            self._tick_view()
            self._draw()

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _get_key(self, action):
        return self._key_binding_manager.get_key(action)

    def _handle_events(self):
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._quit()
        elif event.type == pygame.KEYDOWN:
            self._handle_event_key_down(event.key)

    def _handle_event_key_down(self, key):
        """
        @param key a pygame.K_* value
        """
        action = self._key_binding_manager.get_action(key)
        if action is not None:
            self._handle_action(action)

    def _handle_action(self, action):
        assert(action is not None)
        if action == key_binding_manager.Action.QUIT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self._is_game_playing():
            if action == key_binding_manager.Action.DROP_PIECE:
                self._attempt_to_drop_piece_for_current_player_at_current_location()
            elif action == key_binding_manager.Action.MOVE_LEFT:
                self._move(-1)
            elif action == key_binding_manager.Action.MOVE_RIGHT:
                self._move(1)
        else:
            if action == key_binding_manager.Action.NEW_GAME:
                self._reset_game()

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
    return test.run_doctests(sys.modules[__name__], module_dependencies=[key_binding_manager, model, view])

if __name__ == '__main__':
    run_tests()