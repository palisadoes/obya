"""Utility importation module."""
from collections import namedtuple

# Constants
OBYA_WEBD_NAME = 'obya_webd'
OBYA_WEBD_PROXY = 'obya_wsgid'
FOLDER_WEB_STATIC = 'theme/static'
FOLDER_WEB_TEMPLATE = 'theme/templates'
OBYA_WEB_SITE_PREFIX = '/obya'
OBYA_API_SITE_PREFIX = '{}/api'.format(OBYA_WEB_SITE_PREFIX)

# Named tuples
AgentAPIVariable = namedtuple(
    'AgentAPIVariable', 'ip_bind_port ip_listen_address')

# Class imports
from .configuration import Config
