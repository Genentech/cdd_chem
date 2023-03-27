"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""
import pytest_check as check

from cdd_chem.util.unix import exec_tcsh


def test_exec_tcsh():
    com = "ls ~;\nls -l ~"
    check.equal(0, exec_tcsh(com))
