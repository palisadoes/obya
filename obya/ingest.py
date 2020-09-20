"""Application ingest module."""

import pandas as pd


def ingest(filepath):
    """Ingest data.

    Args:
        filepath: File path to read

    Returns:
        df_: Dataframe of file data

    """
    # Initialize key variables
    columns = 'day time open high low close volume'
    df_ = pd.read_csv(filepath, names=columns.split())

    # Create the timestamp column
    df_['timestamp'] = pd.to_datetime(
        df_['day'] + ':' + df_['time'],
        format='%Y.%m.%d:%H:%M',
        utc=True
        ).astype('int64')//1e9

    # Drop unwanted columns
    df_ = df_.drop(columns=['time', 'day'])
    return df_


def date(_df):
    """Add date column to DataFrame.

    Args:
        _df: DataFrame to modify

    Returns:
        df_: Dataframe with date column added.

    """
    # Initalize key variables
    df_ = _df.copy()

    # Create the timestamp column
    df_['date'] = pd.to_datetime(df_['timestamp'], unit='s', utc=True)
    return df_
