from types import ModuleType
from typing import Set, Tuple

import controller


def _main():
    game_controller = controller.Controller()
    game_controller.run()


def run_tests(headless: bool) -> Tuple[Tuple[int, int], Set[ModuleType]]:
    """
    @return ((failure_count, test_count), tested_modules)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[controller], headless=headless)


if __name__ == '__main__':
    (failure_count, test_count), tested_modules = run_tests(headless=False)
    if failure_count == 0:
        _main()
