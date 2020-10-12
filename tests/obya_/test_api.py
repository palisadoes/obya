#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys
from collections import namedtuple

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
from obya import api


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test__interval_span(self):
        """Testing function _interval_span."""
        timeframes = [60, 3600, 86400, 604800]
        multiplier = 4
        Meta = namedtuple('Meta', 'interval span')
        expected = [
            Meta(interval='MINUTE', span=1),
            Meta(interval='HOUR', span=1),
            Meta(interval='DAY', span=1),
            Meta(interval='WEEK', span=1),
        ]
        for pointer, timeframe in enumerate(timeframes):
            result = api._interval_span(timeframe)
            self.assertEqual(result, expected[pointer])
        for pointer, timeframe in enumerate(timeframes):
            result = api._interval_span(timeframe * multiplier)
            self.assertEqual(result.interval, expected[pointer].interval)
            self.assertEqual(result.span, expected[pointer].span * multiplier)

    def test__convert(self):
        """Testing function _convert."""
        # Initialize key variables
        data = {
            'PriceBars': [
                {'BarDate': '/Date(1602450000000)/', 'Open': 1.30259,
                 'High': 1.30305, 'Low': 1.30242, 'Close': 1.30291},
                {'BarDate': '/Date(1602453600000)/', 'Open': 1.30292,
                 'High': 1.30349, 'Low': 1.30285, 'Close': 1.30342},
                {'BarDate': '/Date(1602457200000)/', 'Open': 1.30342,
                 'High': 1.3038, 'Low': 1.30281, 'Close': 1.30306},
                {'BarDate': '/Date(1602460800000)/', 'Open': 1.30306,
                 'High': 1.30343, 'Low': 1.30232, 'Close': 1.30291},
                {'BarDate': '/Date(1602464400000)/', 'Open': 1.30291,
                 'High': 1.30338, 'Low': 1.30203, 'Close': 1.30289},
                {'BarDate': '/Date(1602468000000)/', 'Open': 1.30288,
                 'High': 1.30307, 'Low': 1.30244, 'Close': 1.30282},
                {'BarDate': '/Date(1602471600000)/', 'Open': 1.30281,
                 'High': 1.30331, 'Low': 1.30265, 'Close': 1.30318},
                {'BarDate': '/Date(1602475200000)/', 'Open': 1.30319,
                 'High': 1.3041, 'Low': 1.30318, 'Close': 1.30404},
                {'BarDate': '/Date(1602478800000)/', 'Open': 1.30403,
                 'High': 1.30468, 'Low': 1.30393, 'Close': 1.30435},
                {'BarDate': '/Date(1602482400000)/', 'Open': 1.30437,
                 'High': 1.3057, 'Low': 1.30396, 'Close': 1.30502},
                {'BarDate': '/Date(1602486000000)/', 'Open': 1.30502,
                 'High': 1.30597, 'Low': 1.3025, 'Close': 1.30316},
                {'BarDate': '/Date(1602489600000)/', 'Open': 1.30316,
                 'High': 1.30377, 'Low': 1.30136, 'Close': 1.30143},
                {'BarDate': '/Date(1602493200000)/', 'Open': 1.30139,
                 'High': 1.30277, 'Low': 1.30085, 'Close': 1.30274}
            ],
            'PartialPriceBar': {
                'BarDate': '/Date(1602518400000)/', 'Open': 1.3062,
                'High': 1.30697, 'Low': 1.30572, 'Close': 1.30627
            }
        }
        expected = [
            {'close': 1.30291,
             'high': 1.30305,
             'low': 1.30242,
             'open': 1.30259,
             'timestamp': 1602450000},
            {'close': 1.30342,
             'high': 1.30349,
             'low': 1.30285,
             'open': 1.30292,
             'timestamp': 1602453600},
            {'close': 1.30306,
             'high': 1.3038,
             'low': 1.30281,
             'open': 1.30342,
             'timestamp': 1602457200},
            {'close': 1.30291,
             'high': 1.30343,
             'low': 1.30232,
             'open': 1.30306,
             'timestamp': 1602460800},
            {'close': 1.30289,
             'high': 1.30338,
             'low': 1.30203,
             'open': 1.30291,
             'timestamp': 1602464400},
            {'close': 1.30282,
             'high': 1.30307,
             'low': 1.30244,
             'open': 1.30288,
             'timestamp': 1602468000},
            {'close': 1.30318,
             'high': 1.30331,
             'low': 1.30265,
             'open': 1.30281,
             'timestamp': 1602471600},
            {'close': 1.30404,
             'high': 1.3041,
             'low': 1.30318,
             'open': 1.30319,
             'timestamp': 1602475200},
            {'close': 1.30435,
             'high': 1.30468,
             'low': 1.30393,
             'open': 1.30403,
             'timestamp': 1602478800},
            {'close': 1.30502,
             'high': 1.3057,
             'low': 1.30396,
             'open': 1.30437,
             'timestamp': 1602482400},
            {'close': 1.30316,
             'high': 1.30597,
             'low': 1.3025,
             'open': 1.30502,
             'timestamp': 1602486000},
            {'close': 1.30143,
             'high': 1.30377,
             'low': 1.30136,
             'open': 1.30316,
             'timestamp': 1602489600},
            {'close': 1.30274,
             'high': 1.30277,
             'low': 1.30085,
             'open': 1.30139,
             'timestamp': 1602493200}
        ]

        result = api._convert(data)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
