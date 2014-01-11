class MainMenuModel:
    def __init__(self, actions):
        self.actions = actions
        self._current_index = 0

    def change_current_index(self, delta_index):
        self._current_index = (self._current_index + delta_index) % len(self.actions)
        print(self._current_index, self.get_current_action())

    def get_current_action(self):
        return self.actions[self._current_index]

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()