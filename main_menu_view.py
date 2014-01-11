import main_menu_model
import pygame

class MainMenuView:
    _BACKGROUND_COLOR = pygame.Color(0, 0, 0, 220)
    _POSITION = (100, 100)
    _ACTION_PADDING = 5
    _FONT_SIZE = 36
    _FONT_COLOR = pygame.Color(255, 255, 255)

    def __init__(self, model):
        self._model = model
        self._background_surface = self._create_background()

        pygame.init()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

    def draw(self, screen):
        self._draw_background(screen)
        self._draw_actions(screen)
        self._draw_selection(screen)

    def _draw_background(self, screen):
        screen.blit(self._background_surface, self._POSITION)

    def _create_background(self):
        size = (200, self._ACTION_PADDING + len(self._model.actions)*self._FONT_SIZE)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill(self._BACKGROUND_COLOR)
        return surface

    def _draw_actions(self, screen):
        for index, action in enumerate(self._model.actions):
            position = self._get_position(index)
            self.draw_message(screen, action, position)

    def _get_position(self, action_index):
        menu_position_x, menu_position_y = self._POSITION
        return (menu_position_x + self._ACTION_PADDING,
                menu_position_y + self._ACTION_PADDING + action_index*self._FONT_SIZE)

    def draw_message(self, screen, message, position):
        """
        @param position (x, y)
        """
        message_surface = self._font.render(message, True, self._FONT_COLOR)
        screen.blit(message_surface, position)

    def _draw_selection(self, screen):
        pass

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()