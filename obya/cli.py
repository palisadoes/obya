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

        # Parse "process", return object used for parser
        _setup(subparsers, width=width)

        # Return the CLI arguments
        # args = parser.parse_args()

        # Return our parsed CLI arguments
        return _parser


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
        help=textwrap.fill(
            'Name of file to ingest.', width=width)
    )

    # Process directory flag
    parser.add_argument(
        '--directory',
        type=str,
        help=textwrap.fill(
            'Name of directory with files to ingest.', width=width)
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