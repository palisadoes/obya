"""Application evaluation module."""

import ta
import pandas as pd
from pprint import pprint

from obya import log
from obya import ingest


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
        self._df = stoch(_df, k_period=k_period, d_period=d_period)

    def above(self, limit=90, fast=True):
        """Get DataFrame rows where Stochastic is greater than a value.

        Args:
            limit: Value
            fast: Get values from fast Stochastic if True, else slow

        Returns:
            result: DataFrame

        """
        # Return
        if bool(fast) is False:
            result = self._df.loc[self._df['d'] >= limit]
        else:
            result = self._df.loc[self._df['k'] >= limit]
        return result

    def below(self, limit=10, fast=True):
        """Get DataFrame rows where Stochastic is less than a value.

        Args:
            limit: Value
            fast: Get values from fast Stochastic if True, else slow

        Returns:
            result: DataFrame

        """
        # Return
        if bool(fast) is False:
            result = self._df.loc[self._df['d'] <= limit]
        else:
            result = self._df.loc[self._df['k'] <= limit]
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
        df_: DataFrame to analyse
        periods: Timeframe to evaluate
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

    # Get DataFrame
    evaluate_4 = Evaluate(df_, k_period=k_period, d_period=d_period)
    hour_4 = evaluate_4.either()

    # Get DataFrame using weekly timeframe (42, 4 hour periods)
    df_168 = summary(df_, periods=periods)
    # df_168 = batch(summary_, boundary=boundary)
    evaluate_168 = Evaluate(df_168, k_period=k_period, d_period=d_period)
    hour_168 = evaluate_168.difference(limit=4)

    # Get common index values
    index_4 = hour_4.index.tolist()
    index_168 = hour_168.index.tolist()
    indexes = tuple(set(index_4).intersection(index_168))

    print('\n\n\n', len(hour_4), len(hour_168), '\n\n\n')

    # Filter DataFrame by indexes
    # result = df_.loc[df_.index.isin(indexes)]
    result = hour_168.copy()
    result['delta'] = result['k'] - result['d']
    result['h4_k'] = hour_4['k']
    result['h4_d'] = hour_4['d']
    result['h4_delta'] = hour_4['k'] - hour_4['d']
    result = result.loc[result.index.isin(indexes)]
    result = frequency(result, hour_4)
    print(ingest.date(result))

    # Calculate the frequencies

    # print('\n\n\n')
    # result = frequency(hour_168, hour_4)
    # print(ingest.date(result))
    # # print('\n\n\n')
    # # print(ingest.date(hour_4))
    # print('\n\n\n')
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
    l_index = sorted(long.index.tolist())
    s_index = sorted(short.index.tolist())
    counts = {}
    column = []

    # Count the occurences
    for _, pointer in enumerate(l_index):
        indexes = list(range(pointer, pointer - periods, - 1))
        count = 0
        for index in s_index:
            if index in indexes:
                count += 1
        counts[pointer] = count

    # Add ocurrences to DataFrame
    if bool(counts) is True:
        column = counts.values()
        long['counts'] = column
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
    result = df_[k_period + 1:]
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
