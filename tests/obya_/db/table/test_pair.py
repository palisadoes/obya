#!/usr/bin/env python3
"""Module to test obya.db.table.pair."""

import os
import unittest
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}obya{0}tests{0}obya_{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Application imports
from tests.libraries.configuration import UnittestConfig
from tests.libraries import dataset
from obya.db.table import pair


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_pairs(self):
        """Testing function pairs."""
        # Initialize key variables
        pair_ = dataset.random_string()

        # Test
        old = len(pair.pairs())
        self.assertFalse(pair.exists(pair_))
        pair.insert(pair_)
        self.assertTrue(pair.exists(pair_))
        self.assertTrue(len(pair.pairs()) == old + 1)

    def test_exists(self):
        """Testing function exists."""
        # Initialize key variables
        pair_ = dataset.random_string()

        # Test
        self.assertFalse(pair.exists(pair_))
        pair.insert(pair_)
        self.assertTrue(pair.exists(pair_))

    def test_insert(self):
        """Testing function insert."""
        # Initialize key variables
        pair_ = dataset.random_string()

        # Test
        self.assertFalse(pair.exists(pair_))
        pair.insert(pair_)
        self.assertTrue(pair.exists(pair_))


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
