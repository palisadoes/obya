"""Database connection module."""
from contextlib import contextmanager

# Application libraries
from obya import log
from obya.db import POOL


@contextmanager
def db_modify(error_code, die=True, close=True):
    """Provide a transactional scope around Update / Insert operations.

    From https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Args:
        error_code: Error code to use in messages
        die: Die if True
        close: Close session if True. GraphQL mutations sometimes require the
            session to remain open.

    Returns:
        None

    """
    # Initialize key variables
    prefix = 'Unable to modify database.'

    # Create session from pool
    session = POOL()

    # Setup basic functions
    try:
        yield session
        session.commit()
    except Exception as exception_error:
        session.rollback()
        log_message = '{}. Error: "{}"'.format(prefix, exception_error)
        if bool(die) is True:
            log.log2die(error_code, log_message)
        else:
            log.log2info(error_code, log_message)
    except:
        session.rollback()
        log_message = '{}. Unknown error'.format(prefix)
        if bool(die) is True:
            log.log2die(error_code, log_message)
        else:
            log.log2info(error_code, log_message)
    finally:
        # Return the Connection to the pool
        if bool(close) is True:
            session.close()


@contextmanager
def db_query(error_code, close=True):
    """Provide a transactional scope around Query operations.

    From https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Args:
        error_code: Error code to use in messages
        close: Close session if True. GraphQL mutations sometimes require the
            session to remain open.
    Returns:
        None

    """
    # Initialize key variables
    prefix = 'Unable to read database.'

    # Create session from pool
    session = POOL()

    # Setup basic functions
    try:
        yield session
    except Exception as exception_error:
        session.close()
        log_message = '{}. Error: "{}"'.format(prefix, exception_error)
        log.log2info(error_code, log_message)
    except:
        session.close()
        log_message = '{}. Unknown error'.format(prefix)
        log.log2info(error_code, log_message)
    finally:
        # Return the Connection to the pool
        if bool(close) is True:
            session.close()
