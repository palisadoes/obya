#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys

import pandas as pd

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
from obya import evaluate
from obya import ingest


class TestEvaluate(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################
    _evaluate = evaluate.Evaluate(
        evaluate.package(
            ingest.ingest(
                '{0}{1}tests{1}data{1}test_ingest_2_years.csv'.format(
                    ROOT_DIR, os.sep)),
            periods=42
        )
    )

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_above(self):
        """Testing function above."""
        # Initialize key variables
        limit = 90

        # Test Fast
        result = self._evaluate.above(limit, fast=True)
        for item in result['k'].tolist():
            self.assertTrue(item > limit)

        # Test slow
        result = self._evaluate.above(limit, fast=False)
        for item in result['d'].tolist():
            self.assertTrue(item > limit)

    def test_below(self):
        """Testing function below."""
        # Initialize key variables
        limit = 10

        # Test Fast
        result = self._evaluate.below(limit, fast=True)
        for item in result['k'].tolist():
            self.assertTrue(item < limit)

        # Test slow
        result = self._evaluate.below(limit, fast=False)
        for item in result['d'].tolist():
            self.assertTrue(item < limit)

    def test_difference(self):
        """Testing function difference."""
        # Initialize key variables
        limit = 5

        # Test
        result = self._evaluate.difference(limit)
        k_values = result['k'].tolist()
        d_values = result['d'].tolist()
        for index, value in enumerate(k_values):
            self.assertTrue(abs(value - d_values[index]) < limit)

    def test_matches(self):
        """Testing function matches."""
        # Initialize key variables
        difference = 5
        above = 90
        below = 10

        # Test
        result = self._evaluate.matches(
            difference=difference,
            above=above,
            below=below
        )

        k_values = result['k'].tolist()
        d_values = result['d'].tolist()
        for index, kval in enumerate(k_values):
            dval = d_values[index]
            self.assertTrue(abs(kval - dval) < difference)

            # Both stochastic values cannot be between above and below
            self.assertFalse(
                (below < kval < above) and (below < dval < above)
            )


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_evaluate(self):
        """Testing function evaluate."""
        pass

    def test_stoch(self):
        """Testing function stoch."""
        # Initialize key variables
        columns = 'open high low close volume timestamp'
        k_period = 5
        d_period = 3
        expected = pd.DataFrame(
            data={
                'open': [
                    86.714, 87.117, 87.032, 87.175
                ],
                'high': [
                    87.139, 87.176, 87.078, 87.401
                ],
                'low': [
                    86.681, 86.756, 86.731, 87.085
                ],
                'close': [
                    87.116, 87.030, 86.731, 87.365
                ],
                'volume': [
                    26309, 23287, 5450, 6023
                ],
                'timestamp': [
                    1486728000, 1486742400, 1486756800, 1486936800
                ],
                'k': [
                    97.245509, 79.722222, 12.228797, 95.081967
                ],
                'd': [
                    86.926937, 81.036488, 63.065509, 62.344329
                ]
            }
        )

        # Test
        data = dataset.dataset()
        result = evaluate.stoch(
            data, k_period=k_period, d_period=d_period)

        # Test one column at a time
        for column in columns.split():
            self.assertEqual(
                result[column].tolist(),
                expected[column].tolist()
            )

    def test_package(self):
        """Testing function package."""
        # Initialize key variables
        columns = 'open high low close volume timestamp'
        periods = 10
        expected = pd.DataFrame(
            data={
                'open': [85.882],
                'high': [87.401],
                'low': [85.864],
                'close': [87.365],
                'volume': [183414.0],
                'timestamp': [1486936800]
            }
        )

        # Test
        data = dataset.dataset()
        result = evaluate.package(data, periods=periods)

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
