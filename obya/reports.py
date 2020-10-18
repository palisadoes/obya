"""Application module to manage email formatting."""

import datetime

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

    # Create report
    pairs = pair.pairs()
    for pair_ in sorted(pairs):
        report_ = report(pair_, timeframe, days=days)
        if bool(report_) is True:
            output.append(report_)

    # Return
    result = '\n\n{}\n'.format('-' * width).join(output)
    return result


def report(_pair, timeframe, days=None):
    """Create reports.

    Args:
        _pair: Pair to Evaluate
        timeframe: Timeframe
        days: Age of report in days

    Returns:
        result: String report

    """
    # Initialize key variables
    if bool(days) is False:
        secondsago = 365 * 86400
    else:
        secondsago = days * 86400
    result = ''

    # Process data
    df_ = data.dataframe(_pair, timeframe, secondsago=None)
    if df_.empty is False:
        result_ = evaluate.evaluate(df_, 29)

        # Drop all rows that are older than days
        result_ = evaluate.recent(result_, secondsago=secondsago)

        # Create report
        if result_.empty is False:
            result = formatter(result_, _pair)
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
