import view

class Controller:
    def __init__(self):
        self.view = view.View()

    def run(self):
        self.view.run()

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[view])

if __name__ == '__main__':
    run_tests()