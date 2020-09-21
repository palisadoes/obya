#!usr/bin/env python3
"""Class for creating home web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import application.libraries
from obya.db.table import pair
from obya.url import chart


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class Home():
    """Class that creates the homepages's various HTML tables."""

    def __init__(self):
        """Initialize the class."""

    def table(self):
        """Create data table for the devices.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Populate the table
        table = _Table(_rows())

        # Get HTML
        html = table.__html__()

        # Return
        return html


class _Table(Table):
    """Declaration of the columns in the Customers table."""

    # Initialize class variables
    col0 = _RawCol('')
    col1 = _RawCol('')
    col2 = _RawCol('')
    col3 = _RawCol('')

    # Define the CSS class to use for the header row
    classes = ['table']

    def thead(self):
        """Turn off the header row.

        Args:
            None

        Returns:
            html:

        """
        # Initialize key variables
        html = ''
        return html


class _Row():
    """Declaration of the rows in the Customers table."""

    def __init__(self, row_data):
        """Initialize the class.

        Args:
            row_data: Row data

        Returns:
            None

        """
        # Initialize key variables
        self.col0 = row_data[0]
        self.col1 = row_data[1]
        self.col2 = row_data[2]
        self.col3 = row_data[3]


def _rows():
    """Return data for the device's system information.

    Args:
        None

    Returns:
        rows: List of Col objects

    """
    # Initialize key variables
    rows = []
    links = []
    column = 0
    max_columns = 3
    pairs = pair.pairs()

    # Create list of links for table
    for pair_ in pairs:
        link = '<a href="{}">{}</a>'.format(chart.stoch(pair_), pair_.upper())
        links.append(link)

    # Add links to table rows
    row_data = [''] * (max_columns + 1)
    for index, link in enumerate(links):
        row_data[column] = links[index]

        # Create new row when max number of columns reached
        column += 1
        if column > max_columns:
            rows.append(_Row(row_data))
            row_data = [''] * (max_columns + 1)
            column = 0

    # Append a row if max number of columns wasn't reached before
    if 0 < column <= max_columns:
        rows.append(_Row(row_data))

    # Return
    return rows
