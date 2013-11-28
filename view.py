import model
import pygame
import sys

class View:
    _WINDOW_SIZE = (800, 600)
    _FONT_SIZE = 36
    _BACKGROUND_COLOR = pygame.Color(128, 128, 128)

    _KEY_QUIT = pygame.K_ESCAPE

    def __init__(self):
        self._model = model.Model()

        pygame.init()
        pygame.display.set_caption('Connect Four')
        self._fps_clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, self._FONT_SIZE)

    def run(self):
        self.print_controls()

        self._screen = pygame.display.set_mode(self._WINDOW_SIZE, pygame.DOUBLEBUF)

        while True:
            self._handle_events()
            self._tick()
            self._draw()

            # Wait long enough to run at 30 FPS.
            self._fps_clock.tick(30)

    def print_controls(self):
        print('Controls:')
        print('\t{}: Quit'.format(pygame.key.name(self._KEY_QUIT)))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == self._KEY_QUIT:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _tick(self):
        pass

    def _draw(self):
        self._screen.fill(self._BACKGROUND_COLOR)

        #...

        pygame.display.flip()

def main():
    view = View()
    view.run()

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[model])

if __name__ == '__main__':
    failure_count, test_count = run_tests()
    if failure_count == 0:
        main()