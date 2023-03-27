"""
(C) 2020 Genentech. All rights reserved.

Tests for cdd_chem package
"""

import os

from .package_test_base import PackageTestBase


class TestRDKit(PackageTestBase):
    """Test class for FASTA depiction."""

    def setup_method(self):
        """Setup method for each test."""
        # pylint: disable=R0201
        os.environ["CDDLIB_TOOLKIT"] = 'rdkit'
