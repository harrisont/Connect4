import controller


def _main():
    game_controller = controller.Controller()
    game_controller.run()


def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[controller])


if __name__ == '__main__':
    (failure_count, test_count), tested_modules = run_tests()
    if failure_count == 0:
        _main()