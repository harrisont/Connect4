import main_menu_model

import pygame

class MainMenuView:
    _BACKGROUND_COLOR = pygame.Color(0, 0, 0, 210)
    _SELECTION_COLOR = pygame.Color(255, 255, 255)
    _POSITION = (100, 100)
    _ENTRY_TEXT_PADDING_X = 15
    _FONT_SIZE = 72
    _FONT_COLOR = pygame.Color(255, 255, 255)
    _FONT_HOVER_COLOR = pygame.Color(0, 0, 0)

    def __init__(self, model):
        self._model = model

        pygame.init()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

        self._size_x = self._calculate_size_x()

    def _calculate_size_x(self):
        max_entry_size_x = 0
        for entry in self._model.entries:
            entry_size_x, entry_size_y = self._font.size(entry.text)
            max_entry_size_x = max(max_entry_size_x, entry_size_x)
        return max_entry_size_x + 2*self._ENTRY_TEXT_PADDING_X

    def draw(self, screen):
        background_surface = self._create_background()

        self._draw_selection(background_surface)
        self._draw_entries(background_surface)

        screen.blit(background_surface, self._POSITION)

    def _create_background(self):
        size = (self._size_x, len(self._model.entries) * self._get_entry_height())
        surface = pygame.Surface(size)
        surface.fill(self._BACKGROUND_COLOR)
        surface.set_alpha(self._BACKGROUND_COLOR.a)
        return surface

    def _draw_entries(self, screen):
        for index, entry in enumerate(self._model.entries):
            position = self._get_entry_text_position(index)

            if index == self._model.current_index:
                color = self._FONT_HOVER_COLOR
            else:
                color = self._FONT_COLOR

            message_surface = self._font.render(entry.text, True, color)
            screen.blit(message_surface, position)

    def _get_entry_text_position(self, entry_index):
        entry_position_x, entry_position_y = self._get_entry_position(entry_index)
        return (entry_position_x + self._ENTRY_TEXT_PADDING_X,
                entry_position_y + 0.1*self._font.get_linesize())

    def _draw_selection(self, screen):
        size = (self._size_x, self._get_entry_height())
        surface = pygame.Surface(size)
        surface.fill(self._SELECTION_COLOR)
        position = self._get_entry_position(self._model.current_index)
        screen.blit(surface, position)

    def _get_entry_position(self, entry_index):
        return (0, entry_index * self._get_entry_height())

    def _get_entry_height(self):
        return 1.1*self._font.get_linesize()

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()