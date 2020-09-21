#!usr/bin/env python3
"""Class for creating customer web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import application libraries
from obya.url import api


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class Stoch():
    """Class that creates the Customer's various HTML tables."""

    def __init__(self, pair, timeframe):
        """Initialize the class.

        Args:
            pair: Currency pair
            timeframe: Timeframe

        Returns:
            None

        """
        # Get cabinet ID data for customer
        self._data = _data(pair, timeframe)

    def table(self):
        """Create the cabinets table for the customer.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        if bool(self._data) is True:
            table = _Table(self._data)
            html = table.__html__()
        else:
            html = ''

        # Return
        return html


class _Table(Table):
    """Declaration of the columns in the Cabinet table."""

    # Initialize class variables
    chart = _RawCol('Chart')

    # Define the CSS class to use for the header row
    classes = ['table']


class _Row():
    """Declaration of the rows in the Cabinet table."""

    def __init__(
            self, chart):
        """Initialize the class.

        Args:
            metadata: Timeframe metadata
            chart: Chart HTML

        Returns:
            None

        """
        # Initialize key variables
        self.chart = chart


def _data(pair, timeframe):
    """Return whether port is enabled.

    Args:
        pair: Currency pair
        timeframe: Timeframe

    Returns:
        rows: List of Col objects

    """
    # Initialize key variables
    rows = []
    y_axis = 'Percent'
    url = api.stoch(pair)

    # Create subheadings
    h1_ = pair.upper()
    h2_ = 'Stochastic Oscillator'
    h3_ = timeframe

    # Assign variables.
    div_id = '{}_stoch_{}'.format(h1_, h3_)
    chart_html = ("""\
<div id="{0}"></div>
<script type="text/javascript">
drawChartBasic('{1}', '#{0}', '{2}', '{3}', '{4}', '{5}');
</script>\
""").format(div_id, url, h1_, h2_, h3_, y_axis)

    # Append row of data
    rows.append(_Row(chart_html))

    # Return
    return rows
