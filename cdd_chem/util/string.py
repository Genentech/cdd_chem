"""
Module with string-related functions.

Created on Jul 1, 2018

@author: albertgo
"""

import re


def strip_spaces_as_in_first_line(txt: str, strip_prefix_newline=True) -> str:
    """
    Remove leading spaces from all lines in txt.

    The number of spaces striped is equal to the number of spaces in the
    first line of the text.

    Parameters
    ----------
    txt
        The text to strip.
    strip_prefix_newline
        Flag for whether to remove all newlines from the beginning of
        txt prior to processing.

    Returns
    -------
    str
        txt with leading spaces stripped.

    Examples
    ----------
    >>> t='''\\n            abc\\n            def'''
    >>> cdd_chem.strip_spaces_as_in_first_line(t)
    'abc\\ndef'
    """
    if strip_prefix_newline:
        txt = re.sub("^[\n\a\r]+", "", txt)

    match = re.search('^ +', txt, re.M)
    if not match:
        return txt
    leading_space = '^' + (match.group())
    return re.sub(leading_space, "", txt, 0, re.M)
