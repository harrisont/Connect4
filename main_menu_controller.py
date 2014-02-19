import key
import key_binding_manager
import main_menu_model
import main_menu_view

import pygame


class MainMenuController:
    _KEY_SELECT_CURRENT_MENU_ITEM = key.ModifiedKey(pygame.K_RETURN)
    _KEY_UP = key.ModifiedKey(pygame.K_UP)
    _KEY_DOWN = key.ModifiedKey(pygame.K_DOWN)

    def __init__(self, game_key_binding_manager, new_game_func, quit_func):
        self._game_key_binding_manager = game_key_binding_manager
        self._is_enabled = True
        self._model = main_menu_model.MainMenuModel([
            main_menu_model.Entry('New Game',
                                  on_select_func=self._get_toggle_then_call_func_func(new_game_func),
                                  on_hover_start_func=None,
                                  on_hover_end_func=None,
                                  does_close_menu=True),
            main_menu_model.Entry('Controls',
                                  on_select_func=None,
                                  on_hover_start_func=lambda: print('TODO(#6): show controls menu'),
                                  on_hover_end_func=lambda: print('TODO(#6): hide controls menu'),
                                  does_close_menu=False),
            main_menu_model.Entry('Quit',
                                  on_select_func=quit_func,
                                  on_hover_start_func=None,
                                  on_hover_end_func=None,
                                  does_close_menu=False),
        ])
        self._view = main_menu_view.MainMenuView(self._model)

        self._on_entry_index_changed()

        self._is_dirty = False

    def is_enabled(self):
        return self._is_enabled

    def toggle(self):
        self._is_enabled = not self._is_enabled
        self._is_dirty = True

    def _get_toggle_then_call_func_func(self, func):
        def toggle_then_call_func_func():
            self.toggle()
            func()
        return toggle_then_call_func_func

    def draw(self, surface):
        self._view.draw(surface, self.is_enabled())
        self._is_dirty = False

    def is_dirty(self):
        return self._is_dirty or self._view.is_dirty()

    def tick(self):
        self._view.tick()

    def handle_event_key_down(self, modified_key):
        """
        @param modified_key a key.ModifiedKey
        @return True if the event is consumed by the handler and should not be further processed.
        """
        self._is_dirty = False
        if not self.is_enabled():
            return False

        # Pass through TOGGLE_MAIN_MENU and QUIT.
        game_action = self._get_game_action(modified_key)
        if (game_action == key_binding_manager.Action.TOGGLE_MAIN_MENU
                or game_action == key_binding_manager.Action.QUIT):
            self._is_dirty = True
            return False

        if modified_key == self._KEY_SELECT_CURRENT_MENU_ITEM:
            self._select_current_menu_item()
        elif modified_key == self._KEY_UP:
            self._change_entry_index(-1)
        elif modified_key == self._KEY_DOWN:
            self._change_entry_index(1)
        return True

    def _select_current_menu_item(self):
        entry = self._model.get_current_entry()
        entry.select()
        self._view.on_menu_item_selected()

    def _change_entry_index(self, delta_index):
        old_entry = self._model.get_current_entry()
        old_entry.end_hover()

        self._model.change_current_index(delta_index)
        self._on_entry_index_changed()

    def _on_entry_index_changed(self):
        entry = self._model.get_current_entry()
        entry.start_hover()
        self._is_dirty = True

    def _get_game_action(self, modified_key):
        """
        @param modified_key a key.ModifiedKey
        """
        return self._game_key_binding_manager.get_action(modified_key)


def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__],
                             module_dependencies=[key,
                                                  key_binding_manager,
                                                  main_menu_model,
                                                  main_menu_view])

if __name__ == '__main__':
    run_tests()