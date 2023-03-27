#!/usr/bin/env python3
"""
(C) 2021 Genentech. All rights reserved.

Tests for cdd_chem package
"""
import os
import subprocess
import sys
import typing


def run_package_tests(argv: typing.List[str]) -> int:
    """Runs package tests."""
    os.environ["CDD_CHEM_PACKAGE_TEST"] = "yes"

    try:
        subprocess.check_call(['pip', 'install', 'scripttest'])
        subprocess.check_call(['pip', 'install', 'pytest'])
        subprocess.check_call(['pytest', '--pyargs', 'cdd_chem'] + argv)
    except subprocess.CalledProcessError:
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(run_package_tests(sys.argv))
