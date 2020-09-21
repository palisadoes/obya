#!/usr/bin/env python3
"""Script to reveal duplicate error codes in the application modules."""

from __future__ import print_function
import os
import sys


# Try to create a working PYTHONPATH
DEV_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(DEV_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}obya{0}tests{0}bin'.format(os.sep)
if DEV_DIR.endswith(_EXPECTED) is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Import application libraries
from tests.libraries import errors


def main():
    """Get all the error codes used in application.

    Args:
        None

    Returns:
        None

    """
    # Get code report
    minimum = 1000
    maximum = 2000
    errors.check_source_code(ROOT_DIR, minimum=minimum, maximum=maximum)


if __name__ == '__main__':
    main()
