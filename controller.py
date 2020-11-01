import sys
from types import ModuleType
from typing import Set, Tuple

import key
import key_binding_manager
import main_menu_controller
import model
import view

import pygame



class Controller:
    """
    >>> controller = Controller()
    >>> controller._attempt_to_drop_piece_for_current_player_at_current_location()
    >>> controller._move(-1)
    >>> controller._move(1)
    >>> controller._toggle_main_menu()
    """

    _CONSECUTIVE_PIECES_TO_WIN = 4
    _BOARD_SIZE_X = 7
    _BOARD_SIZE_Y = 6

    def __init__(self):
        self._model = model.Model(self._CONSECUTIVE_PIECES_TO_WIN, (self._BOARD_SIZE_X, self._BOARD_SIZE_Y))
        self._view = None
        self._key_binding_manager = key_binding_manager.KeyBindingManager()
        self._main_menu_controller = main_menu_controller.MainMenuController(self._key_binding_manager,
                                                                             self._reset_game,
                                                                             self._quit)
        self._reset_game()

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
        self._view = view.View(self._model)
        self._view.add_layer(self._main_menu_controller)

        while True:
            self._handle_events()
            self._tick()
            self._tick_view()
            self._draw()

    @staticmethod
    def _quit():
        pygame.quit()
        sys.exit(0)

    def _handle_events(self):
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._quit()
        elif event.type == pygame.KEYDOWN:
            modified_key = key.get_key_with_current_modifiers(event.key)
            self._handle_event_key_down(modified_key)

    def _handle_event_key_down(self, modified_key):
        """
        @param modified_key a key.ModifiedKey
        """
        if self._main_menu_controller.is_enabled():
            if self._main_menu_controller.handle_event_key_down(modified_key):
                return

        action = self._key_binding_manager.get_action(modified_key)
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
            elif action == key_binding_manager.Action.TOGGLE_MAIN_MENU:
                self._toggle_main_menu()

    def _attempt_to_drop_piece_for_current_player_at_current_location(self):
        self._attempt_to_drop_piece(self._get_current_player_piece(), self._drop_x)
        if not self._is_game_playing():
            self._toggle_main_menu()

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

    def _toggle_main_menu(self):
        self._main_menu_controller.toggle()

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


def run_tests(headless: bool) -> Tuple[Tuple[int, int], Set[ModuleType]]:
    """
    @return ((failure_count, test_count), tested_modules)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__],
                             module_dependencies=[key,
                                                  key_binding_manager,
                                                  main_menu_controller,
                                                  model,
                                                  view],
                             headless=headless)


if __name__ == '__main__':
    run_tests(headless=False)
