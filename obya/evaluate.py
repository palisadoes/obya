"""Application evaluation module."""

# Standard imports
from datetime import timezone
import datetime
from itertools import groupby

# PIP3 imports
import ta
import pandas as pd

# Appliation imports
from obya import log


class Evaluate():
    """Class to evaluate dataframe."""

    def __init__(self, _df, k_period=35, d_period=5):
        """Initialize the class.

        Args:
            _df: pd.DataFrame
            k_period: Periods for calculating Stochastic slow indicator
            d_period: Moving Average periods for smoothing Stochastic to create
                the fast indicator

        Returns:
            None

        """
        # Initalize key variables
        df_ = _df.copy()
        self._df = stoch(df_, k_period=k_period, d_period=d_period)

    def above(self, limit=90, fast=True):
        """Get DataFrame rows where Stochastic is greater than a value.

        Args:
            limit: Value
            fast: Get values from fast Stochastic if True, else slow

        Returns:
            result: DataFrame

        """
        # Initalize key variables
        df_ = self._df.copy()

        # Return
        if bool(fast) is False:
            series = df_['d']
            df_['sequential'] = sequential(series.where(series >= limit, False))
            result = df_.loc[df_['d'] >= limit]
        else:
            series = df_['k']
            df_['sequential'] = sequential(series.where(series >= limit, False))
            result = df_.loc[df_['k'] >= limit]
        return result

    def below(self, limit=10, fast=True):
        """Get DataFrame rows where Stochastic is less than a value.

        Args:
            limit: Value
            fast: Get values from fast Stochastic if True, else slow

        Returns:
            result: DataFrame

        """
        # Initalize key variables
        df_ = self._df.copy()

        # Return
        if bool(fast) is False:
            series = df_['d']
            df_['sequential'] = sequential(series.where(series <= limit, False))
            result = df_.loc[df_['d'] <= limit]
        else:
            series = df_['k']
            df_['sequential'] = sequential(series.where(series <= limit, False))
            result = df_.loc[df_['k'] <= limit]
        return result

    def difference(self, limit=1):
        """Get DataFrame rows where Stochastic difference is less than a value.

        Args:
            limit: Value

        Returns:
            result: DataFrame

        """
        # Return
        result = self._df.loc[abs(self._df['d'] - self._df['k']) < limit]
        return result

    def either(self, below=10, above=90):
        """Create DataFrame that meets evaluation criteria.

        Args:
            below: Below limit
            above: Above limit

        Returns:
            result: DataFrame that matches criteria

        """
        # Initialize key variables
        matches_ = {}

        # Get index values where the Stochastic indicators
        # exceed the desired limits
        for fast in [True, False]:
            for item in self.above(above, fast=fast).index.tolist():
                matches_[item] = None
            for item in self.below(below, fast=fast).index.tolist():
                matches_[item] = None

        # Get the indexes with matches in both cases
        indexes = tuple(sorted(matches_.keys()))

        # Return
        result = self._df[self._df.index.isin(indexes)]
        return result


def evaluate(_df, periods, k_period=35, d_period=5):
    """Evaluate data.

    Args:
        df_: Short term DataFrame to analyse
        periods: Number of periods per long term timeframe
        k_period: Periods for calculating Stochastic slow indicator
        d_period: Moving Average periods for smoothing Stochastic to create
            the fast indicator

    Returns:
        None

    """
    # Initialize key variables
    k_period = 35
    d_period = 5
    # boundary = 604800
    df_ = _df.copy()

    # Evaluate DataFrame
    s_eval = Evaluate(df_, k_period=k_period, d_period=d_period)
    s_term = s_eval.either()

    # Evaluate DataFrame by summarizing (ie. `periods` number of periods)
    s_summary = summary(df_, periods=periods)
    l_eval = Evaluate(s_summary, k_period=k_period, d_period=d_period)
    l_term = l_eval.difference(limit=4)

    # Get common index values
    indexes = tuple(
        set(
            s_term.index.tolist()
        ).intersection(
            l_term.index.tolist()
        )
    )

    # Filter DataFrame by indexes
    result = l_term.copy()
    result = result.rename(columns={'k': 'k_l', 'd': 'd_l'})
    result['delta_l'] = result['k_l'] - result['d_l']
    result['k_s'] = s_term['k']
    result['d_s'] = s_term['d']
    result['sequential'] = s_term['sequential']
    result['delta_s'] = s_term['k'] - s_term['d']
    result = result.loc[result.index.isin(indexes)]
    result = frequency(result, s_term)
    return result


def frequency(long_, short_, periods=28, no_zeros=True):
    """Determine frequency of short instances in long time frame.

    Calculates the number of times within a time period that indexes in the
    short DataFrame match those of the long DataFrame.

    Args:
        long_: DataFrame on long time horizon
        short_: DataFrame on short time horizon
        periods: Number of short periods to create a long period

    Returns:
        result: DataFrame with count column added

    """
    # Initialize key variables
    long = long_.copy()
    short = short_.copy()
    counts = {}

    # Count the occurences
    for _, pointer in enumerate(sorted(long.index.tolist())):
        indexes = list(range(pointer, pointer - periods, - 1))
        count = 0
        for index in sorted(short.index.tolist()):
            if index in indexes:
                count += 1
        counts[pointer] = count

    # Add ocurrences to DataFrame
    if bool(counts) is True:
        long['counts'] = counts.values()
    else:
        long['counts'] = [0] * len(long)

    # Remove entries where the count is zero
    if no_zeros is True:
        result = long.loc[long['counts'] != 0]
    else:
        result = long.copy()
    return result


def stoch(_df, k_period=35, d_period=5):
    """Add stochastic indicators to pd.DataFrame.

    Args:
        _df: pd.DataFrame
        k_period: Periods for calculating Stochastic slow indicator
        d_period: Moving Average periods for smoothing Stochastic to create
            the fast indicator

    Returns:
        result: Modified DataFrame

    """
    # Initialize key variables
    df_ = _df.copy()

    # Get oscillator
    oscillator = ta.momentum.StochasticOscillator(
        high=df_['high'],
        low=df_['low'],
        close=df_['close'],
        n=k_period,
        d_n=d_period
        )

    # Add columns to DataFrame
    df_['k'] = oscillator.stoch()
    df_['d'] = oscillator.stoch_signal()
    result = df_[k_period + d_period:]
    return result


def summary(_df, periods=5):
    """Create a DataFrame summarizing past events.

    Args:
        _df: pd.DataFrame
        periods: Number of previous periods to include in summarization

    Returns:
        result: Modified DataFrame

    """
    # Initialize key variables
    df_ = _df.copy()
    df_['low'] = df_['low'].rolling(periods).min()
    df_['high'] = df_['high'].rolling(periods).max()
    df_['volume'] = df_['volume'].rolling(periods).sum()
    df_['open'] = df_['open'].shift(periods - 1)
    result = df_[periods - 1:]
    return result


def batch(_df, boundary=604800):
    """Get DataFrame entries on a timestamp boundary.

    Args:
        _df: pd.DataFrame
        boundary: Timestamp boundary

    Returns:
        result: Modified DataFrame

    """
    # Initialize key variables
    df_ = _df.copy()

    # Apply offset to account for the fact that epoch time is calculated from
    # midnight, 1/1/1970 which was a Thursday. Weekly day boundaries are
    # calculated starting at midnight, Sunday.
    offset = 259200

    if boundary == 604800:
        # Apply offset to account for the fact that epoch time is calculated
        # from midnight, 1/1/1970 which was a Thursday. Four hour week
        # boundaries are calculated ending at 20:00, friday.
        offset = 158400
    else:
        log_message = 'Boundary value {} is not valid'.format(boundary)
        log.log2die(1012, log_message)

    # Return
    result = df_.loc[((df_['timestamp'] - offset) % boundary) == 0]
    return result


def recent(_df, secondsago=5184000/2):
    """Get only the most recent entries in a DataFrame.

    Args:
        _df: DataFrame
        secondsago: Maximum age of DataFrame entries

    Returns:
        result: String report

    """
    # Initialize key variables
    result = pd.DataFrame()
    df_ = _df.copy()

    # Get starting time
    now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
    start = now - secondsago

    # Process data
    if df_.empty is False:
        # Drop all rows that are older than days
        result = df_.loc[df_['timestamp'] >= start]

    return result


def sequential(series):
    """Return a list of occurences in a series.

    Args:
        series: pd.series of True / False values

    Returns:
        result: List of sequential occurences

    """
    # Initalize key variables
    result = []

    # Create list of occurences
    occurences = [int(bool(_) is True) for _ in series.tolist()]
    duplicate_count = [
        sum(1 for _ in group) for _, group in groupby(occurences)]

    # Create sequential count
    for count in duplicate_count:
        result.extend(range(1, count))
        result.append(count)

    return result
