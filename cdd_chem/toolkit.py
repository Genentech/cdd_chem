"""
(C) 2020 Genentech. All rights reserved.

Created on Feb 13, 2019

@author: albertgo

Module defining the toolkit in use.
"""
import contextlib
import logging
import os
import typing

_TOOLKIT: typing.Optional[str] = None


def set_toolkit(toolkit: str):
    """Set the toolkit that cdd_chem operations will use.

    Calling this is only required if you want to override the default
    behavior of this package.

    Parameters
    ----------
    toolkit
        one of "openeye" or "rdkit"
    """
    if toolkit not in ("openeye", "rdkit"):
        logging.error(
            "Expected toolkit to be one of (openeye, rdkit); not changing TOOLKIT"
        )
        return
    global _TOOLKIT  # pylint: disable=W0603
    _TOOLKIT = toolkit


def get_toolkit() -> str:
    """Returns the value of which python chem package is currently
    backing cdd_chem operations.

    If there is no current value for the _TOOLKIT private variable
    (set with ``set_toolkit``) then the toolkit will be auto-magically set using:

       - An environment variable CDDLIB_TOOLKIT if it exists
       - Else "openeye" if ``import openeye.oechem`` succeeds
       - Else "rdkit"

    Returns
    -------
    One of "openeye" or "rdkit"
    """
    global _TOOLKIT  # pylint: disable=W0603
    if not _TOOLKIT:
        # determine toolkit to be used when loading molecules
        _TOOLKIT = os.environ.get("CDDLIB_TOOLKIT", "")
        if not _TOOLKIT:
            # default is Openeye but try falling back on RDKit if Openeye is not available
            try:
                # pylint:  disable=unused-import
                import openeye.oechem  # noqa
                _TOOLKIT = "openeye"
            except ModuleNotFoundError:
                _TOOLKIT = "rdkit"
    return _TOOLKIT


@contextlib.contextmanager
def cdd_toolkit(toolkit: str):
    """Provides a context for running code with a particular toolkit

    Example
    -------

    I.e. to explicitly use OpenEye::

      with cdd_toolkit("openeye"):
          ...cdd_chem code...

    Parameters
    ----------
    toolkit
        one of "rdkit" or "openeye"
    """
    old_value = get_toolkit()
    set_toolkit(toolkit)
    try:
        yield None
    finally:
        set_toolkit(old_value)
