"""Initialize the OBYA_WEBD module."""

# Import PIP3 libraries
from flask import Flask, url_for

# Define the global URL prefix
from obya import (
    OBYA_WEB_SITE_PREFIX, OBYA_API_SITE_PREFIX, FOLDER_WEB_STATIC,
    FOLDER_WEB_TEMPLATE)

# Import OBYA_WEBD Blueprints
from obya.web.site.route.home import OBYA_WEB_HOME
from obya.web.site.route.chart import OBYA_WEB_CHART
from obya.web.site.route.status import OBYA_WEB_STATUS
from obya.web.api.data import OBYA_API

# Setup flask
OBYA_WEBD = Flask(
    __name__,
    static_url_path='{}/static'.format(OBYA_WEB_SITE_PREFIX),
    static_folder=FOLDER_WEB_STATIC,
    template_folder=FOLDER_WEB_TEMPLATE
)

# Register Blueprints
OBYA_WEBD.register_blueprint(
    OBYA_WEB_HOME, url_prefix=OBYA_WEB_SITE_PREFIX)
OBYA_WEBD.register_blueprint(
    OBYA_WEB_CHART, url_prefix='{}/chart'.format(OBYA_WEB_SITE_PREFIX))
OBYA_WEBD.register_blueprint(
    OBYA_WEB_STATUS, url_prefix='{}/status'.format(OBYA_WEB_SITE_PREFIX))

# Register API Blueprints
OBYA_WEBD.register_blueprint(
    OBYA_API, url_prefix='{}'.format(OBYA_API_SITE_PREFIX))


# Function to easily find your assests
OBYA_WEBD.jinja_env.globals['static'] = (
    lambda filename: url_for(
        'static', filename=filename)
)


@OBYA_WEBD.context_processor
def inject():
    """Inject global variables for use by templates.

    Args:
        None

    Returns:
        HTML

    """
    # Return
    return dict(
        url_home=OBYA_WEB_SITE_PREFIX,
        url_static='{}/static'.format(OBYA_WEB_SITE_PREFIX))
