"""Obya classes that manage various configurations."""

# Standard imports
import os
import yaml

# Import project libraries
from obya import log


def _config_reader(filename):
    """Read a configuration file.

    Args:
        filename: Name of file to read

    Returns:
        config_dict: Dict representation of YAML in the file

    """
    # Get the configuration directory
    # Expand linux ~ notation for home directories if provided.
    directory = os.path.expanduser(log.check_environment())
    filepath = '{}{}{}'.format(directory, os.sep, filename)
    with open(filepath, 'r') as file_handle:
        yaml_from_file = file_handle.read()
    config_dict = yaml.safe_load(yaml_from_file)
    return config_dict


class Config():
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Read data
        self._base_yaml_configuration = _config_reader('obya.yaml')

    def config_directory(self):
        """Get config_directory.

        Args:
            None

        Returns:
            result: result

        """
        # Return
        result = log.check_environment()
        return result

    def log_directory(self):
        """Get log_directory.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        _result = self._base_yaml_configuration.get('log_directory')

        # Expand linux ~ notation for home directories if provided.
        result = os.path.expanduser(_result)

        # Check if value exists. We cannot use log2die_safe as it does not
        # require a log directory location to work properly
        if os.path.isdir(result) is False:
            log_message = (
                'log_directory: "{}" '
                'in configuration doesn\'t exist!'.format(result))
            log.log2die_safe(1003, log_message)

        # Return
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        _log_directory = self.log_directory()
        result = '{}{}obya.log'.format(_log_directory, os.sep)
        return result

    def log_level(self):
        """Get log_level.

        Args:
            None

        Returns:
            result: result

        """
        # Return
        _result = self._base_yaml_configuration.get('log_level', 'debug')
        result = '{}'.format(_result).lower()
        return result

    def db_name(self):
        """Get db_name.

        Args:
            None

        Returns:
            result: result

        """
        # Process configuration
        result = self._base_yaml_configuration.get('db_name', 'obya')
        return result

    def db_username(self):
        """Get db_username.

        Args:
            None

        Returns:
            result: result

        """
        # Process configuration
        result = self._base_yaml_configuration.get('db_username', 'obya')
        return result

    def db_password(self):
        """Get db_password.

        Args:
            None

        Returns:
            result: result

        """
        # Process configuration
        result = self._base_yaml_configuration.get('db_password')
        return result

    def db_hostname(self):
        """Get db_hostname.

        Args:
            None

        Returns:
            result: result

        """
        # Process configuration
        result = self._base_yaml_configuration.get('db_hostname', 'localhost')
        return result

    def db_pool_size(self):
        """Get db_pool_size.

        Args:
            None

        Returns:
            result: result

        """
        # Process configuration
        result = self._base_yaml_configuration.get('db_pool_size', 10)
        return result

    def db_max_overflow(self):
        """Get db_max_overflow.

        Args:
            None

        Returns:
            result: result

        """
        # Process configuration
        result = self._base_yaml_configuration.get('db_max_overflow', 10)
        return result
