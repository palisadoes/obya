"""Application evaluation module."""

import ta

from obya.db.table import data


def evaluate(pair, timeframe):
    """Evaluate data.

    Args:
        pair: Pair to evaluate
        timeframe: Timeframe to evaluate

    Returns:
        None

    """
    df_ = data.dataframe(pair, timeframe)
    stoch(df_)
    package(df_)


def stoch(_df, k_period=35, d_period=5):
    """Add stochastic indicators to pd.DataFrame.

    Args:
        _df: pd.DataFrame
        k_period: Periods for calculating Stochastic slow indicator
        d_period: Moving Average periods for smoothing Stochastic to create
            the fast indicator

    Returns:
        df_: Modified DataFrame

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
    print(df_)
    return df_


def package(_df, offset=5):
    """Add stochastic indicators to pd.DataFrame.

    Args:
        _df: pd.DataFrame
        offset: Offset

    Returns:
        df_: Modified DataFrame

    """
    # Initialize key variables
    df_ = _df.copy()

    df_['low'] = df_['low'].rolling(offset).min()
    df_['high'] = df_['high'].rolling(offset).max()
    df_['volume'] = df_['volume'].rolling(offset).sum()
    df_['open'] = df_['open'].shift(offset - 1)
    # df_['close'] = df_['close'].shift(offset - 1)
    print(df_)
    return df_
