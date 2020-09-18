"""Application module to maniupate the Data database table."""

import pandas as pd
from sqlalchemy import and_

# Import project libraries
from obya.db import db
from obya.db.models import Data as _Data
from obya.db.table import pair


def insert(pair_, df_):
    """Create a Data table entries.

    Args:
        pair_: pair
        df_: pd.Dataframe to insert

    Returns:
        None

    """
    # Initialize key variables
    rows = []
    lookups = []
    items = []

    # Get limits of query, convert to integer values as sqlalchemy doesn't
    # like pandas type ints
    timeframe = int(
        (df_['timestamp'][1:] - df_['timestamp'].shift()[1:]).median()
    )
    start = int(df_['timestamp'].min())
    stop = int(df_['timestamp'].max())

    # Get the index for the pair
    idx_pair = pair.exists(pair_)
    if bool(idx_pair) is False:
        pair.insert(pair_)
        idx_pair = pair.exists(pair_)

    # Get name from database
    with db.db_query(20031) as session:
        items = session.query(_Data.timestamp).filter(
            and_(
                _Data.timeframe == timeframe,
                _Data.idx_pair == idx_pair,
                _Data.timestamp >= start,
                _Data.timestamp <= stop
            )
        )

    # Populate lookup list
    for item in items:
        lookups.append(int(item.timestamp))

    # Poplulate data to be inserted into the database
    for _, row in df_.iterrows():
        if int(row['timestamp']) in lookups:
            continue
        rows.append(
            _Data(
                timeframe=timeframe,
                idx_pair=idx_pair,
                timestamp=int(row['timestamp']),
                open=float(row['open']),
                high=float(row['high']),
                low=float(row['low']),
                close=float(row['close']),
                volume=int(row['volume'])
            )
        )

    # Insert
    with db.db_modify(20052) as session:
        session.add_all(rows)


def dataframe(pair_, timeframe):
    """Create a Data table entries.

    Args:
        pair_: pair
        timeframe: Timeframe of data

    Returns:
        df_: pd.Dataframe retrieved

    """
    # Initialize key variables
    rows = []
    columns = 'timestamp open high low close volume'
    df_ = None

    # Get the index for the pair
    idx_pair = pair.exists(pair_)

    # Get name from database
    with db.db_query(20031) as session:
        rows = session.query(
            _Data.timestamp,
            _Data.open,
            _Data.high,
            _Data.low,
            _Data.close,
            _Data.volume,
            ).filter(
                and_(
                    _Data.timeframe == timeframe,
                    _Data.idx_pair == idx_pair
                )
            )

    # Populate lookup list
    if bool(rows) is True:
        df_ = pd.DataFrame(
            [(row.timestamp,
              row.open,
              row.high,
              row.low,
              row.close,
              row.volume
              ) for row in rows],
            columns=columns.split())

    return df_
