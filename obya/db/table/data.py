"""Application module to maniupate the Data database table."""

from sqlalchemy import and_
from pprint import pprint
import sys

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

    # Update the data
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
