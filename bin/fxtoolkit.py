#!/usr/bin/python3
"""Toolkit script.

Test

"""
# Standard imports
import os
import sys
from datetime import timezone
import datetime

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
from obya import formatter
from obya.db import setup
from obya.db.table import data
from obya.db.table import pair


def main():
    """Main function.

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
        print(_report(args.pair, args.timeframe, days=args.days))
        sys.exit()

    # Email data
    if args.mode == 'email':
        pairs = pair.pairs()
        for pair_ in pairs:
            print(_report(pair_, args.timeframe, days=args.days))
        sys.exit()

    # Exit
    parser.print_help()


def _report(_pair, timeframe, days=None):
    """Create reports.

    Args:
        _pair: Pair to Evaluate
        timeframe: Timeframe
        days: Age of report in days

    Returns:
        result: String report

    """
    # Initialize key variables
    if bool(days) is False:
        secondsago = 365 * 24 * 3600
    else:
        secondsago = 365 * days * 3600
    result = ''

    # Process data
    df_ = data.dataframe(_pair, timeframe, secondsago=secondsago)
    if df_.empty is False:
        result_ = evaluate.evaluate(df_, 29)

        # Drop all rows that are older than days
        result_ = evaluate.recent(result_, secondsago=secondsago)

        # Create report
        if result_.empty is False:
            result = formatter.email(result_)
    return result


if __name__ == '__main__':
    main()
