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
        format='%Y.%m.%d:%H:%M'
        ).astype('int64')//1e9

    # Drop unwanted columns
    df_ = df_.drop(columns=['time', 'day'])
    return df_
