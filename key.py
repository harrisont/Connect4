import pygame


class Modifier:
    """
    Modifier key bitmap values

    >>> ctrl = Modifier.CTRL
    >>> bool(ctrl & Modifier.CTRL)
    True
    >>> bool(ctrl & Modifier.ALT)
    False
    >>> bool(ctrl & Modifier.SHIFT)
    False

    >>> alt_shift = Modifier.ALT | Modifier.SHIFT
    >>> bool(alt_shift & Modifier.CTRL)
    False
    >>> bool(alt_shift & Modifier.ALT)
    True
    >>> bool(alt_shift & Modifier.SHIFT)
    True
    """
    CTRL = 1
    SHIFT = 2
    ALT = 4


class ModifiedKey:
    def __init__(self, key, modifiers=0):
        self.key = key
        self.modifiers = modifiers

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((self.key, self.modifiers))

    def __str__(self):
        """
        >>> (num_pass, num_fail) = pygame.init()
        >>> num_fail == 0
        True

        >>> pygame.key.name(pygame.K_a)
        'a'

        >>> a = ModifiedKey(pygame.K_a)
        >>> str(a)
        'a'

        >>> ctrl_s = ModifiedKey(pygame.K_s, Modifier.CTRL)
        >>> str(ctrl_s)
        'ctrl+s'

        >>> alt_shift_k = ModifiedKey(pygame.K_k, Modifier.ALT | Modifier.SHIFT)
        >>> str(alt_shift_k)
        'alt+shift+k'
        """
        modifier_str = ''
        if self.modifiers & Modifier.CTRL > 0:
            modifier_str += 'ctrl+'
        if self.modifiers & Modifier.ALT > 0:
            modifier_str += 'alt+'
        if self.modifiers & Modifier.SHIFT > 0:
            modifier_str += 'shift+'
        return modifier_str + pygame.key.name(self.key)


def get_key_with_current_modifiers(key):
    """
    @return ModifiedKey
    """
    modifiers = 0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]:
        modifiers |= Modifier.CTRL
    if pressed[pygame.K_LALT] or pressed[pygame.K_RALT]:
        modifiers |= Modifier.ALT
    if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
        modifiers |= Modifier.SHIFT

    return ModifiedKey(key, modifiers)


def run_tests():
    """
    @return (failure_count, test_count)
    """
    import sys
    import test
    return test.run_doctests(sys.modules[__name__], module_dependencies=[])


if __name__ == '__main__':
    run_tests()
