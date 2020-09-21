"""Pattoo version routes."""

# Standard imports
import sys

# PIP libraries
from flask import Blueprint, render_template, request, jsonify, abort
import requests

# Define the various global variables
OBYA_WEB_CHART = Blueprint('OBYA_WEB_CHART', __name__)


@OBYA_WEB_CHART.route('/datapoint/<identifier>')
def route_chart(identifier):
    """Provide data from the Data table.

    Args:
        identifier: GraphQL identifier for the datapoint

    Returns:
        None

    """
    # Return
    return 'Chart page.\n'
    #
    # # Get heading for DataPoint
    # secondsago = uri.integerize_arg(request.args.get('secondsago'))
    #
    # # Get data from API server
    # point = datapoint(identifier)
    #
    # if point.valid is True:
    #     # Get translations from API server
    #     key_pair_translator = translation(point.id_pair_xlate_group())
    #     point_xlate = datapoint_translations(point, key_pair_translator)
    #
    #     # Get table to present
    #     table = chart.Table(point_xlate, secondsago)
    #     html = table.html()
    #
    #     return render_template(
    #         'chart.html',
    #         main_table=html,
    #         target=point.agent_polled_target())
    #
    # # Otherwise abort
    # abort(404)
