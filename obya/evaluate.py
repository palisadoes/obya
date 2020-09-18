"""Application evaluation module."""

import ta

from obya.db.table import data


class Evaluate():
    """Class to evaluate dataframe."""

    def __init__(self, _df):
        """Initialize the class.

        Args:
            _df: pd.DataFrame

        Returns:
            None

        """
        # Initalize key variables
        self._df = stoch(_df)

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

    def matches(self, below=10, above=90, difference=1):
        """Create DataFrame that meets evaluation criteria.

        Args:
            below: Below limit
            above: Above limit
            difference: Difference


        Returns:
            result: DataFrame that matches criteria

        """
        # Initialize key variables
        matches_limit = {}

        # Get index values where the Stochastic indicators
        # exceed the desired limits
        for fast in [True, False]:
            for item in self.above(above, fast=fast).index.tolist():
                matches_limit[item] = None
            for item in self.below(below, fast=fast).index.tolist():
                matches_limit[item] = None

        # Get index values where the difference between Stochastic indicators
        # exceed the desired limits
        matches_d = self.difference(difference).index.tolist()

        # Get the indexes with matches in both cases
        indexes = list(
            set(
                list(
                    matches_limit.keys()
                )
            ).intersection(matches_d)
        )
        indexes.sort()

        # Return
        result = self._df[self._df.index.isin(indexes)]
        return result


def evaluate(pair, timeframe):
    """Evaluate data.

    Args:
        pair: Pair to evaluate
        timeframe: Timeframe to evaluate

    Returns:
        None

    """
    # Initialize key variables
    k_period = 35
    d_period = 5
    offset = k_period + d_period

    # Get DataFrame
    df_ = data.dataframe(pair, timeframe)
    result = stoch(df_, k_period=k_period, d_period=d_period)[offset:]
    evaluate_ = Evaluate(result)
    hour4 = evaluate_.matches()

    # Get DataFrame using weekly timeframe (42, 4 hour periods)
    df_ = package(df_, periods=42)
    result = stoch(df_, k_period=k_period, d_period=d_period)[offset:]
    evaluate_ = Evaluate(result)
    hour168 = evaluate_.matches(difference=4)

    # Remove duplicates
    index_4 = hour4.index.tolist()
    index_168 = hour168.index.tolist()
    indexes = tuple(sorted(list(set(index_4).intersection(index_168))))
    result = df_[df_.index.isin(indexes)]
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


def package(_df, periods=5):
    """Convert dataframe to different timeframe.

    Args:
        _df: pd.DataFrame
        periods: Number of periods to include in new timeframe batch

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
