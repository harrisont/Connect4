import pygame


class FadeAnimation:
    def __init__(self):
        self.alpha = 255

    def fade(self, amount):
        """
        @return True if the animation has finished, False otherwise.
        """
        self.alpha -= amount
        return self.alpha < 0


class MainMenuView:
    _BACKGROUND_COLOR = pygame.Color(0, 0, 0, 210)
    _SELECTION_COLOR = pygame.Color(255, 255, 255)
    _POSITION = (100, 100)
    _ENTRY_TEXT_PADDING_X = 15
    _FONT_SIZE = 72
    _FONT_COLOR = pygame.Color(255, 255, 255)
    _FONT_HOVER_COLOR = pygame.Color(0, 0, 0)
    _FADE_ANIMATION_SPEED = 5

    def __init__(self, model):
        self._model = model

        pygame.init()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

        self._size_x = self._calculate_size_x()

        self._fade_animation = None

    def _calculate_size_x(self):
        max_entry_size_x = 0
        for entry in self._model.entries:
            entry_size_x, entry_size_y = self._font.size(entry.text)
            max_entry_size_x = max(max_entry_size_x, entry_size_x)
        return max_entry_size_x + 2*self._ENTRY_TEXT_PADDING_X

    def draw(self, screen, is_enabled):
        if is_enabled:
            background_surface = self._create_background()

            self._draw_selection(background_surface, self._get_current_entry_position())
            self._draw_entries(background_surface)

            screen.blit(background_surface, self._POSITION)

        if self._fade_animation:
            self._draw_fade_animation(screen)

    def _create_background(self):
        width = self._size_x
        height = len(self._model.entries) * self._get_entry_height() - 1
        surface = pygame.Surface((width, height))
        surface.fill(self._BACKGROUND_COLOR)
        surface.set_alpha(self._BACKGROUND_COLOR.a)
        return surface

    def _draw_entries(self, screen):
        for index in range(len(self._model.entries)):
            self._draw_entry(screen, index, self._get_entry_text_position(index))

    def _draw_entry(self, screen, index, position):
        if index == self._model.current_index:
            color = self._FONT_HOVER_COLOR
        else:
            color = self._FONT_COLOR

        entry = self._model.entries[index]
        message_surface = self._font.render(entry.text, True, color)
        screen.blit(message_surface, position)

    def _get_entry_text_position(self, entry_index):
        entry_position_x, entry_position_y = self._get_entry_position(entry_index)
        return (entry_position_x + self._ENTRY_TEXT_PADDING_X,
                entry_position_y + 0.1*self._font.get_linesize())

    def _draw_selection(self, screen, position):
        surface = pygame.Surface(self._get_selection_size())
        surface.fill(self._SELECTION_COLOR)
        screen.blit(surface, position)

    def _get_selection_size(self):
        return self._size_x, self._get_entry_height()

    def _draw_fade_animation(self, screen):
        animation_surface = pygame.Surface(self._get_selection_size())
        animation_surface.fill(self._BACKGROUND_COLOR)
        animation_surface.set_alpha(self._fade_animation.alpha)

        self._draw_selection(animation_surface, self._get_entry_position(0))
        self._draw_entry(animation_surface, self._model.current_index, self._get_entry_text_position(0))

        animation_surface_position = [a+b for a, b in zip(self._POSITION, self._get_current_entry_position())]
        screen.blit(animation_surface, animation_surface_position)

    def _get_entry_position(self, entry_index):
        return 0, entry_index * self._get_entry_height()

    def _get_current_entry_position(self):
        return self._get_entry_position(self._model.current_index)

    def _get_entry_height(self):
        return 1.1*self._font.get_linesize()

    def is_dirty(self):
        return self._fade_animation is not None

    def on_menu_item_selected(self):
        if self._model.get_current_entry().does_close_menu:
            self._fade_animation = FadeAnimation()

    def tick(self):
        if self._fade_animation:
            if self._fade_animation.fade(self._FADE_ANIMATION_SPEED):
                self._fade_animation = None


def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])


if __name__ == '__main__':
    run_tests()