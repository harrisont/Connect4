class Entry:
    def __init__(self, text, on_select_func, on_hover_start_func, on_hover_end_func, does_close_menu):
        self.text = text
        self._on_select_func = on_select_func
        self._on_hover_start_func = on_hover_start_func
        self._on_hover_end_func = on_hover_end_func
        self.does_close_menu = does_close_menu

    def select(self):
        if self._on_select_func:
            self._on_select_func()

    def start_hover(self):
        if self._on_hover_start_func:
            self._on_hover_start_func()

    def end_hover(self):
        if self._on_hover_end_func:
            self._on_hover_end_func()


class MainMenuModel:
    def __init__(self, entries, game_key_binding_manager):
        self.entries = entries
        self._game_key_binding_manager = game_key_binding_manager
        self.current_index = 0

    def change_current_index(self, delta_index):
        self.current_index = (self.current_index + delta_index) % len(self.entries)

    def get_current_entry(self):
        return self.entries[self.current_index]

    def get_control_lines(self):
        return self._game_key_binding_manager.get_control_lines()


def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])


if __name__ == '__main__':
    run_tests()