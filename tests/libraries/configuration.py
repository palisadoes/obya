"""Module to create configuration for unittesting.

NOTE!! This script CANNOT import any obya libraries. Doing so risks
libraries trying to access a configuration or configuration directory that
doesn't yet exist. This is especially important when running cloud based
automated tests such as 'Travis CI'.

"""

# Standard imports
from __future__ import print_function
import tempfile
import os
import yaml

# Pattoo imports
from obya import log


class UnittestConfig():
    """Creates configuration for testing."""

    def __init__(self):
        """Initialize the class."""
        # Initialize GLOBAL variables
        self._config_directory = (
            '{}{}.obya-unittests'.format(os.environ['HOME'], os.sep))

        # Make sure the environmental variables are OK
        _environment(self._config_directory)

        # Set global variables
        self._log_directory = tempfile.mkdtemp()

        # Make sure the configuration directory is OK
        if os.path.isdir(self._config_directory) is False:
            os.makedirs(self._config_directory, mode=0o750, exist_ok=True)

        self._config = {
            'obya': {
                'log_directory': self._log_directory,
                'log_level': 'debug',
                'db_hostname': 'localhost',
                'db_username': 'travis',
                'db_password': 'fKjafGGQqw89CtbS',
                'db_name': 'obya_unittest'
            },
        }

    def create(self):
        """Create a good config and set the OBYA_CONFIGDIR variable.

        Args:
            None

        Returns:
            self.config_directory: Directory where the config is placed

        """
        # Delete any existing configuration files to make a clean start
        _delete_files(self._config_directory, delete_directory=False)

        # Initialize filenames and their contents
        data_ = {
            '{}{}obya.yaml'.format(
                self._config_directory, os.sep): self._config,
        }

        # Write configurations
        for filename, contents in data_.items():
            # Write to obya.yaml
            try:
                f_handle = open(filename, 'w')
            except PermissionError:
                log.log2die(1010, '''\
Insufficient permissions for creating the file:{}'''.format(f_handle))
            else:
                with f_handle:
                    yaml.dump(contents, f_handle, default_flow_style=False)

        # Return
        return self._config_directory

    def cleanup(self):
        """Remove all residual directories.

        Args:
            None

        Returns:
            None

        """
        # Delete directories
        directories = [
            self._log_directory,
            self._config_directory]
        for directory in directories:
            _delete_files(directory)


def _delete_files(directory, delete_directory=True):
    """Delete all files in directory."""
    # Cleanup files in temp directories
    filenames = [filename for filename in os.listdir(
        directory) if os.path.isfile(
            os.path.join(directory, filename))]

    # Get the full filepath for the cache file and remove filepath
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        os.remove(filepath)

    # Remove directory after files are deleted.
    if bool(delete_directory) is True:
        os.rmdir(directory)


def _environment(config_directory):
    """Make sure environmental variables are OK.

    Args:
        config_directory: Directory with the configuration

    Returns:
        None

    """
    # Create a message for the screen
    screen_message = ('''
The OBYA_CONFIGDIR is set to the wrong directory. Run this command to do \
so:

$ export OBYA_CONFIGDIR={}

Then run this command again.
'''.format(config_directory))

    # Make sure the OBYA_CONFIGDIR environment variable is set
    if 'OBYA_CONFIGDIR' not in os.environ:
        log.log2die_safe(1011, screen_message)

    # Make sure the OBYA_CONFIGDIR environment variable is set correctly
    if os.environ['OBYA_CONFIGDIR'] != config_directory:
        log.log2die_safe(1009, screen_message)

    # Update message
    screen_message = ('''{}

OBYA_CONFIGDIR is incorrectly set to {}

'''.format(screen_message, os.environ['OBYA_CONFIGDIR']))

    # Make sure the OBYA_CONFIGDIR environment variable is set to unittest
    if 'unittest' not in os.environ['OBYA_CONFIGDIR']:
        log_message = (
            'The OBYA_CONFIGDIR is not set to a unittest directory')
        log.log2die_safe(1008, log_message)
