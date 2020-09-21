#!/usr/bin/env python3
"""Module to test obya.db.table.data."""

import os
import unittest
import sys
from datetime import timezone
import datetime

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
from obya.db.table import data


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_insert(self):
        """Testing function insert."""
        # Initialize key variables
        pair_ = dataset.random_string()
        df_ = dataset.dataset()
        timeframe = int(
            (df_['timestamp'][1:] - df_['timestamp'].shift()[1:]).median()
        )

        # Insert pair
        self.assertFalse(pair.exists(pair_))
        pair.insert(pair_)

        # Insert and get data
        data.insert(pair_, df_)
        result = data.dataframe(pair_, timeframe)

        # Test one column at a time
        for column in df_.columns.values:
            self.assertEqual(
                result[column].astype(float).round(3).tolist(),
                df_[column].astype(float).round(3).tolist()
            )

        #######################################################################
        # Test getting data since last entry in original DataFrame.
        #######################################################################

        now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
        secondsago = int(now - df_['timestamp'].tolist()[-1]) + 1
        result = data.dataframe(pair_, timeframe, secondsago=secondsago)

        # Test one column at a time. Result should equal the last value
        # of original DataFrame
        for column in df_.columns.values:
            self.assertEqual(
                result[column].astype(float).round(3).tolist(),
                [df_[column].astype(float).round(3).tolist()[-1]]
            )

    def test_dataframe(self):
        """Testing function dataframe."""
        # Initialize key variables
        pair_ = dataset.random_string()
        df_ = dataset.dataset()
        timeframe = int(
            (df_['timestamp'][1:] - df_['timestamp'].shift()[1:]).median()
        )

        # Insert pair
        self.assertFalse(pair.exists(pair_))
        pair.insert(pair_)

        # Insert and get data
        data.insert(pair_, df_)
        result = data.dataframe(pair_, timeframe)

        # Test one column at a time
        for column in df_.columns.values:
            self.assertEqual(
                result[column].astype(float).round(3).tolist(),
                df_[column].astype(float).round(3).tolist()
            )

        #######################################################################
        # Test getting data since last entry in original DataFrame.
        #######################################################################

        now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
        secondsago = int(now - df_['timestamp'].tolist()[-1]) + 1
        result = data.dataframe(pair_, timeframe, secondsago=secondsago)

        # Test one column at a time. Result should equal the last value
        # of original DataFrame
        for column in df_.columns.values:
            self.assertEqual(
                result[column].astype(float).round(3).tolist(),
                [df_[column].astype(float).round(3).tolist()[-1]]
            )


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
