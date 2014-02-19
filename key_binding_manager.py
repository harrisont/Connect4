import key

import pygame


class Action:
    QUIT = 0
    DROP_PIECE = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    TOGGLE_MAIN_MENU = 4


class KeyBindingManager:
    _KEY_QUIT = key.ModifiedKey(pygame.K_F4, key.Modifier.ALT)
    _KEY_DROP_PIECE = key.ModifiedKey(pygame.K_DOWN)
    _KEY_MOVE_LEFT = key.ModifiedKey(pygame.K_LEFT)
    _KEY_MOVE_RIGHT = key.ModifiedKey(pygame.K_RIGHT)
    _KEY_TOGGLE_MAIN_MENU = key.ModifiedKey(pygame.K_ESCAPE)

    def __init__(self):
        self._action_to_key_map = {
            Action.QUIT: self._KEY_QUIT,
            Action.DROP_PIECE: self._KEY_DROP_PIECE,
            Action.MOVE_LEFT: self._KEY_MOVE_LEFT,
            Action.MOVE_RIGHT: self._KEY_MOVE_RIGHT,
            Action.TOGGLE_MAIN_MENU: self._KEY_TOGGLE_MAIN_MENU,
        }
        self._on_action_to_key_map_changed()

    def _on_action_to_key_map_changed(self):
        self._key_to_action_map = {modified_key: action for action, modified_key in self._action_to_key_map.items()}

    def get_key(self, action):
        """
        @return the key that corresponds to the action, or None if there is none.

        >>> key_binding_manager = KeyBindingManager()
        >>> key_binding_manager.get_key(Action.DROP_PIECE) == KeyBindingManager._KEY_DROP_PIECE
        True

        Returns None if the action has no corresponding key.
        >>> key_binding_manager.get_key(12345)
        """
        return self._action_to_key_map.get(action)

    def get_action(self, modified_key):
        """
        @param modified_key a key.ModifiedKey
        @return the action that corresponds to the key, or None if there is none.

        >>> key_binding_manager = KeyBindingManager()
        >>> key_binding_manager.get_action(KeyBindingManager._KEY_DROP_PIECE) == Action.DROP_PIECE
        True

        Returns None if the key has no corresponding action.
        >>> key_binding_manager.get_action(12345)
        """
        return self._key_to_action_map.get(modified_key)

    def print_controls(self):
        print('Controls:')
        print('\t{}: Toggle Menu'.format(self.get_key(Action.TOGGLE_MAIN_MENU)))
        print('\t{}: Quit'.format(self.get_key(Action.QUIT)))
        print('\t{}: Drop Piece'.format(self.get_key(Action.DROP_PIECE)))
        print('\t{}/{}: Move'.format(self.get_key(Action.MOVE_LEFT), self.get_key(Action.MOVE_RIGHT)))


def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[key])


if __name__ == '__main__':
    run_tests()