"""Generic linux daemon base class for python 3.x."""

from __future__ import print_function
import atexit
import signal
import sys
import os
import time

# Application imports
from obya import log


class Daemon():
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.

    Modified from http://www.jejik.com/files/examples/daemon3x.py

    """

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: Agent object

        Returns:
            None

        """
        self.name = agent.name()
        self.pidfile = agent.pidfile_parent
        self.lockfile = agent.lockfile_parent
        self._config = agent.config

    def _daemonize(self):
        """Deamonize class. UNIX double fork mechanism.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        daemon_log_file = self._config.log_file_daemon

        # Make sure that the log file is accessible.
        try:
            open(daemon_log_file, 'a').close()
        except:
            log_message = '''Cannot access daemon log file {}. Please check \
file and directory permissions.'''.format(daemon_log_file)
            log.log2die(1054, log_message)

        # Create a parent process that will manage the child
        # when the code using this class is done.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            log_message = 'Daemon fork #1 failed: {}'.format(err)
            log_message = '{} - PID file: {}'.format(log_message, self.pidfile)
            log.log2die(1067, log_message)

        # Decouple from parent environment
        os.chdir('{}'.format(os.sep))
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            log_message = 'Daemon fork #2 failed: {}'.format(err)
            log_message = '{} - PID file: {}'.format(log_message, self.pidfile)
            log.log2die(1072, log_message)

        # Redirect standard file descriptors, but first make sure that the
        sys.stdout.flush()
        sys.stderr.flush()
        f_handle_si = open(os.devnull, 'r')
        f_handle_so = open(daemon_log_file, 'a+')
        f_handle_se = open(daemon_log_file, 'a+')
        os.dup2(f_handle_si.fileno(), sys.stdin.fileno())
        os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f_handle:
            f_handle.write('{}\n'.format(pid))

    def delpid(self):
        """Delete the PID file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if os.path.exists(self.pidfile) is True:
            try:
                os.remove(self.pidfile)
            except:
                log_message = (
                    'PID file {} already deleted'.format(self.pidfile))
                log.log2warning(1041, log_message)

    def dellock(self):
        """Delete the lock file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if self.lockfile is not None:
            if os.path.exists(self.lockfile) is True:
                os.remove(self.lockfile)

    def start(self):
        """Start the daemon.

        Args:
            None

        Returns:
            None

        """
        # Check for a pidfile to see if the daemon already runs
        pid = _pid(self.pidfile)

        # Die if already running
        if bool(pid) is True:
            log_message = (
                'PID file: {} already exists. Daemon already running?'
                ''.format(self.pidfile))
            log.log2die(1073, log_message)

        # Start the daemon
        self._daemonize()

        # Log success
        log_message = (
            'Daemon {} started - PID file: {}'
            ''.format(self.name, self.pidfile))
        log.log2info(1070, log_message)

        # Run code for daemon
        self.run()

    def force(self):
        """Stop the daemon by deleting the lock file first.

        Args:
            None

        Returns:
            None

        """
        # Delete lock file and stop
        self.dellock()
        self.stop()

    def stop(self):
        """Stop the daemon.

        Args:
            None

        Returns:
            None

        """
        # Check for a pidfile to see if the daemon already runs
        pid = _pid(self.pidfile)
        if bool(pid) is False:
            log_message = (
                'PID file: {} does not exist. Daemon not running?'
                ''.format(self.pidfile))
            log.log2warning(1063, log_message)
            # Not an error in a restart
            return

        # Try killing the daemon process
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as err:
            error = str(err.args)
            if error.find('No such process') > 0:
                self.delpid()
                self.dellock()
            else:
                log_message = (str(err.args))
                log_message = (
                    '{} - PID file: {}'.format(log_message, self.pidfile))
                log.log2die(1068, log_message)
        except:
            log_message = (
                'Unknown daemon "stopped" error for PID file: {}'
                ''.format(self.pidfile))
            log.log2die(1066, log_message)

        # Log success
        self.delpid()
        self.dellock()
        log_message = (
            'Daemon {} stopped - PID file: {}'
            ''.format(self.name, self.pidfile))
        log.log2info(1071, log_message)

    def restart(self):
        """Restart the daemon.

        Args:
            None

        Returns:
            None

        """
        # Restart with a wait period to make sure things shutdown smoothly
        self.stop()
        time.sleep(3)
        self.start()

    def status(self):
        """Get daemon status.

        Args:
            verbose: Print message if True

        Returns:
            result: True if the PID and PID file exists

        """
        # Determine whether pid file exists
        pid = _pid(self.pidfile)
        if bool(pid) is True:
            print('Daemon is running - {}'.format(self.name))
        else:
            print('Daemon is stopped - {}'.format(self.name))
        return bool(pid)

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().
        """
        # Simple comment to pass linter
        pass


def _pid(pidfile):
    """Start the daemon.

    Args:
        pidfile: Name of file containing PID

    Returns:
        result: Value of PID

    """
    # Initialize key varialbes
    result = None

    # Check for a pidfile
    try:
        with open(pidfile, 'r') as pf_handle:
            result = int(pf_handle.read().strip())

    except IOError:
        result = None

    # Return
    return result
