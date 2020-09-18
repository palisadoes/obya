#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}obya{0}tests{0}obya_'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig
from tests.libraries import dataset
from obya import ingest


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_ingest(self):
        """Testing ingest."""
        # Initialize key variables
        columns = 'open high low close volume timestamp'
        filepath = '{0}{1}tests{1}data{1}test_ingest.csv'.format(
            ROOT_DIR, os.sep)

        # Get results
        result = ingest.ingest(filepath)
        expected = dataset.dataset()

        # Test one column at a time
        for column in columns.split():
            self.assertEqual(
                result[column].tolist(),
                expected[column].tolist()
            )


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
