#!/usr/bin/python3
"""Toolkit script.

Test

"""
# Standard imports
import os
import sys
import time
from datetime import datetime

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
from obya import evaluate
from obya import reports
from obya import email
from obya.db import setup
from obya.db.table import data
from obya.db.table import pair
from obya.ingest import files
from obya.ingest import api


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
    report = ''

    # Get data from API data source
    if args.mode == 'api':
        secondsago = args.days * 86400
        api.ingest(secondsago, verbose=args.verbose)
        sys.exit()

    # Ingest data
    if args.mode == 'ingest':
        df_ = files.ingest(args.filename)
        data.insert(args.pair, df_)
        sys.exit()

    # Setup database
    if args.mode == 'setup':
        setup.setup()
        sys.exit()

    # Evaluate data
    if args.mode == 'evaluate':
        if bool(args.pair) is True:
            report = reports.report(args.pair, args.timeframe, days=args.days)
        else:
            report = reports.reports(args.timeframe, days=args.days)
        print(report)
        sys.exit()

    # Email data
    if args.mode == 'email':
        report = reports.reports(args.timeframe, days=args.days)
        now = int(time.time())
        subject = 'Obya FX Report - {}'.format(
            datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M'))
        email.send(report, subject)
        sys.exit()

    # Exit
    parser.print_help()


if __name__ == '__main__':
    main()
