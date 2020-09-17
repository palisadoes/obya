"""Application module to maniupate the Pair database table."""

# Import project libraries
from obya.db import db
from obya.db.models import Pair as _Pair


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
    with db.db_query(20031) as session:
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
    with db.db_modify(20052) as session:
        session.add(row)
