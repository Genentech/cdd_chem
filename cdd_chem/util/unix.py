"""
This module provides unix specific functions.

Created on Jul 1, 2018

@author: albertgo
"""

import shutil
import sys
import subprocess

from cdd_chem.util.io import warn # noqa: F401; # pylint: disable=W0611


def is_unix() -> bool:
    """Check whether running under linux system.
    Parameters
    ---------
    None

    Returns
    -------
    bool
        True if running on Linux; False otherwise.
    """
    return sys.platform.startswith("linux")


def is_darwin() -> bool:
    """Check whether running under Mac OS system.
    Parameters
    ---------
    None

    Returns
    -------
    bool
        True if running on Max OS; False otherwise.
    """
    return sys.platform.startswith("darwin")


def exec_tcsh(cmd: str, fail_on_error: bool = False) -> int:
    """
    Execute command using tcsh.

    Parameters
    ----------
    cmd
        Command to execute
    fail_on_error:
        Flag for whether script should exit on error in executing cmd.
        If True the script will exit on error

    Returns
    -------
    int
        Exit code from command.

    Examples
    ----------
    >>> cdd_chem.exec_tcsh(cmd="ls ~")
    0
    """
    if not is_unix() and not is_darwin():
        return 0   # fake execution on windows for debugging

    tcsh_command = shutil.which("tcsh")
    if tcsh_command is None and fail_on_error:
        warn("Command tcsh can not be located")
        sys.exit(1)

    ex = subprocess.call(f"{tcsh_command} -fc {cmd}", shell=True)
    if ex != 0 and fail_on_error:
        warn(f"Error executing command:\n{cmd}\n")
        sys.exit(ex)
    return ex
