"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, render_template

# Application imports
# from pattoo_web.web.tables import home

# Define the various global variables
OBYA_WEB_HOME = Blueprint('OBYA_WEB_HOME', __name__)


@OBYA_WEB_HOME.route('/')
def route_data():
    """Provide data from the Data table.

    Args:
        None

    Returns:
        None

    """
    # Return
    return 'Home page.\n'

    # Process the data
    # if _agents.valid is True:
    #     # Render data from database
    #     table = home.table(_agents)
    #     return render_template('home.html', main_table=table)
    #
    # # No database
    # return render_template('no-api.html')
