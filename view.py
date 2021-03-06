import math
import os
from types import ModuleType
from typing import Set, Tuple

import model

import pygame


class ViewState:
    PLAYING = 1
    GAME_OVER = 2


class DropAnimation:
    _COEFFICIENT_OF_RESTITUTION = 0.3  # Bounciness [0-1)

    def __init__(self, piece, board_x, board_y_initial, board_y_final, bounce):
        self.piece = piece
        self.board_x = board_x
        self.board_y = board_y_initial
        self.board_y_initial = board_y_initial
        self.board_y_final = board_y_final
        self._bounce = bounce
        self._is_bouncing = False
        self._prevent_new_bounce = False
        self._time = 0
        self._bounce_1_time = math.sqrt(board_y_initial - board_y_final)
        self._get_y_after_1_bounce = self._create_get_y_after_1_bounces_func(board_y_initial, board_y_final)

    def prevent_new_bounce(self):
        """Prevents the drop from bouncing if it hasn't started yet."""
        self._prevent_new_bounce = True

    def drop(self, delta):
        """
        @return True if the animation is done, False otherwise.
        """
        self._time += delta
        self.board_y = self._get_y(self._time)
        if self._is_finished():
            self.board_y = self.board_y_final
            return True
        else:
            return False

    def _get_y(self, time):
        if (not self._bounce
                or time <= self._bounce_1_time
                or (not self._is_bouncing and self._prevent_new_bounce)):
            y = self._get_y_after_0_bounces(time)
            return y
        else:
            self._is_bouncing = True
            y = self._get_y_after_1_bounce(time)
            return y

    def _get_y_after_0_bounces(self, time):
        y0 = self.board_y_initial
        return -time**2 + y0

    @classmethod
    def _create_get_y_after_1_bounces_func(cls, board_y_initial, board_y_final):
        """
        @return a function y(t) that returns the board-y position after the first bounce.
        y(t) satisfies the following constraints:
         * y(t_bounce) = y_after_0_bounces(t_bounce)
            This is because the position is the same as the equations transition just after the bounce.
         * velocity(t_bounce) = -c * velocity_after_0_bounces(t_bounce)
            This represents the bounce flipping the velocity and the coefficient of restitition.

        """
        y0 = board_y_initial
        yf = board_y_final
        dy = y0 - yf
        c = cls._COEFFICIENT_OF_RESTITUTION
        constant_1 = 2*math.sqrt(dy)*(1+c)
        constant_2 = yf - dy - 2*dy*c
        return lambda time: -time**2 + constant_1*time + constant_2

    def _is_finished(self):
        return (self.board_y <= self.board_y_final
                and (not self._is_bouncing or self._time >= self._bounce_1_time))


class View:
    _WINDOW_SIZE_X = 800
    _WINDOW_SIZE_Y = 700
    _DESIRED_FPS = 60

    _FONT_SIZE = 36

    _BACKGROUND_COLOR = pygame.Color(128, 128, 128)

    _BOARD_COLOR = pygame.Color(0, 116, 179)
    _PIECE_COLORS = [
        _BACKGROUND_COLOR,
        pygame.Color(200, 0, 0),
        pygame.Color(10, 10, 10)]
    _POTENTIAL_PIECE_COLORS = [
        _BACKGROUND_COLOR,
        pygame.Color(164, 64, 64),
        pygame.Color(69, 69, 69)]
    _WINNING_PIECES_LINE_COLOR = pygame.Color(30, 200, 30)
    _BOARD_MARGIN = 50
    _BOARD_OPENING_RADIUS = 40
    _BOARD_OPENING_MARGIN = 15

    _ANIMATION_SPEED_MULTIPLIER = 8
    _DRAW_DROP_X_DELAY_AFTER_DROP = 1 / _ANIMATION_SPEED_MULTIPLIER  # seconds

    def __init__(self, view_model):
        self.reset()
        self._model = view_model
        self._drop_animations = []
        self._additional_layers = []

        pygame.init()
        pygame.display.set_caption('Connect Four')
        self._fps_clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

        pygame.display.set_icon(pygame.image.load(os.path.join('data', 'icon.png')))
        self._screen = pygame.display.set_mode((self._WINDOW_SIZE_X, self._WINDOW_SIZE_Y), pygame.DOUBLEBUF)

        self._board_surface = self._create_board_surface()

    def reset(self):
        """
        Do not reset self._drop_animations because we want these to persist across games to support
        animating the pieces from the previous game being dropped off of the board.
        """
        self._state = ViewState.PLAYING
        self._last_tracked_num_drops = 0
        self._last_drop_x = -1
        self._time_since_last_drop = 1000000  # large number
        self._dirty = True

    def draw(self, drop_x):
        # Optimization to skip the draw step if nothing changed.
        if not self._is_dirty(drop_x):
            return

        self._dirty = False

        self._screen.fill(self._BACKGROUND_COLOR)

        self._draw_pieces_at_rest()
        self._draw_dropping_pieces()
        self._draw_board()

        if self._state == ViewState.PLAYING:
            if self._time_since_last_drop >= self._DRAW_DROP_X_DELAY_AFTER_DROP:
                self._draw_drop_x(drop_x)
            else:
                self._dirty = True
            if not self._drop_animations:
                self._draw_drop_preview(drop_x)
        elif self._state == ViewState.GAME_OVER:
            self._draw_won_message()

        for layer in self._additional_layers:
            layer.draw(self._screen)

        pygame.display.flip()
        self._last_drop_x = drop_x

    def _is_dirty(self, drop_x):
        return (len(self._drop_animations) > 0
                or drop_x != self._last_drop_x
                or self._dirty
                or any([layer.is_dirty() for layer in self._additional_layers]))

    def _draw_pieces_at_rest(self):
        for x in range(self._model.size_x):
            for y in range(self._model.size_y):
                if self._has_dropping_piece_with_final_position(x, y):
                    continue
                piece = self._model.get_piece_at_opening(x, y)
                if piece == model.Piece.NONE:
                    continue
                self._draw_piece(piece, x, y)

    def _create_board_surface(self):
        """
        Create a board surface with transparent openings.
        @return the created board surface
        """
        x, y, width, height = self._get_board_rect()
        openings_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        openings_surface.fill(pygame.Color(0, 0, 0, 0))
        offset = (0, 0)
        for x in range(self._model.size_x):
            for y in range(self._model.size_y):
                self._draw_piece_onto_surface(openings_surface, pygame.Color(255, 255, 255), x, y, offset)

        board_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        board_surface.fill(self._BOARD_COLOR)
        board_surface.blit(openings_surface, (0, 0), area=None, special_flags=pygame.BLEND_RGBA_SUB)
        return board_surface

    def _draw_board(self):
        x, y = self._get_board_position()
        self._screen.blit(self._board_surface, (x, y))

    def _has_dropping_piece_with_final_position(self, x, y):
        """
        @return True if there is a dropping piece whose final position is (x, y), False otherwise.
        """
        for drop_animation in self._drop_animations:
            if x == drop_animation.board_x and y == drop_animation.board_y_final:
                return True
        return False

    def _draw_dropping_pieces(self):
        for drop_animation in self._drop_animations:
            self._draw_piece(drop_animation.piece, drop_animation.board_x, drop_animation.board_y)

    def _draw_piece(self, piece, x, y, potential_piece=False):
        """
        @param potential_piece (Boolean) if True, draws the piece as a potential piece
        """
        color = self._get_piece_color(piece, potential_piece)
        board_position = self._get_board_position()
        self._draw_piece_onto_surface(self._screen, color, x, y, board_position)

    def _draw_piece_onto_surface(self, surface, color, x, y, offset):
        """
        @param offset (x,y)
        """
        opening_center = self._get_opening_center(x, y, offset)
        pygame.draw.circle(surface, color, opening_center, self._BOARD_OPENING_RADIUS)

    def _draw_drop_x(self, drop_x):
        self._draw_piece(self._model.current_player_piece, drop_x, self._model.size_y)

    def _draw_drop_preview(self, drop_x):
        drop_y = self._model.get_drop_row(drop_x)
        if drop_y >= 0:
            self._draw_piece(self._model.current_player_piece, drop_x, drop_y, potential_piece=True)

    def _get_board_position(self):
        return self._BOARD_MARGIN, self._BOARD_MARGIN

    def _get_board_rect(self):
        """Returns the (left, top, width, height) of the board."""
        board_x, board_y = self._get_board_position()
        size_per_opening = self._BOARD_OPENING_MARGIN + 2*self._BOARD_OPENING_RADIUS
        return (board_x,
                board_y,
                self._BOARD_OPENING_MARGIN + self._model.size_x * size_per_opening,
                self._BOARD_OPENING_MARGIN + self._model.size_y * size_per_opening)

    def _get_opening_center(self, x, y, offset):
        """
        @param offset (x,y)
        """
        offset_x, offset_y = offset
        flipped_y = self._model.size_y - y - 1
        return (int(offset_x
                    + (x+1) * self._BOARD_OPENING_MARGIN
                    + (2*x + 1) * self._BOARD_OPENING_RADIUS),
                int(offset_y
                    + (flipped_y+1) * self._BOARD_OPENING_MARGIN
                    + (2*flipped_y + 1) * self._BOARD_OPENING_RADIUS))

    def _get_piece_color(self, piece, potential_piece):
        if potential_piece:
            return self._POTENTIAL_PIECE_COLORS[piece]
        else:
            return self._PIECE_COLORS[piece]

    def _draw_won_message(self):
        self._draw_player_won_message()
        if self._model.winning_player != model.Piece.NONE:
            self._draw_winning_pieces(self._model.winning_piece_positions)

    def _draw_player_won_message(self):
        message = self._get_player_won_message()
        message_color = pygame.Color(255, 255, 255)
        message_surface = self._font.render(message, True, message_color)
        message_rect = message_surface.get_rect()
        message_rect.topleft = (5, 5)
        self._screen.blit(message_surface, message_rect)

    def _get_player_won_message(self):
        winning_player = self._model.winning_player
        if winning_player == model.Piece.NONE:
            return 'Tie Game!'
        else:
            return 'Player {} Won!'.format(winning_player)

    def _draw_winning_pieces(self, winning_piece_positions):
        """
        @param winning_piece_positions [(piece_1_x, piece_1_y), (piece_2_x, piece_2_y), ...]
        """
        color = self._WINNING_PIECES_LINE_COLOR
        board_position = self._get_board_position()
        line_start = self._get_opening_center(*winning_piece_positions[0], offset=board_position)
        line_end = self._get_opening_center(*winning_piece_positions[-1], offset=board_position)
        line_width = self._BOARD_OPENING_RADIUS // 4
        pygame.draw.line(self._screen, color, line_start, line_end, line_width)

    def tick(self):
        # Wait long enough to run at a fixed FPS.
        self._fps_clock.tick(self._DESIRED_FPS)

        winning_player = self._model.winning_player
        if winning_player is not None:
            self._state = ViewState.GAME_OVER

        self._track_newly_dropped_pieces()
        self._drop_dropping_pieces()

        self._time_since_last_drop += 1 / self._DESIRED_FPS

        for layer in self._additional_layers:
            layer.tick()

    def _track_newly_dropped_pieces(self):
        drop_history = self._get_drop_history()
        num_drops = len(drop_history)
        for drop_history_index in range(self._last_tracked_num_drops, num_drops):
            piece, x, y_final = drop_history[drop_history_index]
            y_initial = self._model.size_y
            self._drop_animations.append(DropAnimation(piece, x, y_initial, y_final, bounce=True))
            self._time_since_last_drop = 0
        self._last_tracked_num_drops = num_drops

    def _get_drop_history(self):
        return self._model.drop_history

    def _drop_dropping_pieces(self):
        delta_y = self._ANIMATION_SPEED_MULTIPLIER / self._DESIRED_FPS
        finished_drop_animation_indices = []

        for drop_animation_index, drop_animation in enumerate(self._drop_animations):
            drop_finished = drop_animation.drop(delta_y)
            if drop_finished:
                finished_drop_animation_indices.append(drop_animation_index)

        for drop_animation_index in reversed(finished_drop_animation_indices):
            self._drop_animations.pop(drop_animation_index)

            # This is necessary to draw the last frame of the animation.
            # Otherwise the frame will be skipped (by optimization) when this is the last animation.
            self._dirty = True

    def drop_all_pieces_off_of_board_from_current_location(self):
        drop_history = self._get_drop_history()
        y_final = -1
        existing_drop_animations = self._drop_animations.copy()
        for piece, x, y_initial in drop_history:
            has_existing_drop_animation = False
            for exiting_drop_animation in existing_drop_animations:
                if exiting_drop_animation.board_x == x and exiting_drop_animation.board_y_final == y_initial:
                    exiting_drop_animation.board_y_final = y_final
                    exiting_drop_animation.prevent_new_bounce()
                    has_existing_drop_animation = True
                    break
            if has_existing_drop_animation:
                continue
            self._drop_animations.append(DropAnimation(piece, x, y_initial, y_final, bounce=False))

    def add_layer(self, drawable):
        """
        @param drawable is an object that contains the following methods:
            is_dirty() -> bool
            draw(Surface) -> None
            tick() -> None
        """
        return self._additional_layers.append(drawable)


def run_tests(headless: bool) -> Tuple[Tuple[int, int], Set[ModuleType]]:
    """
    @return ((failure_count, test_count), tested_modules)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[model], headless=headless)


if __name__ == '__main__':
    run_tests(headless=False)
