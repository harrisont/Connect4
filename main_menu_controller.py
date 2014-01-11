import key_binding_manager
import main_menu_view
import pygame

class MainMenuController:
    _KEY_SELECT_CURRENT_MENU_ITEM = pygame.K_RETURN
    _KEY_UP = pygame.K_UP
    _KEY_DOWN = pygame.K_DOWN

    def __init__(self, game_key_binding_manager):
        self._game_key_binding_manager = game_key_binding_manager
        self._is_enabled = False
        self._view = main_menu_view.MainMenuView()
        self._is_dirty = False

        self._menu_actions = ['New Game', 'Controls', 'Exit']
        self._current_menu_index = 0

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

    def handle_event_key_down(self, key):
        """
        @param key a pygame.K_* value
        """
        self._is_dirty = self._handle_event_key_down_helper(key)

    def _handle_event_key_down_helper(self, key):
        """
        @param key a pygame.K_* value
        @return True if the key was handled, False otherwise.
        """
        if not self.is_enabled():
            return False

        if self._get_game_action(key) == key_binding_manager.Action.TOGGLE_MAIN_MENU:
            self._is_enabled = False
            return True
        elif key == self._KEY_SELECT_CURRENT_MENU_ITEM:
            self._select_current_menu_item()
            return True
        elif key == self._KEY_UP:
            self._change_current_menu_index(-1)
            return True
        elif key == self._KEY_DOWN:
            self._change_current_menu_index(1)
            return True
        else:
            return False

    def _select_current_menu_item(self):
        pass

    def _change_current_menu_index(self, delta_index):
        max_index = len(self._menu_actions) - 1
        self._current_menu_index = min(max(0, self._current_menu_index + delta_index), max_index)

    def _get_game_action(self, key):
        """
        @param key a pygame.K_* value
        """
        return self._game_key_binding_manager.get_action(key)

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__],
                             module_dependencies=[key_binding_manager,
                                                  main_menu_view])

if __name__ == '__main__':
    run_tests()