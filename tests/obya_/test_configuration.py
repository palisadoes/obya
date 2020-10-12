#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}obya{0}tests{0}obya_'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Application imports
from tests.libraries.configuration import UnittestConfig
from obya import configuration


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test__config_reader(self):
        """Testing function _config_reader."""
        pass


class TestConfig(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = configuration.Config()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_api_hostname(self):
        """Testing function api_hostname."""
        # Test
        self.assertEqual(self.config.api_hostname, 'rkpQ9hKWS7U7Pv5X')

    def test_api_key(self):
        """Testing function api_key."""
        # Test
        self.assertEqual(self.config.api_key, 'fxck5rT2aqa3SLTv')

    def test_api_password(self):
        """Testing function api_password."""
        # Test
        self.assertEqual(self.config.api_password, '73QRBH4y4VdXZyF7')

    def test_api_username(self):
        """Testing function api_username."""
        # Test
        self.assertEqual(self.config.api_username, 'c4FwmcXmH2ZnQMng')

    def test_db_name(self):
        """Testing function db_name."""
        # Test
        self.assertEqual(self.config.db_name, 'obya_unittest')

    def test_db_username(self):
        """Testing function db_username."""
        # Test
        self.assertEqual(self.config.db_username, 'travis')

    def test_db_password(self):
        """Testing function db_password."""
        # Test
        self.assertEqual(self.config.db_password, 'fKjafGGQqw89CtbS')

    def test_db_hostname(self):
        """Testing function db_hostname."""
        # Test
        self.assertEqual(self.config.db_hostname, 'localhost')

    def test_db_pool_size(self):
        """Testing function db_pool_size."""
        # Test
        self.assertEqual(self.config.db_pool_size, 10)

    def test_db_max_overflow(self):
        """Testing function db_max_overflow."""
        # Test
        self.assertEqual(self.config.db_max_overflow, 10)

    def test_email_from(self):
        """Testing function email_from."""
        # Test
        self.assertEqual(self.config.email_from, 'noreply@example.org')

    def test_email_to(self):
        """Testing function email_to."""
        # Test
        self.assertEqual(self.config.email_to, ['test@example.org'])

    def test_pairs(self):
        """Testing function pairs."""
        # Test
        self.assertEqual(
            self.config.pairs,
            [
                'AUDCAD', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADJPY', 'EURAUD',
                'EURCAD', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD',
                'GBPCAD', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDJPY', 'NZDUSD',
                'USDCAD', 'USDJPY', 'GBPJPY'
            ]
        )

    def test_smtp_pass(self):
        """Testing function smtp_pass."""
        # Test
        self.assertEqual(self.config.smtp_pass, 'YsaaHsQzruHwT5V5')

    def test_smtp_user(self):
        """Testing function smtp_user."""
        # Test
        self.assertEqual(self.config.smtp_user, 'obya')

    def test_log_directory(self):
        """Testing function log_directory."""
        pass

    def test_log_file(self):
        """Testing function log_file."""
        pass

    def test_log_level(self):
        """Testing function log_level."""
        # Test
        self.assertEqual(self.config.log_level, 'debug')


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
