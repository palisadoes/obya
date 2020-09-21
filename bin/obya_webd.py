#!/usr/bin/env python3
"""Web application WSGI script.

Serves as a Gunicorn WSGI entry point for the application

"""

# Standard libraries
import sys
import os

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
_EXPECTED = '{0}obya{0}bin'.format(os.sep)
if _BIN_DIRECTORY.endswith(_EXPECTED) is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Application libraries
from obya import log
from obya.daemon.agent import Agent, AgentCLI, AgentAPI
from obya import Config
from obya import OBYA_WEBD_NAME, OBYA_WEBD_PROXY
from obya.web.site import OBYA_WEBD


def main():
    """Start the Gunicorn WSGI."""
    # Initialize key variables
    config = Config()

    # Get PID filenename for Gunicorn
    agent_gunicorn = Agent(OBYA_WEBD_PROXY, config=config)

    # Get configuration
    agent_api = AgentAPI(
        OBYA_WEBD_NAME, OBYA_WEBD_PROXY, OBYA_WEBD, config=config)

    # Do control (API first, Gunicorn second)
    cli = AgentCLI()
    cli.control(agent_api)
    cli.control(agent_gunicorn)


if __name__ == '__main__':
    log.env()
    main()
