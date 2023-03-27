"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""
import os

import pytest_check as check

from cdd_chem.oechem.io import MolInputStream
from cdd_chem.oechem.confomer_generation import ConformerGenerator, CONFOPT_STRAIN


def test_default(shared_datadir):
    coord_sum = 0.0
    with MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf, \
            ConformerGenerator(inf) as conf_in:
        for mol in conf_in:
            coord_sum += mol.coordinates.sum()

    check.almost_equal(230.8392740623094, coord_sum, rel=0.1)


def test_strain(shared_datadir):
    coord_sum = 0.0
    with MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf, \
            ConformerGenerator(inf, CONFOPT_STRAIN) as conf_in:
        for mol in conf_in:
            coord_sum += mol.coordinates.sum()

    check.almost_equal(230.8392740623094, coord_sum, rel=0.1)
