#!/usr/bin/python3
"""Toolkit script.

Test

"""
# Standard imports
import os
import sys

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
_EXPECTED = '{0}obya{0}bin'.format(os.sep)
if _BIN_DIRECTORY.endswith(_EXPECTED) is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


# Import application libraries
from obya import cli
from obya import ingest
from obya import evaluate
from obya.db import setup
from obya.db.table import data


def main():
    """Format Nagios host configuration.

    Args:
        None

    Returns:
        None

    """
    # Process the CLI
    parse = cli.Parser()
    parser = parse.parser()
    args = parser.parse_args()

    # Ingest data
    if args.mode == 'ingest':
        df_ = ingest.ingest(args.filename)
        data.insert(args.pair, df_)
        sys.exit()

    # Setup database
    if args.mode == 'setup':
        setup.setup()
        sys.exit()

    # Evaluate data
    if args.mode == 'evaluate':
        evaluate.evaluate(args.pair, args.timeframe)
        sys.exit()

    # Exit
    parser.print_help()


if __name__ == '__main__':
    main()
