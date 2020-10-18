#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys
from operator import itemgetter

import pandas as pd
import numpy as np

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

# Application imports
from tests.libraries.configuration import UnittestConfig
from tests.libraries import dataset
from obya import evaluate
from obya.ingest import files


class TestEither(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_fast(self):
        """Testing function fast."""
        pass

    def test_slow(self):
        """Testing function slow."""
        pass

    def test__process(self):
        """Testing function _process."""
        pass


class TestAbove(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    df = evaluate.stoch(
        evaluate.summary(
            files.ingest(
                '{0}{1}tests{1}data{1}test_ingest_2_years.csv'.format(
                    ROOT_DIR, os.sep)),
            periods=10
        )
    )

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_fast(self):
        """Testing function fast."""
        # Initalize key variables
        limit = 99

        expected = [
            {
                'close': 71.834,
                'd': 96.3619738908452,
                'high': 71.924,
                'k': 99.25249169435213,
                'low': 71.092,
                'open': 71.255,
                'sequential': 1.0,
                'timestamp': 1590782400.0,
                'volume': 153698.0},
            {
                'close': 74.258,
                'd': 97.28526798717137,
                'high': 74.36,
                'k': 99.29538546559822,
                'low': 71.602,
                'open': 71.685,
                'sequential': 2.0,
                'timestamp': 1591099200.0,
                'volume': 148269.0}
            ]

        # Get data
        above = evaluate.Above(self.df, limit=limit)
        result_ = above.fast

        # Test
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp')
        )
        self.assertEqual(result, expected)

    def test_slow(self):
        """Testing function slow."""
        # Initalize key variables
        limit = 97.4

        expected = [
            {
                'close': 75.25,
                'd': 97.64132279683986,
                'high': 75.756,
                'k': 96.81199596774194,
                'low': 74.211,
                'open': 74.259,
                'sequential': 1.0,
                'timestamp': 1591243200.0,
                'volume': 168746.0},
            {
                'close': 76.346,
                'd': 97.44648427090023,
                'high': 76.739,
                'k': 97.36577518600443,
                'low': 74.855,
                'open': 75.252,
                'sequential': 2.0,
                'timestamp': 1591387200.0,
                'volume': 190698.0}
            ]

        # Get data
        above = evaluate.Above(self.df, limit=limit)
        result_ = above.slow

        # Test
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp')
        )
        self.assertEqual(result, expected)


class TestBelow(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    df = evaluate.stoch(
        evaluate.summary(
            files.ingest(
                '{0}{1}tests{1}data{1}test_ingest_2_years.csv'.format(
                    ROOT_DIR, os.sep)),
            periods=10
        )
    )

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_fast(self):
        """Testing function fast."""
        # Initalize key variables
        limit = 1

        expected = [
            {
                'close': 74.524,
                'd': 7.493933912777486,
                'high': 75.011,
                'k': 0.7857601026299962,
                'low': 74.475,
                'open': 74.888,
                'sequential': 1.0,
                'timestamp': 1560542400.0,
                'volume': 163733.0},
            {
                'close': 72.974,
                'd': 30.79906942353987,
                'high': 74.885,
                'k': 0.9296920395122202,
                'low': 72.942,
                'open': 74.818,
                'sequential': 1.0,
                'timestamp': 1564675200.0,
                'volume': 180925.0}
            ]

        # Get data
        below = evaluate.Below(self.df, limit=limit)
        result_ = below.fast

        # Test
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp')
        )
        self.assertEqual(result, expected)

    def test_slow(self):
        """Testing function slow."""
        # Initalize key variables
        limit = 4

        expected = [
            {
                'close': 74.195,
                'd': 3.6290158972643987,
                'high': 74.768,
                'k': 4.007071302298048,
                'low': 74.027,
                'open': 74.083,
                'sequential': 1.0,
                'timestamp': 1560988800.0,
                'volume': 181321.0},
            {
                'close': 74.36,
                'd': 3.124966257517659,
                'high': 74.673,
                'k': 6.437831467295195,
                'low': 74.125,
                'open': 74.194,
                'sequential': 2.0,
                'timestamp': 1561132800.0,
                'volume': 218113.0}
            ]

        # Get data
        below = evaluate.Below(self.df, limit=limit)
        result_ = below.slow

        # Test
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp')
        )
        self.assertEqual(result, expected)


class TestEvaluate(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################
    _evaluate = evaluate.Evaluate(
        evaluate.summary(
            files.ingest(
                '{0}{1}tests{1}data{1}test_ingest_2_years.csv'.format(
                    ROOT_DIR, os.sep)),
            periods=10
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
        self.assertFalse(result.empty)
        for item in result['k'].tolist():
            self.assertTrue(item > limit)

        # Test slow
        result = self._evaluate.above(limit, fast=False)
        self.assertFalse(result.empty)
        for item in result['d'].tolist():
            self.assertTrue(item > limit)

    def test_below(self):
        """Testing function below."""
        # Initialize key variables
        limit = 20

        # Test Fast
        result = self._evaluate.below(limit, fast=True)
        self.assertFalse(result.empty)
        for item in result['k'].tolist():
            self.assertTrue(item < limit)

        # Test slow
        result = self._evaluate.below(limit, fast=False)
        self.assertFalse(result.empty)
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

        expected = [
            {
                'close': 69.679,
                'counts': 9.0,
                'd_l': 95.59992943843139,
                'd_s': 86.92494398788244,
                'Δ_l': 3.7234151724919684,
                'Δ_s': 10.543410442498057,
                'high': 69.693,
                'k_l': 99.32334461092336,
                'k_s': 97.4683544303805,
                'low': 69.169,
                'open': 69.489,
                'sequential': 2.0,
                'timestamp': 1588953600.0,
                'volume': 63955.0},
            {
                'close': 70.519,
                'counts': 7.0,
                'd_l': 50.73520488225466,
                'd_s': 73.55230154282829,
                'Δ_l': 0.6208756076843542,
                'Δ_s': 20.251485032042424,
                'high': 70.555,
                'k_l': 51.35608048993902,
                'k_s': 93.80378657487071,
                'low': 70.02,
                'open': 70.206,
                'sequential': 1.0,
                'timestamp': 1590354000.0,
                'volume': 34297.0}
            ]

        # Get data
        data = files.ingest(filepath)
        result_ = evaluate.evaluate(
            data, periods, k_period=k_period, d_period=d_period).tail(2)

        # Test
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp'))
        self.assertEqual(result, expected)

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
                    87.032, 87.175
                ],
                'high': [
                    87.078, 87.401
                ],
                'low': [
                    86.731, 87.085
                ],
                'close': [
                    86.731, 87.365
                ],
                'volume': [
                    5450, 6023
                ],
                'timestamp': [
                    1486756800, 1486936800
                ],
                'k': [
                    12.228797, 95.081967
                ],
                'd': [
                    63.065509, 62.344329
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
        columns = 'timestamp low close open high volume'.split()
        rows = 25
        interval = 2
        periods = 10

        # Create data
        data = pd.DataFrame(
            np.arange(rows * len(columns)).reshape(rows, len(columns)),
            index=range(0, rows * interval, interval),
            columns=columns)

        # Determine what's expected
        expected = [
            {
                'close': 86.0,
                'high': 88.0,
                'low': 31.0,
                'open': 33.0,
                'timestamp': 84.0,
                'volume': 620.0},
            {
                'close': 146.0,
                'high': 148.0,
                'low': 91.0,
                'open': 93.0,
                'timestamp': 144.0,
                'volume': 1220.0}
        ]

        # Test
        result_ = evaluate.summary(data, periods=periods)
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp'))
        self.assertEqual(result, expected)

    def test_recent(self):
        """Testing function recent."""
        pass

    def test_sequential(self):
        """Testing function sequential."""
        # Initialize key values
        values = [
            False, False, False, True, False,
            True, False, True, True, True,
            True, True, False, False, True,
            False, False, False, False, False
        ]

        expected = [
            1, 2, 3, 1, 1,
            1, 1, 1, 2, 3,
            4, 5, 1, 2, 1,
            1, 2, 3, 4, 5]

        result = evaluate.sequential(pd.Series(values))
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
