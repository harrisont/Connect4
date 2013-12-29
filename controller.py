import model
import view

class Controller:
    _CONSECUTIVE_PIECES_TO_WIN = 4
    _BOARD_SIZE_X = 7
    _BOARD_SIZE_Y = 6

    def __init__(self):
        self.model = model.Model(self._CONSECUTIVE_PIECES_TO_WIN, (self._BOARD_SIZE_X, self._BOARD_SIZE_Y))
        self.view = view.View(self.model)

    def run(self):
        self.view.run()

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[model, view])

if __name__ == '__main__':
    run_tests()