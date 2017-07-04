import sys

import connect4


def _main():
    # TODO: read from argument
    headless = True

    (failure_count, test_count), tested_modules = connect4.run_tests(headless)
    if failure_count:
        sys.exit(1)


if __name__ == '__main__':
    _main()
