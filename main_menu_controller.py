import key
import key_binding_manager
import main_menu_model
import main_menu_view
import pygame


class MainMenuController:
    _KEY_SELECT_CURRENT_MENU_ITEM = key.ModifiedKey(pygame.K_RETURN)
    _KEY_UP = key.ModifiedKey(pygame.K_UP)
    _KEY_DOWN = key.ModifiedKey(pygame.K_DOWN)

    def __init__(self, game_key_binding_manager):
        self._game_key_binding_manager = game_key_binding_manager
        self._is_enabled = False
        self._model = main_menu_model.MainMenuModel(actions=['New Game', 'Controls', 'Exit'])
        self._view = main_menu_view.MainMenuView(self._model)
        self._is_dirty = False

    def is_enabled(self):
        return self._is_enabled

    def toggle(self):
        self._is_enabled = not self._is_enabled
        self._is_dirty = True

    def draw(self, surface):
        if self.is_enabled():
            self._view.draw(surface)

    def is_dirty(self):
        return self._is_dirty

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
            self._is_dirty = True
        elif modified_key == self._KEY_UP:
            self._model.change_current_index(-1)
            self._is_dirty = True
        elif modified_key == self._KEY_DOWN:
            self._model.change_current_index(1)
            self._is_dirty = True
        return True

    def _select_current_menu_item(self):
        pass

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