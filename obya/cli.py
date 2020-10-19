"""Application CLI module."""

import textwrap
import argparse
import sys

# Import custom libraries
from obya import log


class Parser(object):
    """Class gathers all CLI information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        get_cli:
    """

    def __init__(self, additional_help=None):
        """Function for intializing the class."""
        # Create a number of here-doc entries
        if additional_help is not None:
            self.config_help = additional_help
        else:
            self.config_help = ''

        # Default days
        self._default_days = 365

    def parser(self):
        """Return all the CLI options.

        Args:
            self:

        Returns:
            args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        # Initialize key variables
        width = 80

        # Log the cli command
        log_message = 'CLI: {}'.format(' '.join(sys.argv))
        log.log2debug(1000, log_message)

        # Header for the help menu of the application
        _parser = argparse.ArgumentParser(
            description=self.config_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = _parser.add_subparsers(dest='mode')

        # Parse "ingest", return object used for parser
        _ingest(subparsers, width=width)

        # Parse "setup", return object used for parser
        _setup(subparsers, width=width)

        # Parse "evaluate", return object used for parser
        _evaluate(subparsers, width=width, days=self._default_days)

        # Parse "email", return object used for parser
        _email(subparsers, width=width, days=self._default_days)

        # Parse "api", return object used for parser
        _api(subparsers, width=width, days=(self._default_days * 2))

        # Return our parsed CLI arguments
        return _parser


def _api(subparsers, width=80, days=365):
    """Process "api" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping
        days: Days of data to process

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'api',
        help=textwrap.fill(
            'Connect to the obya data source API.', width=width)
    )

    # Process days flag
    parser.add_argument(
        '--days',
        type=int,
        required=False,
        default=days,
        help=textwrap.fill(
            'Number of days to use for backfill. Default: {}'.format(days),
            width=width)
    )

    # Process verbose flag
    parser.add_argument(
        '--verbose',
        help='Verbose progress reporting.',
        action='store_true')


def _email(subparsers, width=80, days=365):
    """Process "email" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping
        days: Days of data to process

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'email',
        help=textwrap.fill(
            'Evaluate FX data in database.', width=width)
    )

    # Process timeframe flag
    parser.add_argument(
        '--timeframe',
        type=int,
        required=True,
        help=textwrap.fill(
            'Timeframe to email.', width=width)
    )

    # Process days flag
    parser.add_argument(
        '--days',
        type=int,
        default=days,
        help=textwrap.fill('''\
Number of days to include in the report. Data is always processed from the \
first day of available data. Default: {}'''.format(days), width=width)
    )


def _evaluate(subparsers, width=80, days=365):
    """Process "evaluate" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping
        days: Days of data to process

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'evaluate',
        help=textwrap.fill(
            'Evaluate FX data in database.', width=width)
    )

    # Process pair flag
    parser.add_argument(
        '--pair',
        type=str,
        required=True,
        help=textwrap.fill(
            'Pair to evaluate.', width=width)
    )

    # Process timeframe flag
    parser.add_argument(
        '--timeframe',
        type=int,
        required=True,
        help=textwrap.fill(
            'Timeframe to evaluate.', width=width)
    )

    # Process days flag
    parser.add_argument(
        '--days',
        type=int,
        default=days,
        help=textwrap.fill('''\
Number of days to include in the report. Data is always processed from the \
first day of available data. Default: {}'''.format(days), width=width)
    )


def _ingest(subparsers, width=80):
    """Process "ingest" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'ingest',
        help=textwrap.fill(
            'ingest FX data from file.', width=width)
    )

    # Process filename flag
    parser.add_argument(
        '--filename',
        type=str,
        required=True,
        help=textwrap.fill(
            'Name of file to ingest.', width=width)
    )

    # Process pair flag
    parser.add_argument(
        '--pair',
        type=str,
        required=True,
        help=textwrap.fill(
            'Pair to ingest.', width=width)
    )


def _setup(subparsers, width=80):
    """Process "setup" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping

    Returns:
        None

    """
    # Initialize key variables
    _ = subparsers.add_parser(
        'setup',
        help=textwrap.fill('Setup the database.', width=width)
    )
