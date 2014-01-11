import pygame

class Action:
    QUIT = 0
    DROP_PIECE = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    NEW_GAME = 4

class KeyBindingManager:
    _KEY_QUIT = pygame.K_ESCAPE
    _KEY_DROP_PIECE = pygame.K_DOWN
    _KEY_MOVE_LEFT = pygame.K_LEFT
    _KEY_MOVE_RIGHT = pygame.K_RIGHT
    _KEY_NEW_GAME = pygame.K_RETURN

    def __init__(self):
        self._action_to_key_map = {
            Action.QUIT: self._KEY_QUIT,
            Action.DROP_PIECE: self._KEY_DROP_PIECE,
            Action.MOVE_LEFT: self._KEY_MOVE_LEFT,
            Action.MOVE_RIGHT: self._KEY_MOVE_RIGHT,
            Action.NEW_GAME: self._KEY_NEW_GAME,
            }

    def get_key(self, action):
        """
        >>> key_binding_manager = KeyBindingManager()
        >>> key_binding_manager.get_key(Action.DROP_PIECE) == KeyBindingManager._KEY_DROP_PIECE
        True
        """
        return self._action_to_key_map[action]

    def print_controls(self):
        print('Controls:')
        print('\t{}: Quit'.format(pygame.key.name(self.get_key(Action.QUIT))))
        print('\t{}: Drop Piece'.format(pygame.key.name(self.get_key(Action.DROP_PIECE))))
        print('\t{}/{}: Move'.format(pygame.key.name(self.get_key(Action.MOVE_LEFT)), pygame.key.name(self.get_key(Action.MOVE_RIGHT))))

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()