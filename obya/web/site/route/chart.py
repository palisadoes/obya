"""Application routes - Charts."""

# PIP libraries
from flask import Blueprint, render_template, request, jsonify, abort, make_response
import requests

# Application imports
from obya.web.site.table.chart.stoch import Stoch

# Define the various global variables
OBYA_WEB_CHART = Blueprint('OBYA_WEB_CHART', __name__)


@OBYA_WEB_CHART.route('/stoch/<pair_>')
def stoch(pair_):
    """Provide data from the Data table.

    Args:
        pair_: Currency pair

    Returns:
        None

    """
    # Return
    pair = pair_.upper()
    timeframe = 14400

    slow = Stoch(pair, timeframe, periods=28)
    slow_table = slow.table()

    fast = Stoch(pair, timeframe, periods=None)
    fast_table = fast.table()

    # Show bandwidth charts only if the customer has allocated bandwidth
    response = make_response(
        render_template(
            'stoch.html',
            pair=pair,
            slow_table=slow_table,
            fast_table=fast_table)
    )
    return response
