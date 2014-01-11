import pygame

class MainMenuView:
    _BACKGROUND_COLOR = pygame.Color(0, 0, 0, 220)
    _POSITION = (100, 100)
    _SIZE = (200, 100)

    def __init__(self):
        self._surface = pygame.Surface(self._SIZE, pygame.SRCALPHA)
        self._surface.fill(self._BACKGROUND_COLOR)

    def draw(self, screen):
        screen.blit(self._surface, self._POSITION)

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()