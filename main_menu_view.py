import main_menu_model
import pygame

class MainMenuView:
    _BACKGROUND_COLOR = pygame.Color(0, 0, 0, 220)
    _SELECTION_COLOR = pygame.Color(255, 255, 255)
    _POSITION = (100, 100)
    _ACTION_TEXT_PADDING = 5
    _FONT_SIZE = 36
    _FONT_COLOR = pygame.Color(255, 255, 255)
    _FONT_SELECTED_COLOR = pygame.Color(0, 0, 0)

    def __init__(self, model):
        self._model = model

        pygame.init()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

    def draw(self, screen):
        background_surface = self._create_background()

        self._draw_selection(background_surface)
        self._draw_actions(background_surface)

        screen.blit(background_surface, self._POSITION)

    def _create_background(self):
        size = (200,
                len(self._model.actions) * (self._FONT_SIZE + self._ACTION_TEXT_PADDING) - self._ACTION_TEXT_PADDING)
        surface = pygame.Surface(size)
        surface.fill(self._BACKGROUND_COLOR)
        surface.set_alpha(self._BACKGROUND_COLOR.a)
        return surface

    def _draw_actions(self, screen):
        for index, action in enumerate(self._model.actions):
            position = self._get_action_text_position(index)

            if index == self._model.current_index:
                color = self._FONT_SELECTED_COLOR
            else:
                color = self._FONT_COLOR

            message_surface = self._font.render(action, True, color)
            screen.blit(message_surface, position)

    def _get_action_position(self, action_index):
        return (0,
                action_index * (self._FONT_SIZE + self._ACTION_TEXT_PADDING))

    def _get_action_text_position(self, action_index):
        action_position_x, action_position_y = self._get_action_position(action_index)
        return (action_position_x + self._ACTION_TEXT_PADDING,
                action_position_y + self._ACTION_TEXT_PADDING)

    def _draw_selection(self, screen):
        size = (200, self._FONT_SIZE)
        surface = pygame.Surface(size)
        surface.fill(self._SELECTION_COLOR)

        position = self._get_action_position(self._model.current_index)
        screen.blit(surface, position)

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()