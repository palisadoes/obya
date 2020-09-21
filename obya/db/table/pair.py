"""Application module to maniupate the Pair database table."""

# Import project libraries
from obya.db import db
from obya.db.models import Pair as _Pair


def pairs():
    """Get list of pairs in table.

    Args:
        None

    Returns:
        result: list of pairs

    """
    # Initialize key variables
    result = []
    rows = []

    # Get name from database
    with db.db_query(1016) as session:
        rows = session.query(_Pair.pair)

    # Return
    for row in rows:
        result.append(row.pair.decode())
    return result


def exists(pair):
    """Determine whether pair exists in the Pair table.

    Args:
        pair: pair name

    Returns:
        result: Pair.idx value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get name from database
    with db.db_query(1005) as session:
        rows = session.query(_Pair.idx).filter(
            _Pair.pair == pair.lower().encode())

    # Return
    for row in rows:
        result = row.idx
        break
    return result


def insert(item):
    """Create a Pair table entry.

    Args:
        item: pair to insert

    Returns:
        None

    """
    # Lowercase the name
    pair = item.strip().lower()

    # Return if exists already
    if bool(exists(pair)) is True:
        return

    # Insert
    row = _Pair(pair=pair.encode())
    with db.db_modify(1002) as session:
        session.add(row)
