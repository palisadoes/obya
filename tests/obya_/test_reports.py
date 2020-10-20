#!/usr/bin/env python3
"""Test the reports module."""

# Standard imports
import unittest
import os
import sys
import time

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
from obya import reports
from obya.ingest import files


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    # Initialize key variables
    k_period = 5
    d_period = 3
    periods = 4
    filepath = '{0}{1}tests{1}data{1}test_ingest_2_years.csv'.format(
        ROOT_DIR, os.sep)
    pair = 'abc123'
    timeframe = 14400

    # Get data
    data = files.ingest(filepath)
    data['date'] = [
        time.strftime('%Y-%m-%d %H:%M %a', time.gmtime(_)) for _ in data[
            'timestamp'].tolist()]

    def test_reports(self):
        """Testing function reports."""
        pass

    def test_report(self):
        """Testing function report."""
        pass

    def test__report(self):
        """Testing function _report."""
        # Initialize key variables
        days = int(time.time() / 86400)

        expected = {
            'pair': 'abc123',
            'report': '''\
ABC123

                        k_l    d_l   Δ_l    k_s    d_s    Δ_s  seq   cnt
date
2020-09-01 16:00 Tue  98.69  96.69  1.99  90.63  88.54   2.09  2.0  19.0
2020-09-01 12:00 Tue  98.60  96.39  2.21  90.19  87.86   2.33  1.0  18.0
2020-09-01 04:00 Tue  98.83  96.43  2.40  91.78  90.36   1.42  1.0  17.0
2020-08-31 12:00 Mon  99.68  95.76  3.92  97.67  89.88   7.79  2.0  13.0
2020-08-28 08:00 Fri  97.12  94.84  2.27  77.87  90.77 -12.90  7.0  12.0
2020-08-28 00:00 Fri  99.28  95.87  3.40  93.53  94.62  -1.09  5.0  10.0
2020-08-27 08:00 Thu  99.51  95.76  3.75  94.01  92.03   1.98  1.0   6.0
2020-08-27 00:00 Thu  99.12  95.39  3.73  95.45  88.39   7.06  3.0   7.0
2020-08-26 16:00 Wed  98.85  95.37  3.49  91.59  84.96   6.63  1.0   5.0
2020-08-26 00:00 Wed  98.75  95.72  3.03  90.13  74.06  16.07  1.0   4.0
2020-08-21 16:00 Fri  93.00  93.24 -0.25   6.09  25.52 -19.43  1.0   4.0
2020-08-20 12:00 Thu  93.28  94.13 -0.85   1.41  20.58 -19.16  2.0   3.0
2020-08-20 08:00 Thu  93.81  94.90 -1.09   5.25  33.67 -28.42  1.0   2.0
2020-08-05 12:00 Wed  96.42  92.54  3.87  90.46  89.44   1.03  3.0   4.0
2020-08-05 04:00 Wed  94.26  92.35  1.91  97.09  80.20  16.88  1.0   2.0
2020-07-30 08:00 Thu  88.94  89.20 -0.26   6.52  21.66 -15.15  1.0   1.0
2020-07-15 00:00 Wed  89.61  85.69  3.93  94.77  67.88  26.88  1.0   2.0
2020-07-10 04:00 Fri  84.55  82.60  1.96   0.41  35.84 -35.43  1.0   9.0
2020-07-06 16:00 Mon  89.07  86.04  3.03  88.08  91.64  -3.56  5.0  10.0
2020-07-06 00:00 Mon  88.57  84.83  3.74  96.87  92.23   4.64  1.0   6.0
2020-07-03 20:00 Fri  86.86  84.95  1.91  90.05  89.36   0.69  3.0   5.0
2020-07-03 12:00 Fri  87.08  84.12  2.96  92.77  84.19   8.58  1.0   3.0
2020-07-01 00:00 Wed  87.48  88.04 -0.57  99.20  76.03  23.17  2.0   2.0
2020-06-30 20:00 Tue  86.42  86.25  0.18  92.81  71.49  21.32  1.0   1.0
2020-06-12 00:00 Fri  75.23  71.76  3.47   0.10   3.86  -3.77  3.0  14.0
2020-05-15 20:00 Fri  52.46  54.00 -1.54   4.80  17.90 -13.10  1.0   4.0
2020-05-08 20:00 Fri  58.15  54.16  3.99  92.70  86.95   5.75  3.0   6.0
2020-05-06 16:00 Wed  48.00  51.95 -3.95   1.00  12.03 -11.03  2.0   7.0
2020-05-06 12:00 Wed  48.96  51.93 -2.97   3.72  16.32 -12.60  1.0   7.0
2020-05-03 21:00 Sun  49.04  51.43 -2.39   2.13  16.26 -14.12  1.0  21.0
2020-04-21 08:00 Tue  44.74  42.11  2.62   0.47  20.33 -19.86  2.0   2.0
2020-04-21 04:00 Tue  46.17  42.47  3.70   3.11  34.50 -31.39  1.0   2.0
2020-01-21 16:00 Tue  78.87  82.59 -3.73   4.04  14.95 -10.91  1.0   6.0
2020-01-21 04:00 Tue  82.80  81.65  1.15   9.84  20.25 -10.42  1.0   7.0
2020-01-07 16:00 Tue  69.65  69.56  0.09   8.43  10.60  -2.17  1.0   5.0
2020-01-07 08:00 Tue  69.56  70.79 -1.23   3.15  17.11 -13.96  2.0   4.0
2020-01-07 04:00 Tue  72.64  70.71  1.93   1.78  20.53 -18.75  1.0   3.0
2019-12-04 04:00 Wed  39.11  40.10 -0.99   3.18  38.60 -35.42  1.0   5.0
2019-12-03 00:00 Tue  44.33  42.07  2.26  96.66  82.24  14.42  1.0   5.0
2019-12-02 00:00 Mon  40.67  41.76 -1.09  98.56  71.25  27.31  1.0   4.0
2019-11-29 08:00 Fri  39.72  40.58 -0.86  91.08  81.84   9.24  1.0   3.0
2019-11-27 16:00 Wed  40.11  40.96 -0.86  99.11  81.34  17.78  2.0   2.0
2019-11-27 12:00 Wed  39.11  40.61 -1.50  98.26  75.52  22.74  1.0   1.0
2019-11-14 04:00 Thu  37.68  41.60 -3.92  11.13   7.98   3.15  2.0  10.0
2019-11-13 16:00 Wed  40.37  40.76 -0.39   7.18  10.58  -3.41  3.0   8.0
2019-11-13 08:00 Wed  40.96  43.01 -2.05   3.33   9.45  -6.12  1.0   6.0
2019-11-13 00:00 Wed  42.77  43.88 -1.11  14.53   9.18   5.35  1.0   5.0
2019-11-12 16:00 Tue  42.85  42.68  0.17   2.82  12.73  -9.92  1.0   3.0
2019-11-11 20:00 Mon  43.86  41.51  2.35   9.95  12.18  -2.23  1.0   3.0
2019-11-11 08:00 Mon  43.74  41.27  2.47   8.78  21.45 -12.67  1.0   2.0
2019-10-11 04:00 Fri  30.55  29.26  1.30  97.10  95.37   1.72  2.0   5.0'''
            }

        # Test
        result = reports._report(
            self.pair, self.timeframe, days=days, dataframe=self.data)
        self.assertEqual(result, expected)

    def test_formatter(self):
        """Testing function formatter."""
        pass

    def test__no_sequential_matches(self):
        """Testing function _no_sequential_matches."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
