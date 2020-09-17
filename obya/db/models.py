"""Application ORM Table classes.

Used to define the tables used in the database.

"""

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import (
    BIGINT, DATETIME, VARBINARY, FLOAT, INTEGER)
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from obya.db import POOL

###############################################################################
# Create Base SQLAlchemy class. This must be in the same file as the database
# definitions or else the database won't be created on install. Learned via
# trial and error.
BASE = declarative_base()

# GraphQL: Bind engine to metadata of the base class
BASE.metadata.bind = POOL

# GraphQL: Used by graphql to execute queries
BASE.query = POOL.query_property()
###############################################################################


class Pair(BASE):
    """Class defining the ob_pair table of the database."""

    __tablename__ = 'ob_pair'
    __table_args__ = (
        UniqueConstraint(
            'pair'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    pair = Column(VARBINARY(512), nullable=True, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Data(BASE):
    """Class defining the ob_data table of the database."""

    __tablename__ = 'ob_data'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_pair', 'timestamp', 'timeframe'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_pair = Column(
        BIGINT(unsigned=True),
        ForeignKey('ob_pair.idx'),
        nullable=False,
        server_default='1')

    timeframe = Column(INTEGER, index=True, nullable=False, default=None)

    open = Column(FLOAT, nullable=False, default=None)

    high = Column(FLOAT, nullable=False, default=None)

    low = Column(FLOAT, nullable=False, default=None)

    close = Column(FLOAT, nullable=False, default=None)

    volume = Column(FLOAT, nullable=False, default=None)

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a row
    # to rows in the tables used by foreign keys
    pair = relationship(
        Pair,
        backref=backref(
            'data_pair', uselist=True, cascade='delete,all'))
