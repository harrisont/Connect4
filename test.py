"""
TODO: Currently it's possible for run_doctests to call run_doctests on a dependency more than
once.

e.g.
    A
   / \
  B   C
   \ /
    D
Here D's run_tests function is called twice: once each for B and C.
"""
from types import ModuleType
from typing import Set, Tuple


def run_doctests(module, module_dependencies, headless: bool) -> Tuple[Tuple[int, int], Set[ModuleType]]:
    """
    @param module the module to test
    @param module_dependencies iterable(module-with-run_tests-method)
    @param headless If running in headless mode
    @return ((failure_count, test_count), tested_modules)
    """
    import doctest

    tested_modules = {module}

    # Test self
    test_results = doctest.testmod(module)

    # Test other modules
    if module_dependencies:
        for module in module_dependencies:
            if module in tested_modules:
                continue
            current_test_results, current_tested_modules = module.run_tests(headless)
            test_results = tuple(x + y for x, y in zip(test_results, current_test_results))
            tested_modules.update(current_tested_modules)

    return test_results, tested_modules
