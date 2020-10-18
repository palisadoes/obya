#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys
from operator import itemgetter

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
            periods=42
        )
    )

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_fast(self):
        """Testing function fast."""
        # Initalize key variables
        limit = 99.85

        expected = [
            {
                'close': 76.072,
                'd': 95.32805956258748,
                'high': 76.072,
                'k': 100.0,
                'low': 74.842,
                'open': 75.316,
                'sequential': 1.0,
                'timestamp': 1577361600.0,
                'volume': 461569.0},
            {
                'close': 76.154,
                'd': 97.55385459885271,
                'high': 76.156,
                'k': 99.91445680068394,
                'low': 74.842,
                'open': 75.214,
                'sequential': 2.0,
                'timestamp': 1577376000.0,
                'volume': 455266.0},
            {
                'close': 69.605,
                'd': 95.89611795590197,
                'high': 69.608,
                'k': 99.8709122203098,
                'low': 67.284,
                'open': 68.583,
                'sequential': 1.0,
                'timestamp': 1588118400.0,
                'volume': 636298.0},
            {
                'close': 71.114,
                'd': 84.81680956998703,
                'high': 71.117,
                'k': 99.88349514563106,
                'low': 68.572,
                'open': 68.75,
                'sequential': 1.0,
                'timestamp': 1590465600.0,
                'volume': 487421.0}
            ]

        # Get data
        above = evaluate.Above(self.df, limit=limit)
        result_ = above.fast

        # Test
        result = list(result_.T.to_dict().values())
        self.assertEqual(result, expected)

    def test_slow(self):
        """Testing function slow."""
        # Initalize key variables
        limit = 98.4

        expected = [
            {
                'close': 73.643,
                'd': 98.48676926683488,
                'high': 73.651,
                'k': 99.78384220480963,
                'low': 71.085,
                'open': 71.697,
                'sequential': 1.0,
                'timestamp': 1568030400.0,
                'volume': 811320.0},
            {
                'close': 73.569,
                'd': 98.42765215417081,
                'high': 73.658,
                'k': 97.59978425026972,
                'low': 71.085,
                'open': 71.509,
                'sequential': 2.0,
                'timestamp': 1568044800.0,
                'volume': 810805.0},
            {
                'close': 73.668,
                'd': 98.49321305481887,
                'high': 73.694,
                'k': 99.30555555555566,
                'low': 71.085,
                'open': 71.566,
                'sequential': 3.0,
                'timestamp': 1568059200.0,
                'volume': 801402.0},
            {
                'close': 74.944,
                'd': 98.45249701019864,
                'high': 74.966,
                'k': 99.65592743196761,
                'low': 70.191,
                'open': 70.52,
                'sequential': 1.0,
                'timestamp': 1591128000.0,
                'volume': 597115.0},
            {
                'close': 75.569,
                'd': 99.07275107362229,
                'high': 75.665,
                'k': 98.64655293951779,
                'low': 70.215,
                'open': 70.384,
                'sequential': 2.0,
                'timestamp': 1591142400.0,
                'volume': 601706.0}
            ]

        # Get data
        above = evaluate.Above(self.df, limit=limit)
        result_ = above.slow

        # Test
        result = list(result_.T.to_dict().values())
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
            periods=42
        )
    )

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_fast(self):
        """Testing function fast."""
        # Initalize key variables
        limit = 0.4

        expected = [
            {
                'close': 78.179,
                'd': 15.365495624313136,
                'high': 79.641,
                'k': 0.12254901960755822,
                'low': 78.177,
                'open': 79.515,
                'sequential': 1.0,
                'timestamp': 1551974400.0,
                'volume': 726819.0},
            {
                'close': 71.802,
                'd': 7.286698618858651,
                'high': 73.365,
                'k': 0.20072260136530165,
                'low': 71.797,
                'open': 72.746,
                'sequential': 1.0,
                'timestamp': 1570017600.0,
                'volume': 762582.0},
            {
                'close': 73.544,
                'd': 6.270072812073204,
                'high': 75.665,
                'k': 0.14124293785311207,
                'low': 73.541,
                'open': 75.262,
                'sequential': 1.0,
                'timestamp': 1573732800.0,
                'volume': 624713.0},
            {
                'close': 73.991,
                'd': 12.536208966162807,
                'high': 76.238,
                'k': 0.1776988005333132,
                'low': 73.987,
                'open': 75.934,
                'sequential': 1.0,
                'timestamp': 1580076000.0,
                'volume': 533561.0},
            {
                'close': 64.073,
                'd': 9.177950859497836,
                'high': 70.049,
                'k': 0.36217303822919944,
                'low': 64.046,
                'open': 69.837,
                'sequential': 1.0,
                'timestamp': 1584432000.0,
                'volume': 1332995.0}
            ]

        # Get data
        below = evaluate.Below(self.df, limit=limit)
        result_ = below.fast

        # Test
        result = list(result_.T.to_dict().values())
        self.assertEqual(result, expected)

    def test_slow(self):
        """Testing function slow."""
        # Initalize key variables
        limit = 3

        expected = [
            {
                'close': 73.979,
                'd': 1.402334911610705,
                'high': 76.0,
                'k': 0.7367387033399095,
                'low': 73.964,
                'open': 75.718,
                'sequential': 1.0,
                'timestamp': 1560830400.0,
                'volume': 686017.0},
            {
                'close': 74.082,
                'd': 2.51166407738639,
                'high': 76.0,
                'k': 7.655272026961577,
                'low': 73.923,
                'open': 75.685,
                'sequential': 2.0,
                'timestamp': 1560844800.0,
                'volume': 691036.0},
            {
                'close': 73.649,
                'd': 2.618728683322854,
                'high': 76.159,
                'k': 4.288354898336404,
                'low': 73.533,
                'open': 76.123,
                'sequential': 1.0,
                'timestamp': 1580155200.0,
                'volume': 543623.0},
            {
                'close': 72.532,
                'd': 2.2475757990867375,
                'high': 75.358,
                'k': 3.3133315940515367,
                'low': 72.405,
                'open': 75.309,
                'sequential': 1.0,
                'timestamp': 1580680800.0,
                'volume': 645049.0},
            {
                'close': 72.646,
                'd': 2.983186048301978,
                'high': 75.358,
                'k': 6.287503261153137,
                'low': 72.405,
                'open': 75.292,
                'sequential': 2.0,
                'timestamp': 1580688000.0,
                'volume': 654566.0}
            ]

        # Get data
        below = evaluate.Below(self.df, limit=limit)
        result_ = below.slow

        # Test
        result = list(result_.T.to_dict().values())
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
        limit = 10

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

        expected_data = {
            'close': {2566: 76.352, 2655: 77.346},
            'counts': {2566: 7, 2655: 6},
            'd_l': {2566: 89.22393014361, 2655: 90.0327966129483},
            'd_s': {2566: 93.16129032258061, 2655: 88.03735941877359},
            'delta_l': {2566: 0.5825214692939511, 2655: 1.6818178864760114},
            'delta_s': {2566: -3.354838709676656, 2655: 2.9513765011260205},
            'high': {2566: 76.431, 2655: 77.418},
            'k_l': {2566: 89.80645161290396, 2655: 91.71461449942431},
            'k_s': {2566: 89.80645161290396, 2655: 90.98873591989961},
            'low': {2566: 75.656, 2655: 76.662},
            'open': {2566: 75.909, 2655: 76.683},
            'sequential': {2566: 1.0, 2655: 1.0},
            'timestamp': {2566: 1596758400.0, 2655: 1598558400.0},
            'volume': {2566: 60664.0, 2655: 71270.0}
        }
        expected_ = pd.DataFrame(data=expected_data)

        # Get data
        data = files.ingest(filepath)
        result_ = evaluate.evaluate(
            data, periods, k_period=k_period, d_period=d_period).tail(2)

        # Test
        result = sorted(
            list(result_.T.to_dict().values()),
            key=itemgetter('timestamp'))
        expected = sorted(
            list(expected_.T.to_dict().values()),
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
