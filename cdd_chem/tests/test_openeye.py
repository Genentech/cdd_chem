"""
(C) 2020 Genentech. All rights reserved.

Tests for cdd_chem package
"""
import os

import pytest

from .package_test_base import PackageTestBase
from . import valid_oechem_license


@pytest.mark.skipif(valid_oechem_license() is False, reason="No valid OEChem license!")
class TestOpeneye(PackageTestBase):
    """Test class for FASTA depiction."""

    def setup_method(self):
        """Setup method for each test."""
        # pylint: disable=R0201
        os.environ["CDDLIB_TOOLKIT"] = 'openeye'
