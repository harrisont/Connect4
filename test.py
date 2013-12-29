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

def run_doctests(module, module_dependencies=None):
    """
    @param module the module to test
    @param module_dependencies iteratable(module-with-run_tests-method)
    @return (failure_count, test_count)
    """
    import doctest

    # Test self
    test_results = doctest.testmod(module)

    # Test other modules
    if module_dependencies:
        for module in module_dependencies:
            test_results = tuple(x + y for x,y in zip(test_results, module.run_tests()))

    return test_results
