"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""
import pytest_check as check

from cdd_chem.util.string import strip_spaces_as_in_first_line


def test_strip_spaces_as_in_first_line():
    test = '''\n            abc\n            def'''
    res = strip_spaces_as_in_first_line(test)
    check.equal(res, 'abc\ndef')

    test = '''       \n            abc\n            def'''
    res = strip_spaces_as_in_first_line(test, strip_prefix_newline=False)
    check.equal(res, '\n     abc\n     def')
