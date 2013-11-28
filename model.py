class Model:
    _SIZE_X = 7
    _SIZE_Y = 6

    def __init__(self):
        self.size_x = self._SIZE_X
        self.size_y = self._SIZE_Y

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()
