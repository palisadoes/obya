"""Database setup module."""

# Pip3 libraries
from sqlalchemy import create_engine

# Application libraries
from obya import Config
from obya import log
from obya.db.models import BASE
from obya.db import URL


def setup():
    """Setup server.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    use_mysql = True
    pool_size = 25
    max_overflow = 25

    # Get configuration
    config = Config()

    # Create DB connection pool
    if use_mysql is True:
        # Add MySQL to the pool
        engine = create_engine(
            URL, echo=True,
            encoding='utf8',
            max_overflow=max_overflow,
            pool_size=pool_size, pool_recycle=3600)

        # Try to create the database
        print('Attempting to create database tables')
        try:
            sql_string = ('''\
ALTER DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci\
'''.format(config.db_name()))
            engine.execute(sql_string)
        except:
            log_message = '''\
Cannot connect to database {}. Verify database server is started. Verify \
database is created. Verify that the configured database authentication is \
correct.'''.format(config.db_name())
            log.log2die(1036, log_message)

        # Apply schemas
        print('Applying Schemas')
        BASE.metadata.create_all(engine)
