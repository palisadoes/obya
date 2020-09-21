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
        evaluate.summary(
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
        limit = 1

        # Test
        result = self._evaluate.difference(limit)
        k_values = result['k'].tolist()
        d_values = result['d'].tolist()
        for index, value in enumerate(k_values):
            self.assertTrue(abs(value - d_values[index]) < limit)

    def test_either(self):
        """Testing function either."""
        # Initialize key variables
        above = 90
        below = 10

        # Test
        result = self._evaluate.either(
            above=above,
            below=below
        )

        k_values = result['k'].tolist()
        d_values = result['d'].tolist()
        for index, kval in enumerate(k_values):
            # Both stochastic values cannot be between above and below
            dval = d_values[index]
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
        # Initialize key variables
        k_period = 5
        d_period = 3
        periods = 4
        filepath = '{0}{1}tests{1}data{1}test_ingest_2_years.csv'.format(
            ROOT_DIR, os.sep)

        expected_data = {
            'index': [2657, 2666, 2669, 2671, 2672],
            'open': [76.959, 77.528, 78.027, 78.141, 78.028],
            'high': [77.95, 78.45, 78.45, 78.354, 78.326],
            'low': [76.776, 77.403, 78.008, 78.007, 78.007],
            'close': [77.81, 78.194, 78.233, 78.191, 78.206],
            'volume': [73970, 60312, 58036, 64416, 77026],
            'timestamp': [
                1598587200, 1598889600, 1598932800, 1598961600, 1598976000],
            'k': [94.052676, 91.030133, 92.396636, 90.189394, 90.757576],
            'd': [94.626981, 91.223783, 90.83075, 88.427949, 89.018147],
            'delta': [-0.574305, -0.19365, 1.565887, 1.761445, 1.739429],
            'h4_k': [94.052676, 91.030133, 91.780303, 90.189394, 90.6298],
            'h4_d': [94.626981, 91.223783, 90.360365, 87.862439, 88.535051],
            'h4_delta': [-0.574305, -0.19365, 1.419938, 2.326955, 2.094749],
            'counts': [11, 14, 17, 18, 18]
        }

        expected = pd.DataFrame(data=expected_data)

        # Test
        data = ingest.ingest(filepath)
        result = evaluate.evaluate(
            data, periods, k_period=k_period, d_period=d_period).tail()

        # Test one column at a time
        for column, _ in expected_data.items():
            if column == 'index':
                continue
            self.assertEqual(
                result[column].astype(float).round(3).tolist(),
                expected[column].astype(float).round(3).tolist()
            )

    def test_frequency(self):
        """Testing function frequency."""
        # Initialize key variables
        long = pd.DataFrame(data={'long': list(range(20))})
        short = pd.DataFrame(data={'short': list(range(5))})
        periods = 10
        expected_data = {
            'long': list(range(20)),
            'counts': [
                1, 2, 3, 4, 5,
                5, 5, 5, 5, 5,
                4, 3, 2, 1, 0,
                0, 0, 0, 0, 0
            ]
        }

        # Expected
        expected = pd.DataFrame(data=expected_data)

        # Test with zeros
        result = evaluate.frequency(
            long, short, periods=periods, no_zeros=False)

        # Test one column at a time
        for column, _ in expected_data.items():
            self.assertEqual(
                result[column].tolist(),
                expected[column].tolist()
            )

        # Test without zeros
        result = evaluate.frequency(
            long, short, periods=periods)

        no_zero_data = {
            'long': list(range(14)),
            'counts': [
                1, 2, 3, 4, 5,
                5, 5, 5, 5, 5,
                4, 3, 2, 1
            ]
        }

        # Test one column at a time
        for column, _ in no_zero_data.items():
            self.assertEqual(
                result[column].tolist(),
                no_zero_data[column]
            )

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

    def test_summary(self):
        """Testing function summary."""
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
        result = evaluate.summary(data, periods=periods)

        # Test one column at a time
        for column in columns.split():
            self.assertEqual(
                result[column].tolist(),
                expected[column].tolist()
            )

        # Test for a short period
        periods = 5
        expected = pd.DataFrame(
            data={
                'open': [
                    85.882, 86.184, 86.419, 86.465, 86.964, 86.983
                ],
                'high': [
                    87.015, 87.015, 87.139, 87.176, 87.176, 87.401
                ],
                'low': [
                    85.864, 86.126, 86.304, 86.456, 86.669, 86.669
                ],
                'close': [
                    86.985, 86.714, 87.116, 87.030, 86.731, 87.365
                ],
                'volume': [
                    101024, 93260, 99727, 110365, 93567, 82390
                ],
                'timestamp': [
                    1486699200, 1486713600, 1486728000,
                    1486742400, 1486756800, 1486936800
                ]
            }
        )

        # Test
        data = dataset.dataset()
        result = evaluate.summary(data, periods=periods)

        # Test one column at a time
        for column in columns.split():
            self.assertEqual(
                result[column].tolist(),
                expected[column].tolist()
            )

    def test_batch(self):
        """Testing function batch."""
        # Initialize key variables
        columns = 'open high low close volume timestamp'
        boundary = 604800
        expected = pd.DataFrame(
            data={
                'open': [87.032],
                'high': [87.078],
                'low': [86.731],
                'close': [86.731],
                'volume': [5450],
                'timestamp': [1486756800]
            }
        )

        # Test
        data = dataset.dataset()
        result = evaluate.batch(data, boundary=boundary)

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
