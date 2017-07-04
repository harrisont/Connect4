from types import ModuleType
from typing import Set, Tuple

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
    _CONTROLS_FONT_SIZE = 50

    def __init__(self, model):
        self._model = model

        pygame.init()
        self._font = pygame.font.Font(None, self._FONT_SIZE)
        self._controls_font = pygame.font.Font(None, self._CONTROLS_FONT_SIZE)

        self._entries_size_x = self._calculate_entries_size_x()
        self._fade_animation = None
        self._is_right_area_enabled = False
        self._right_area_width = self._calculate_controls_size_x()

    def _calculate_entries_size_x(self):
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
            if self._is_right_area_enabled:
                self._draw_right_area(background_surface)

            screen.blit(background_surface, self._POSITION)

        if self._fade_animation:
            self._draw_fade_animation(screen)

    def _create_background(self):
        width = self._entries_size_x
        if self._is_right_area_enabled:
            width += self._right_area_width
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
        return self._entries_size_x, self._get_entry_height()

    def _draw_right_area(self, screen):
        right_area_rect = pygame.Rect(self._entries_size_x, 0, self._right_area_width, screen.get_height())
        screen.fill(self._SELECTION_COLOR, right_area_rect)

        for control_index, control_line in enumerate(self._model.get_control_lines()):
            message_surface = self._controls_font.render(control_line, True, self._FONT_HOVER_COLOR)
            controls_text_position = (
                self._entries_size_x + self._ENTRY_TEXT_PADDING_X,
                self._ENTRY_TEXT_PADDING_X + control_index * 1.1 * self._controls_font.get_linesize()
            )
            screen.blit(message_surface, controls_text_position)

    def _calculate_controls_size_x(self):
        max_size_x = 0
        for control_line in self._model.get_control_lines():
            size_x, size_y = self._controls_font.size(control_line)
            max_size_x = max(max_size_x, size_x)
        return max_size_x + 2*self._ENTRY_TEXT_PADDING_X

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

    def set_right_area_enabled(self, is_enabled):
        self._is_right_area_enabled = is_enabled


def run_tests(headless: bool) -> Tuple[Tuple[int, int], Set[ModuleType]]:
    """
    @return ((failure_count, test_count), tested_modules)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[], headless=headless)


if __name__ == '__main__':
    run_tests(headless=False)
