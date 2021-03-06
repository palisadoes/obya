"""Application module to manage email formatting."""

import datetime
from multiprocessing import cpu_count, get_context
from operator import itemgetter

import numpy as np
import pandas as pd

# Application imports
from obya.db.table import pair
from obya.db.table import data
from obya import evaluate


def reports(timeframe, days=None, width=60):
    """Create reports.

    Args:
        timeframe: Timeframe
        days: Age of report in days

    Returns:
        result: String report

    """
    # Initialize key variables
    output = []
    arguments = []
    reporting = []
    cpus = max(1, cpu_count() - 2)

    # Create argument list for report
    pairs = pair.pairs()
    for item in pairs:
        arguments.append(
            (item, timeframe, days)
        )

    # Multiprocess the results
    with get_context('spawn').Pool(processes=cpus) as pool:
        reporting = pool.starmap(_report, arguments)
    pool.join()

    # Process non-blank reports
    reporting = [_ for _ in reporting if bool(_) is True]
    for item in sorted(reporting, key=itemgetter('report')):
        if bool(item) is True:
            output.append(item['report'])

    # Return
    result = '\n\n{}\n'.format('-' * width).join(output)
    return result


def report(_pair, timeframe, days=None):
    """Create report.

    Args:
        _pair: Pair to Evaluate
        timeframe: Timeframe
        days: Age of report in days

    Returns:
        result: String report

    """
    # Return
    result_ = _report(_pair, timeframe, days=days)
    result = result_.get('report', '')
    return result


def _report(_pair, timeframe, days=None, dataframe=None):
    """Create reports.

    Args:
        _pair: Pair to Evaluate
        timeframe: Timeframe
        days: Age of report in days

    Returns:
        result: String report

    """
    # Initialize key variables
    k_period = 35
    d_period = 5
    summary = 29
    result = {}

    # Account for giving enough extra time for calculating the stochastic
    # for the summarized timeframe.
    offset = timeframe * summary * (k_period * d_period)

    # Define lookback timeframe
    if bool(days) is False:
        secondsago = (365 * 86400) + offset
    else:
        # Account for giving enough extra time for calculating the stochastic
        # for the summarized timeframe.
        secondsago = (days * 86400) + offset

    # Process data
    if isinstance(dataframe, pd.DataFrame) is False:
        df_ = data.dataframe(_pair, timeframe, secondsago=secondsago)
    else:
        df_ = dataframe.copy()

    if df_.empty is False:
        result_ = evaluate.evaluate(
            df_, summary, k_period=k_period, d_period=d_period)

        # Drop all rows that are older than days
        result_ = evaluate.recent(result_, secondsago=(secondsago - offset))

        # Create report
        if result_.empty is False:
            result = {
                'pair': _pair,
                'report': formatter(result_, _pair, timeframe=timeframe)
            }

    # Return
    return result


def formatter(_df, _pair, timeframe=14400):
    """Read a configuration file.

    Args:
        _df: DataFrame
        _pair: Pair corresponding to DataFrame
        timeframe: Timeframe

    Returns:
        result: Formatted string

    """
    # Initialize key variables
    result = ''
    drops = 'timestamp open high low close volume'
    rounding = {
        'k_l': 2,
        'd_l': 2,
        'Δ_l': 2,
        'k_s': 2,
        'd_s': 2,
        'Δ_s': 2,
        'seq': 0,
        'cnt': 0,
    }
    secondsago = 3600 * 24 * 7
    df_ = _df.copy()

    # Get starting time for 'star' column
    now = datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc).timestamp()
    start = now - secondsago

    # Process
    if df_.empty is False:
        # Create heading for the _pair
        result = '{}\n'.format(_pair.upper())

        # Create 'star' column
        timestamp = df_['timestamp']
        filtered = timestamp.where(timestamp > start, other='').tolist()
        df_[''] = ['*' if bool(_) is True else '' for _ in filtered]

        # Round columns
        df_ = df_.round(rounding)

        # Rename columns
        df_ = df_.rename(
            columns={
                'sequential': 'seq',
                'counts': 'cnt'
            }
        )

        # Remove rows with sequential matches
        df_ = _no_sequential_matches(df_, timeframe=timeframe)

        # Reverse sort the results
        df_ = df_.sort_values(by=['timestamp'], ascending=False)

        # Drop unwanted columns. Reset index to 'date'
        df_ = df_.drop(columns=drops.split())
        df_.set_index('date', inplace=True)

        # Add data to report
        result = '{}\n{}'.format(result, df_.to_string())

        # Trim trailing spaces from each line of output
        result = '\n'.join([_.rstrip() for _ in result.split('\n')])
    return result


def _no_sequential_matches(_df, timeframe=14400):
    """Read a configuration file.

    Args:
        _df: DataFrame
        timeframe: Timeframe

    Returns:
        result: Formatted string

    """
    # Initialize key variables
    df_ = _df.copy().sort_values(by=['timestamp'])
    d_col = 'diff'
    l_col = 'last'

    # Get diffs and filter
    result = df_.copy()[1:]
    result[d_col] = df_['timestamp'][1:] - df_['timestamp'].shift(1)[1:]

    # Identify lasts
    diffs = result[d_col].tolist()
    lasts = []
    for key, value in enumerate(diffs[:-1]):
        not_last = (int(diffs[key + 1]) == timeframe) and (value == timeframe)
        lasts.append(not_last)
    lasts.append(False)
    lasts = [not bool(_) for _ in lasts]
    result[l_col] = np.asarray(lasts)

    # Filter and drop excess column
    result = result[result[l_col] == True]
    result = result.drop(columns=[l_col, d_col])

    # Return
    return result
