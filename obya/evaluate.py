"""Application evaluation module."""

# Standard imports
from datetime import timezone
import datetime
from itertools import groupby

# PIP3 imports
import ta
import pandas as pd


class Either():
    """Class to identify dataframe stochastic values beyond a limit."""

    def __init__(self, _df, limit=90, greater=True):
        """Initialize the class.

        Args:
            _df: stochastic pd.DataFrame
            limit: Value above/below which we care
            greater: Limit is above, if True

        Returns:
            None

        """
        # Initalize key variables
        self._df = _df
        self._limit = limit
        self._greater = bool(greater)

    @property
    def fast(self):
        """Get DataFrame rows where fast Stochastic is greater than a value.

        Args:
            None

        Returns:
            result: DataFrame

        """
        # Return
        result = self._process('k')
        return result

    @property
    def slow(self):
        """Get DataFrame rows where slow Stochastic is greater than a value.

        Args:
            None

        Returns:
            result: DataFrame

        """
        # Return
        result = self._process('d')
        return result

    def _process(self, column):
        """Get DataFrame rows where fast Stochastic is greater than a value.

        Args:
            None

        Returns:
            result: DataFrame

        """
        # Initalize key variables
        _df = self._df.copy()
        series = _df[column]

        # Find matches
        if self._greater is True:
            matches = series.where(series >= self._limit, other=False)
            _df['sequential'] = sequential(matches)
            result = _df.loc[series >= self._limit]

        else:
            matches = series.where(series <= self._limit, other=False)
            _df['sequential'] = sequential(matches)
            result = _df.loc[series <= self._limit]

        # Return
        return result


class Above(Either):
    """Class to identify dataframe stochastic values above a limit."""

    def __init__(self, _df, limit=90):
        """Initialize the class.

        Args:
            _df: stochastic pd.DataFrame
            limit: Value above which we care

        Returns:
            None

        """
        # Initalize key variables
        Either.__init__(self, _df, limit=limit, greater=True)


class Below(Either):
    """Class to identify dataframe stochastic values below a limit."""

    def __init__(self, _df, limit=90):
        """Initialize the class.

        Args:
            _df: stochastic pd.DataFrame
            limit: Value below which we care

        Returns:
            None

        """
        # Initalize key variables
        Either.__init__(self, _df, limit=limit, greater=False)


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
        # Return
        _above = Above(self._df, limit=limit)
        result = _above.fast if bool(fast) else _above.slow
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
        _below = Below(self._df, limit=limit)
        result = _below.fast if bool(fast) else _below.slow
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
        # Merge both DataFrames where they don't share index values
        df1 = self.above(above, fast=True)
        df2 = self.above(above, fast=False)
        _above = _min_sequential(df1, df2)

        # Merge both DataFrames where they don't share index values
        df1 = self.below(below, fast=True)
        df2 = self.below(below, fast=False)
        _below = _min_sequential(df1, df2)

        # Merge above and below
        result = pd.concat([_above, _below])

        # Return
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
    df_ = _df.copy()
    lt_index = []

    # Evaluate DataFrame
    s_eval = Evaluate(df_, k_period=k_period, d_period=d_period)
    s_term = s_eval.either()

    # Get a list of timestamps
    timestamps = s_term['timestamp'].tolist()

    for timestamp in timestamps:
        # Get values upto the current timestamp
        temp_data = df_[df_['timestamp'] <= timestamp]

        # Get long term values
        # Evaluate DataFrame by summarizing (ie. `periods` number of periods)
        temp_summ = summary(temp_data, periods=periods)

        temp_eval = Evaluate(temp_summ, k_period=k_period, d_period=d_period)
        temp_long = temp_eval.difference(limit=4)

        lt_index.extend(temp_long.index.tolist())

    # Get unique values
    lt_index = list(set(lt_index))

    # Get common index values
    indexes = tuple(
        set(
            s_term.index.tolist()
        ).intersection(
            lt_index
        )
    )

    # Create the stochastic version of the long timeframe
    result = summary(
        stoch(df_, k_period=k_period, d_period=d_period),
        periods=periods, crawling=False)
    result = result.rename(columns={'k': 'k_l', 'd': 'd_l'})

    # Add long term columns
    result['Δ_l'] = result['k_l'] - result['d_l']

    # Add short term columns
    result['Δ_s'] = s_term['k'] - s_term['d']
    result['k_s'] = s_term['k']
    result['d_s'] = s_term['d']
    result['sequential'] = s_term['sequential']

    # Filter by shared indexes
    result = result.loc[result.index.isin(indexes)]

    # Add the frequency column
    result = frequency(result, s_term, periods=periods)

    # Return
    return result


def _evaluate(_df, periods, k_period=35, d_period=5):
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
    result['Δ_l'] = result['k_l'] - result['d_l']
    result['Δ_s'] = s_term['k'] - s_term['d']
    result['k_s'] = s_term['k']
    result['d_s'] = s_term['d']
    result['sequential'] = s_term['sequential']
    result = result.loc[result.index.isin(indexes)]
    result = frequency(result, s_term)
    return result


def summary(_df, periods=5, crawling=False):
    """Create a DataFrame summarizing past events.

    Args:
        _df: pd.DataFrame
        periods: Number of previous periods to include in summarization
        crawling:

    Returns:
        result: Modified DataFrame

    """
    # Initialize key variables
    df_ = _df.copy()
    df_['low'] = df_['low'].rolling(periods).min()
    df_['high'] = df_['high'].rolling(periods).max()
    df_['volume'] = df_['volume'].rolling(periods).sum()
    df_['open'] = df_['open'].shift(periods - 1)

    # Trim NaNs
    result = df_[periods - 1:]

    # Get every `period` row and reverse sort the index to
    # mimic the original ordering
    if bool(crawling) is False:
        result = result[::-periods].iloc[::-1]
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


def _min_sequential(df1, df2):
    """Create merged DataFrame with only rows of minium 'sequential' values.

    Args:
        df1: First DataFrame
        df2: Second DataFrame

    Returns:
        result: DataFrame that matches criteria

    """
    # Merge missing values from on DataFrame into the other.
    # They will both have the same indexes after this operation.
    merged_1 = pd.concat([df1, df2[~df2.index.isin(df1.index)]])
    merged_2 = pd.concat([df2, df1[~df1.index.isin(df2.index)]])

    # Extract the 'sequential' values while maintaining the DataFrame indexes
    s_1 = pd.Series(merged_1['sequential'].tolist(), index=[merged_1.index])
    s_2 = pd.Series(merged_2['sequential'].tolist(), index=[merged_2.index])

    # Create pd.Series of the minimum 'sequential' values in each DataFrame
    escrow = pd.DataFrame(index=s_1.index)
    escrow['s_1'] = s_1
    escrow['s_2'] = s_2
    minima = escrow.min(axis=1)

    # Replace 'sequential' column with minima and return
    merged_1['sequential'] = minima.tolist()
    result = merged_1.copy()
    return result
