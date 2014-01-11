class Entry:
    def __init__(self, text, on_select_func):
        self.text = text
        self._on_select_func = on_select_func

    def select(self):
        self._on_select_func()

class MainMenuModel:
    def __init__(self, entries):
        self.entries = entries
        self.current_index = 0

    def change_current_index(self, delta_index):
        self.current_index = (self.current_index + delta_index) % len(self.entries)

    def get_current_entry(self):
        return self.entries[self.current_index]

def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])

if __name__ == '__main__':
    run_tests()