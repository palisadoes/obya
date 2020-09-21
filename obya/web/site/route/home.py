"""Application routes - Home Screen."""

# PIP libraries
from flask import Blueprint, render_template, make_response

# Application imports
from obya.web.site.table.home import Home

# Define the various global variables
OBYA_WEB_HOME = Blueprint('OBYA_WEB_HOME', __name__)


@OBYA_WEB_HOME.route('/')
def home():
    """Create home page.

    Args:
        None

    Returns:
        response: HTML

    """
    # Render page
    homepage = Home()
    customer_table = homepage.table()
    response = make_response(
        render_template(
            'index.html',
            customer_table=customer_table)
    )
    return response
