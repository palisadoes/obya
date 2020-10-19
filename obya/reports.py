"""Application module to manage email formatting."""

import datetime
from multiprocessing import Pool
from operator import itemgetter

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

    # Create argument list for report
    pairs = pair.pairs()
    for item in pairs:
        if item.lower() == 'audjpy':
            arguments.append(
                (item, timeframe, days)
            )

    # Multiprocess the results
    with Pool(processes=4) as pool:
        reporting = pool.starmap(_report, arguments)

    # Get report
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
    result = ''
    result_ = _report(_pair, timeframe, days=days)
    for _, result in result_.items():
        break
    return result


def _report(_pair, timeframe, days=None):
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

    # Account for giving enough extra time for calculating the stochastic
    # for the summarized timeframe.
    offset = timeframe * summary * (k_period + d_period) * 2

    # Define lookback timeframe
    if bool(days) is False:
        secondsago = (365 * 86400) + offset
    else:
        # Account for giving enough extra time for calculating the stochastic
        # for the summarized timeframe.
        secondsago = (days * 86400) + offset
    result = {}

    # Process data
    df_ = data.dataframe(_pair, timeframe, secondsago=secondsago)
    if df_.empty is False:
        result_ = evaluate.evaluate(
            df_, summary, k_period=k_period, d_period=d_period)

        # Drop all rows that are older than days
        result_ = evaluate.recent(result_, secondsago=secondsago)

        # Create report
        if result_.empty is False:
            result = {'pair': _pair, 'report': formatter(result_, _pair)}

    # Return
    return result


def formatter(_df, _pair):
    """Read a configuration file.

    Args:
        _df: DataFrame
        _pair: Pair corresponding to DataFrame

    Returns:
        result: Formatted string

    """
    # Initialize key variables
    result = ''
    drops = 'timestamp open high low close volume Δ_s'
    rounding = {
        'k_l': 2,
        'd_l': 2,
        'k_s': 2,
        'd_s': 2,
        'Δ_l': 2,
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

        # Drop unwanted columns. Reset index to 'date'
        df_ = df_.drop(columns=drops.split())
        df_.set_index('date', inplace=True)

        # Add data to report
        result = '{}\n{}'.format(result, df_.to_string())
    return result
