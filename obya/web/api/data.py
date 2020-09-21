"""Application routes - API data."""

# PIP libraries
from flask import Blueprint, render_template, request, jsonify, abort, make_response
import requests

# Application imports
from obya.db.table import data
from obya import evaluate

# Define the various global variables
OBYA_API = Blueprint('OBYA_API', __name__)


@OBYA_API.route('/stoch/<pair_>')
def stoch(pair_):
    """Provide data from the Data table.

    Args:
        pair_: Currency pair

    Returns:
        None

    """
    # Return
    pair = pair_.lower()
    timeframe = 14400
    results = []
    rounding = 2

    # Get data
    df_ = data.dataframe(pair, timeframe)
    if df_.empty is False:
        result_ = evaluate.evaluate(df_, 29)
        k_values = result_['k_l'].values.tolist()
        d_values = result_['d_l'].values.tolist()
        timestamps = result_['timestamp'].values.tolist()
        for pointer, timestamp in enumerate(timestamps):
            results.append(
                {
                    'k': round(k_values[pointer], rounding),
                    'd': round(d_values[pointer], rounding),
                    'date': timestamp
                }
            )
    return jsonify(results)