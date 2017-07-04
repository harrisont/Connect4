import argparse
import sys

import connect4


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()
    (failure_count, test_count), tested_modules = connect4.run_tests(args.headless)
    if failure_count:
        sys.exit(1)


if __name__ == '__main__':
    _main()
