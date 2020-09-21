"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint

# Define the various global variables
OBYA_WEB_STATUS = Blueprint('OBYA_WEB_STATUS', __name__)


@OBYA_WEB_STATUS.route('')
def index():
    """Provide the status page.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    return 'The application is operational.\n'
